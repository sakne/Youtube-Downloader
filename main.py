import sys
import subprocess
import pkg_resources

required  = {'pytube', 'moviepy'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed

if missing:
    # implement pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

from pytube import YouTube
from moviepy.editor import VideoFileClip
import logging
import time
import os

logging.getLogger('moviepy').setLevel(logging.ERROR)

def download(url, quality, format):
	yt = YouTube(url)
	print(f'\n[*] Title: {yt.title}')
	print(f'[*] Publish Date: {yt.publish_date}')
	print(f'[*] Length of video: {yt.length} seconds\n')

	start_time = time.time()  # Add start time variable

	# Use list to map quality number to resolution
	quality_resolution_mapping = [
		None,  # Quality 0 is not valid
		'144p',  # Quality 1 corresponds to resolution 144p
		'240p',  # Quality 2 corresponds to resolution 240p
		'360p',  # Quality 3 corresponds to resolution 360p
		'480p',  # Quality 4 corresponds to resolution 480p
		'720p',  # Quality 5 corresponds to resolution 720p
		'1080p',  # Quality 6 corresponds to resolution 1080p
		'1440p',  # Quality 7 corresponds to resolution 1440p
		'2160p'  # Quality 8 corresponds to resolution 2160p
	]

	# Convert quality to integer
	try:
		quality_int = int(quality)
	except ValueError:
		# Handle invalid input
		if quality == 'max':
			# Find maximum available resolution
			available_resolutions = [stream.resolution for stream in
									 yt.streams.filter(progressive=True)]
			resolution = max(available_resolutions, default=None)
		else:
			print('Invalid quality')
			return
	else:
		# Handle valid input
		if quality_int < 1 or quality_int > 8:
			print('Invalid quality')
			return
		resolution = quality_resolution_mapping[quality_int]


	if resolution not in [stream.resolution for stream in
						  yt.streams.filter(progressive=True)]:
		print(f'{resolution} resolution is not available for this video')
		return

	yt.streams.filter(progressive=True, res=resolution).first().download()

	cleaned_Title = yt.title.replace("/", "")

	end_time = time.time()
	time_spent = end_time - start_time
	print(f'[*] Video downloaded successfully from [{url}] in {int(time_spent)} seconds')

	if format == 'mp3':
		print(f'[*] Converting the [{yt.title}] to mp3 format')
		videoclip = VideoFileClip(f'{cleaned_Title}.mp4')
		audioclip = videoclip.audio
		audioclip.write_audiofile(f'{cleaned_Title}.mp3')
		audioclip.close()
		print(f'[*] [{yt.title}] converted successfully to mp3 format')



os.system('cls' if os.name=='nt' else 'clear')
userinput = input("[*] Enter the URL: ")
print("=====================\n[*]  1: 144p \n[*]  2: 240p\n[*]  3: 360p\n[*]  4: 480p\n[*]  5: 720p\n[*]  max: Highest available\n=====================")
quality = input("[*] Enter the quality: ")
print("Available Formats : mp4, mp3")
format = input("[*] Enter the Output Format: ")

download(userinput, quality, format)
