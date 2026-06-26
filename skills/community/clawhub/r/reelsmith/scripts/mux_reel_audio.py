#!/usr/bin/env python3
import argparse
import subprocess


def main():
    ap = argparse.ArgumentParser(description='Mux reel video with narration audio')
    ap.add_argument('--video', required=True)
    ap.add_argument('--audio', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    subprocess.run([
        'ffmpeg', '-y', '-i', args.video, '-i', args.audio,
        '-c:v', 'copy', '-c:a', 'aac', '-shortest', args.output
    ], check=True)
    print(args.output)


if __name__ == '__main__':
    main()
