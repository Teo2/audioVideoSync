import moviepy
from moviepy.editor import *
from moviepy.audio.AudioClip import *

from numpy.lib.scimath import log

import math

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

def get_cost(ratio1, ratio2):
    return abs(log(ratio1 + 0.1) - log(ratio2 + 0.1))

video_times = []
audio_times = []

sample_size = 250
for sample_start in range(0,len(audio_volumes) - sample_size, 500):
    volume_change_ratios = [0.0] * (sample_size - 1)
    for i in range(sample_start + 1, sample_start + sample_size - 1):
        volume_change_ratios[i - sample_start] = audio_volumes[i] / audio_volumes[i-1]

    best_match_index = 0;
    best_cost = sys.float_info.max
    for i in range(0,len(video_volumes) - sample_size):
        cost = 0
        for j in range(i,i + sample_size - 1):
            video_volume_change_ratio = video_volumes[j] / video_volumes[j - 1]
            cost += get_cost(volume_change_ratios[j-i]video_volume_change_ratio)
        if cost <= best_cost:
            best_cost = cost
            best_match_index = i
    audio_times.append(sample_start * clip_length)
    video_times.append(best_match_index * clip_length)

audio_times.append(len(audio_volumes) * clip_length)
video_times.append(len(video_volumes) * clip_length)


print(audio_times)
print(video_times)

def to_time(seconds):
    if int(seconds) % 60 < 10:
        seconds_str = "0" + str(int(seconds) % 60)
    else:
        seconds_str = str(int(seconds) % 60)
    return str(int(seconds) // 60) + ":" + seconds_str

adjusted_clips = []
for i in range(0, len(video_times) - 1):
    #print(to_time(video_times[i]))
    #print(to_time(audio_times[i]))
    adjusted_clips.append(moviepy.video.fx.all.accel_decel(video.subclip(video_times[i], video_times[i + 1]), new_duration = audio_times[i + 1] - audio_times[i], abruptness = 0))

adjusted_video = concatenate_videoclips(adjusted_clips)
video_with_audio = adjusted_video.set_audio(audio)
video_with_audio.write_videofile("adjusted_video.mp4")
