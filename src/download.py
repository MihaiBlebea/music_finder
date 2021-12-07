from pytube import YouTube
import argparse
from pathlib import Path
from dotenv import dotenv_values
import string
import re


ROOT_PATH = Path(__file__).parent.resolve()

config = dotenv_values(f"{ROOT_PATH}/../.env")

def main():
	parser = argparse.ArgumentParser(
		prog= "music_finder", 
		usage="%(prog)s [options]", 
		description="download music from youtube.",
	)

	parser.add_argument(
		"-l",
		"--link",
		dest="link",
		required=False,
		help="provide link to download music from",
	)

	parser.add_argument(
		"-i",
		"--input",
		dest="input",
		required=False,
		help="input file with youtube links",
	)

	args = parser.parse_args()

	if args.link is not None:
		# download from link
		download_to_file(args.link)
		return

	if args.input is not None:
		# download from input file
		get_links_from_file(args.input)
		return

	print("No input was supplied")


def get_links_from_file(input_file: str):
	input_file = open(input_file, "r")
	lines = input_file.readlines()
	
	for line in lines:
		link = line.strip()
		download_to_file(link)


def download_to_file(youtube_link: str):
	yt = YouTube(youtube_link)
	stream = yt.streams.filter(only_audio=True).get_audio_only()
	file_name = f"{format_file_name(yt.title)}.mp4"
	download_path = config["DOWNLOAD_PATH"]
	stream.download(download_path, filename=file_name)


def format_file_name(file_name: str)-> str:
	chars = re.escape(string.punctuation)
	parts = re.sub(r'['+chars+']', '', file_name).split(" ")
	return "_".join(parts).replace("__", "_")


if __name__ == "__main__":
	main()