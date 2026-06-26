import argparse
import os
import urllib.request
import urllib.parse
import sys

def main():
    parser = argparse.ArgumentParser(description='Download an image from a URL.')
    parser.add_argument('--url', type=str, required=True, help='The URL of the image to download')
    parser.add_argument('--output', type=str, default='./assets', help='The output directory or filename (default: ./assets)')

    args = parser.parse_args()

    # Extract filename from URL
    parsed_url = urllib.parse.urlparse(args.url)
    filename = os.path.basename(parsed_url.path)
    
    # If no filename in path, use a default
    if not filename:
        filename = 'downloaded_image.png'

    # Determine output path
    output_path = args.output
    if os.path.isdir(output_path) or not os.path.splitext(output_path)[1]:
        # It's a directory (or looks like one)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        output_path = os.path.join(output_path, filename)
    else:
        # It's a filename, ensure parent directory exists
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
        with urllib.request.urlopen(req) as response, open(output_path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Successfully downloaded image to {output_path}")
    except Exception as e:
        print(f"Error downloading image: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
