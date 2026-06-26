import argparse
import os
import urllib.request
import sys

def main():
    parser = argparse.ArgumentParser(description='Download a video from a URL.')
    parser.add_argument('--url', type=str, required=True, help='The URL of the video to download')
    parser.add_argument('--output', type=str, default='./assets/video.mp4', help='The output directory or filename (default: ./assets/video.mp4)')

    args = parser.parse_args()

    # Determine output path and filename
    default_filename = 'video.mp4'
    output_path = args.output

    if os.path.isdir(output_path) or not os.path.splitext(output_path)[1]:
        # It's a directory (or looks like one because it has no extension)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_path = os.path.join(output_path, default_filename)
    else:
        # It's a filename with an extension, ensure parent directory exists
        parent_dir = os.path.dirname(output_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

    print(f"Downloading {args.url} to {output_path}...")

    try:
        # Some servers check for a User-Agent header
        req = urllib.request.Request(
            args.url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        )
        with urllib.request.urlopen(req) as response:
            with open(output_path, 'wb') as out_file:
                # Chunked writing for large video files
                chunk_size = 1024 * 1024  # 1MB
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
        print(f"Successfully downloaded video to {output_path}")
    except Exception as e:
        print(f"Error downloading video: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
