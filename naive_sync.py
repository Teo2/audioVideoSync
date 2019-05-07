import moviepy
from moviepy.editor import *
from moviepy.audio.AudioClip import *

from numpy.lib.scimath import log

import math

video = VideoFileClip("zeroGravity.mp4")
audio = AudioFileClip("zeroGravity.mp3")


#adjusted_video = moviepy.video.fx.all.accel_decel(video, new_duration = audio.duration, abruptness = 0)
video_with_audio = video.set_audio(audio)
video_with_audio.write_videofile("video_with_audio.mp4")
