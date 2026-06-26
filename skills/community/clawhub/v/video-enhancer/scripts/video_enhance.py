#!/usr/bin/env python3
# /// script
# requires-python = ">=3.08"
# ///
"""
Video Enhance Tool
Enhance video quality using filmora cloud AI services

Security Notice:
- This tool uploads videos to external cloud AI services for processing
- Original files are never modified
- Enhanced videos are downloaded and saved locally
- User consent is required before uploading videos
- Cloud-side data is deleted after processing completes
"""

import argparse
import os
import sys
import urllib.request
from pathlib import Path
import json
import time
import string
import secrets
import urllib.error
import subprocess
import hashlib
import uuid
import platform

API_BASE = "https://filmora-cloud-api-alisz.wondershare.cc"

def log_info(msg: str):
    """Print info message"""
    print(f"[INFO] {msg}")


def log_error(msg: str):
    """Print error message"""
    print(f"[ERROR] {msg}", file=sys.stderr)


def log_warn(msg: str):
    """Print warning message"""
    print(f"[WARN] {msg}")

def generate_output_filename(input_path: str, output_dir: str) -> str:
    """Generate output filename based on input"""
    input_path_obj = Path(input_path)
    base_name = input_path_obj.stem
    ext = input_path_obj.suffix
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_name = f"{base_name}_hd_{timestamp}{ext}"
    
    output_filename = os.path.join(output_dir, output_name)
    return convert_windows_path(output_filename)

def get_file_md5(file_path, block_size=4096):
    """
    Calculate the MD5 hash of a specified file.

    :param file_path: File path (string or Path object)
    :param block_size: Block size for reading the file in bytes, default is 4KB
    :return: MD5 hash of the file as a hexadecimal string, or None if the file does not exist
    """
    try:
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(block_size), b''):
                md5.update(chunk)
        return md5.hexdigest()
    except FileNotFoundError:
        # File not found, return None. Can be changed to raise an exception if needed.
        print(f"File not found for MD5 calculation: {file_path}")
        return None
    except Exception as e:
        # Error occurred while calculating MD5
        print(f"Error calculating MD5: {e}")
        return None

def generate_random_string(length=16):
    """Generate a random string of specified length (letters + digits)"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def check_ffmpeg() -> bool:
    """Check if ffmpeg is installed"""
    try:
        subprocess.run(['ffprobe', '-version'], capture_output=True, check=True, timeout=5)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_video_info(video_path: str) -> dict:
    """
    Get video resolution and duration using ffprobe
    Returns: {"width": int, "height": int, "duration": float}
    """
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,r_frame_rate',
            '-show_entries', 'format=duration',
            '-of', 'json',
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        data = json.loads(result.stdout)
        
        stream = data.get('streams', [{}])[0]
        format_info = data.get('format', {})
        
        width = stream.get('width', 0)
        height = stream.get('height', 0)

        duration = float(format_info.get('duration', 0))
        
        return {
            'width': width,
            'height': height,
            'duration': duration
        }
    except Exception as e:
        log_warn(f"Failed to get video info: {e}")
        return {'width': 0, 'height': 0, 'duration': 0, 'fps': 0}

def convert_windows_path(path: str) -> str:
    """Convert Windows path to Unix path if needed"""
    # Handle paths like C:\Users\... or C:/Users/...
    if len(path) >= 2 and path[1] == ':':
        # Windows path detected
        # Convert to Unix format for consistency
        return path.replace('\\', '/')
    return path

def validate_video_file(path: str) -> bool:
    """Validate video file exists and has supported format"""
    # Convert path for checking
    check_path = convert_windows_path(path)
    
    if not os.path.exists(check_path):
        log_error(f"File not found: {path}")
        return False
    
    if not os.path.isfile(check_path):
        log_error(f"Not a file: {path}")
        return False
    
    # Check extension
    ext = Path(path).suffix.lower()
    supported_exts = ['.mp4', '.mov']
    
    if ext not in supported_exts:
        log_error(f"Unsupported video format: {ext}")
        log_info(f"Supported formats: {', '.join(supported_exts)}")
        return False
    
    # Check file size
    size_mb = os.path.getsize(check_path) / (1024 * 1024)
    if size_mb > 1024:
        log_warn(f"File size {size_mb}MB exceeds the 1GB limit.")
        return False
    elif size_mb > 500:
        log_warn(f"File size ({size_mb:.1f}MB) exceeds recommended limit (500MB)")
        log_warn("Large files may take longer to process or fail")
    else:
        log_info(f"File size: {size_mb:.1f}MB")
    
    return True

def get_language_code() -> str:
    if sys.platform == 'win32':
        import ctypes
        buf = ctypes.create_unicode_buffer(85)
        ctypes.windll.kernel32.GetUserDefaultLocaleName(buf, 85)
        return buf.value.replace('-', '_')
    else:
        import locale
        lang, _ = locale.getlocale()
        return lang


def get_device_unique_id():
    parts = [
        platform.system(),
        platform.machine(),
        platform.node(),
        str(uuid.getnode()),
    ]
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def build_auth_headers():
    """
    Build authentication headers
    :return: Dictionary of authentication headers
    """
    request_id = str(uuid.uuid4())

    headers = {
        'X-Request-Id': request_id,
        "X-Language": get_language_code(),
        "X-Device-Id": get_device_unique_id()
    }
    return headers


def enhance(file_info) -> str:
    """    
    Args:
        video_path: Path to input video file
        
    Returns:
        URL of enhanced video
    """
    print(f"[INFO] Starting video enhancement")

    # Step 1: Upload video
    print("[INFO] Uploading video ...")
    resource_id = _upload_video(file_info)
    print(f"[INFO] Video uploaded, ID: {resource_id}")
    
    # Step 2: Submit enhancement task
    print("[INFO] Submitting enhancement task...")
    task_id = _submit_task(file_info, resource_id)
    print(f"[INFO] Task submitted, ID: {task_id}")
    
    # Step 3: Poll for completion
    print("[INFO] Waiting for enhancement to complete...")
    result = _poll_task(task_id)

    # Step 4: Get download URL
    download_url = result.get('video_result')
    if not download_url:
        raise Exception("No output URL in result")
    
    print(f"[INFO] Enhancement completed!")
    return download_url

def create_multipart_formdata(fields: dict, files: dict) -> tuple:
    """
    Create multipart/form-data body and Content-Type header
    :param fields: Dictionary of form fields, values should be strings
    :param files: Dictionary of file fields, values should be (filename, filedata) tuples, filedata should be bytes
    :return: (content_type, body_bytes)
    """
    boundary = '----WebKitFormBoundary' + generate_random_string(16)
    lines = []

    for name, value in fields.items():
        lines.append(f'--{boundary}'.encode())
        lines.append(f'Content-Disposition: form-data; name="{name}"'.encode())
        lines.append(b'')
        lines.append(str(value).encode('utf-8'))

    for name, file_info in files.items():
        if len(file_info) == 3:
            filename, filedata, mime_type = file_info
        else:
            filename, filedata = file_info
            mime_type = 'application/octet-stream'
        lines.append(f'--{boundary}'.encode())
        lines.append(f'Content-Disposition: form-data; name="{name}"; filename="{filename}"'.encode())
        lines.append(f'Content-Type: {mime_type}'.encode())
        lines.append(b'')
        lines.append(filedata)

    lines.append(f'--{boundary}--'.encode())
    lines.append(b'')

    body = b'\r\n'.join(lines)
    content_type = f'multipart/form-data; boundary={boundary}'
    return content_type, body

def send_http_request(url: str, method: str = 'GET', headers: dict = None, data: bytes = None) -> dict:
    """
    Sends an HTTP request and returns the parsed JSON response as a dictionary.
    """
    req = urllib.request.Request(url, method=method, headers=headers or {}, data=data)
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            resp_data = resp.read()
            try:
                return json.loads(resp_data.decode('utf-8'))
            except:
                return {'raw_response': resp_data.decode('utf-8', errors='ignore')}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='ignore')
        raise Exception(f"HTTP {e.code}: {e.reason} - {error_body}")
    except Exception as e:
        raise Exception(f"request error: {e}")

def _upload_video(file_info) -> str:
    """Upload video to Kling and return video ID"""

    upload_url = f"{API_BASE}/open/v1/resources/upload"
    video_path = file_info['video_file']

    # Build headers
    headers = build_auth_headers()

    # Prepare multipart data
    fields = {
        'scene': 'common_video',
        'file_time': int(file_info['video_duration']),
        'width': int(file_info['video_width']),
        'height': int(file_info['video_height']),
        'file_md5': str(file_info['file_md5'])
    }

    ext = Path(video_path).suffix.lower()
    mime_type ='video/mp4' if ext == '.mp4' else 'video/quicktime'
    with open(video_path, 'rb') as f:
        file_data = f.read()
    files = {
        'file': (os.path.basename(video_path), file_data, mime_type)
    }
    content_type, body = create_multipart_formdata(fields, files)
    headers['Content-Type'] = content_type
    
    result = send_http_request(upload_url, method='POST', headers=headers, data=body)
    resource_id = result['data']['resource_id']

    return resource_id

def _submit_task(file_info, resource_id) -> str:
    """Submit enhancement task"""
    task_url = f"{API_BASE}/open/v1/tasks"

    # Build headers
    headers = build_auth_headers()
    headers['Idempotency-Key'] = str(uuid.uuid4())

    data = {
        'task_type': 'vqe',
        'input': {
            'resource_id': str(resource_id),
            'file_info': {
                'file_time': int(file_info['video_duration']),
                'width': int(file_info['video_width']),
                'height': int(file_info['video_height']),
                'file_md5': str(file_info['file_md5'])
            }
        }
    }

    body =  json.dumps(data).encode('utf-8')
    result = send_http_request(task_url, method='POST', headers=headers, data=body)
    task_id = result['data']['task_id']

    return task_id   


def _poll_task(task_id: str, max_attempts: int = 360, interval: int = 5) -> dict:
    """Poll task status until completion"""
    status_url = f"{API_BASE}/open/v1/tasks/{task_id}"
    print(f'poll_url: {status_url}')
    for attempt in range(max_attempts):
        result = send_http_request(status_url)

        if result.get('code', 0) != 0:
            raise Exception(f"Status check failed: {result.get('message', 'Unknown error')}")
        data = result['data']
        status = data['status']
        
        if status == 'SUCCESS':
            return data.get('result', {})
        elif status == 'FAILED':
            raise Exception(f"Task failed: {result.get('msg', {})}")
        elif status in ('RUNNING', 'PENDING'):
            time.sleep(interval)
        else:
            print(f"\r[WARN] Unknown status: {status}", end='', flush=True)
            time.sleep(interval)    
    print()  # New line after progress
    raise Exception(f"Task timeout after {max_attempts * interval} seconds")

def download_video(url: str, output_path: str) -> bool:
    """Download video from URL to local path"""
    log_info(f"Downloading enhanced video to: {output_path}")
    
    try:
        urllib.request.urlretrieve(url, output_path)
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            log_info(f"Video saved: {output_path} ({size_mb:.1f}MB)")
            return True
        else:
            log_error("Downloaded file is empty")
            return False
    except Exception as e:
        log_error(f"Download failed: {e}")
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Enhance video quality using cloud AI services',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Make video clearer
  python video_enhance.py --input "D:\\Videos\\test.mp4"
        """
    )
    
    parser.add_argument('--input', '-i', required=True,
                        help='Input video file path (Windows/Mac format supported)')
    parser.add_argument('--output', '-o', default='',
                        help='Output directory (default: current directory)')
    
    args = parser.parse_args()
    
    # Validate input file
    if not validate_video_file(args.input):
        sys.exit(1)

    # Convert input path for processing
    input_filename = convert_windows_path(args.input)

    #Get video info using ffmpeg
    video_width = 0
    video_height = 0
    video_duration = 0
    if check_ffmpeg():
        info = get_video_info(input_filename)
        video_width = info['width']
        video_height = info['height']
        video_duration = info['duration']
    else:
        log_warn("ffmpeg not found. Video info (resolution, duration) will not be displayed.")
        log_info("Install ffmpeg for better video analysis.")
        sys.exit(1)
    
    if video_width == 0 or video_height == 0 or video_duration == 0 :
        sys.exit(1)

    # Ensure output directory exists
    output_dir = args.output
    if not output_dir:
        output_dir = os.path.dirname(args.input)
    output_dir = convert_windows_path(output_dir)
    if not os.path.exists(output_dir):
        log_info(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename
    output_filename = generate_output_filename(input_filename, output_dir)

    # Generate file md5
    file_md5 = get_file_md5(input_filename)
    if not file_md5:
        log_error('get file md5 error')
        sys.exit(1)
    
    # Show settings
    log_info("Video Enhancement Settings:")
    log_info(f"  Input: {input_filename}")
    log_info(f"  Resolution: {video_width}x{video_height}, Duration: {video_duration}")
    log_info(f"  Md5: {file_md5}")
    log_info(f"  Output: {output_filename}")
    
    try:        
        # Enhance video
        log_info(f"Starting video enhancement using ...")
        
        file_info = {
            'video_file': input_filename,
            'video_width': video_width,
            'video_height': video_height,
            'video_duration': video_duration,
            'file_md5': file_md5
        }
        video_url = enhance(file_info)
        
        # Download enhanced video
        if download_video(video_url, output_filename):
            log_info("=" * 50)
            log_info("Video enhancement completed successfully!")
            log_info(f"Output: {output_filename}")
            log_info("=" * 50)
            sys.exit(0)
        else:
            log_error("Failed to download enhanced video")
            sys.exit(1)
            
    except ValueError as e:
        log_error(f"Configuration error: {e}")
        log_info("Please set the required API key environment variable")
        sys.exit(1)
    except Exception as e:
        log_error(f"Enhancement failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
