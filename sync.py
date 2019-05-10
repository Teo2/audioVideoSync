import moviepy
from moviepy.editor import *
from moviepy.audio.AudioClip import *

from numpy.lib.scimath import log

import math

def is_sorted(data):
	for i in range(1,len(data)):
		if(data[i-1] > data[i]):
			return False
	return True

def power_set(a):
	if len(a) == 0:
		return [[]]
	cs = []
	for c in power_set(a[1:]):
		cs += [c,c+[a[0]]]
	return cs

def remove_noise(data):
	min_size = sys.maxsize
	fewest_elements_to_remove = []
	for p in power_set(range(0,len(data))):
		if len(p) < min_size:
			copy = list.copy(data)
			for i in p:
				copy.pop(i)
			if(is_sorted(copy)):
				fewest_elements_to_remove = p
				min_size = len(p)
	fewest_elements_to_remove.sort(reverse = True)
	return fewest_elements_to_remove

'''
def remove_noise(data):
	if(is_sorted(data)):
		return []
	min_length = sys.maxsize
	best_sublist_indicies = []
	best_index = 0
	for i in range(0,len(data)):
		copy = list.copy(data)
		copy.pop(i)
		without_i = remove_noise(copy)
		print(without_i)
		for j in without_i:
			copy.pop(j)
		if(is_sorted(copy) and len(without_i) < min_length):
			min_length = len(without_i)
			best_sublist_indicies = without_i
			best_index = i
	best_sublist_indicies.append(best_index);
	return best_sublist_indicies
'''

#print(remove_noise([1,2,24,25,4,5,26,47,48,47,49,50,51]))

def to_time(seconds):
    if int(seconds) % 60 < 10:
        seconds_str = "0" + str(int(seconds) % 60)
    else:
        seconds_str = str(int(seconds) % 60)
    return str(int(seconds) // 60) + ":" + seconds_str

video = VideoFileClip("zeroGravity.mp4")
audio = AudioFileClip("zeroGravity.mp3")

clip_length = 0.1 #in seconds

def get_volume_array(audio, clip_length):
    cut = lambda i: audio.subclip(i*clip_length,i*clip_length+clip_length).to_soundarray(fps=22000)
    volume = lambda array: np.sqrt(((1.0*array)**2).mean())
    volumes = [volume(cut(i)) for i in range(0,int(audio.duration/clip_length - 2))]
    return volumes

video_volumes = get_volume_array(video.audio, clip_length)
audio_volumes = get_volume_array(audio, clip_length)

steepness = 2.7
def sigmoid(x):
	if math.isnan(x) or math.isinf(x):
		return 1
	return 1/(1 + steepness ** (-x))

def get_cost(ratio1, ratio2):
	return (sigmoid(ratio1) - sigmoid(ratio2)) ** 2

video_times = [0.0]
audio_times = [0.0]

sample_size = 50
for sample_start in range(50,len(audio_volumes) - sample_size, 50):
    volume_change_ratios = [0.0] * (sample_size - 1)
    for i in range(sample_start + 1, sample_start + sample_size - 1):
        volume_change_ratios[i - sample_start] = audio_volumes[i] / audio_volumes[i-1]

    best_match_index = 0;
    best_cost = sys.float_info.max
    for i in range(0,len(video_volumes) - sample_size):
        cost = 0
        for j in range(i,i + sample_size - 1):
            video_volume_change_ratio = video_volumes[j] / video_volumes[j - 1]
            cost += get_cost(volume_change_ratios[j-i],video_volume_change_ratio)
        if cost <= best_cost:
            best_cost = cost
            best_match_index = i
    print("Best " + str(best_cost) + " at " + to_time(best_match_index / clip_length))
    if(best_cost <= 1):
    	audio_times.append(sample_start * clip_length)
    	video_times.append(best_match_index * clip_length)

audio_times.append(len(audio_volumes) * clip_length)
video_times.append(len(video_volumes) * clip_length)

for i in remove_noise(video_times):
	video_times.pop(i)
	audio_times.pop(i)


print(audio_times)
print(video_times)

adjusted_clips = []
for i in range(0, len(video_times) - 1):
    #print(to_time(video_times[i]))
    #print(to_time(audio_times[i]))
    adjusted_clips.append(moviepy.video.fx.all.accel_decel(video.subclip(video_times[i], video_times[i + 1]), new_duration = audio_times[i + 1] - audio_times[i], abruptness = 0))



adjusted_video = concatenate_videoclips(adjusted_clips)
video_with_audio = adjusted_video.set_audio(audio)
video_with_audio.write_videofile("adjusted_video.mp4")
