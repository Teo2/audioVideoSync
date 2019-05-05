import moviepy
from moviepy.editor import *
from moviepy.audio.AudioClip import *

import math

from scipy.io.wavfile import write

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

print(len(video_volumes))
print(len(audio_volumes))




'''
super_cool_new_audio = AudioArrayClip(audio.to_soundarray(),fps=44100)
super_cool_new_audio.write_audiofile("test.mp3")
'''
#sped_up = moviepy.video.fx.all.accel_decel(video, new_duration = audio.duration, abruptness = 0)

#video_with_audio = sped_up.set_audio(audio)

#video_with_audio.write_videofile("spedUp.mp4")
