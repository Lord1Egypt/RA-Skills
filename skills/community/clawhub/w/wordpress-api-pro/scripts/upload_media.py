#!/usr/bin/env python3
"""Upload media files to WordPress via REST API"""
import argparse, json, os, sys, urllib.request, urllib.parse, urllib.error, mimetypes
from base64 import b64encode

from security import SafetyError, die_safety, fetch_https_media, validate_local_file, warn_insecure_wp_url

def upload_media(url, username, app_credential, file_path, title=None, alt_text=None, caption=None, allow_remote_url=False):
    """Upload a media file to WordPress"""
    api_url = f"{url.rstrip('/')}/wp-json/wp/v2/media"
    credentials = f"{username}:{app_credential}".encode('utf-8')
    auth_header = b64encode(credentials).decode('ascii')
    
    # Determine if file_path is URL or local path
    is_url = file_path.startswith('http://') or file_path.startswith('https://')
    
    if is_url:
        # Remote URL fetching is disabled unless explicitly requested. This
        # prevents prompt-injection driven exfiltration/SSRF in agentic use.
        if not allow_remote_url and os.getenv('WP_ALLOW_REMOTE_URLS') != '1':
            raise SafetyError("Remote media URLs require --allow-remote-url or WP_ALLOW_REMOTE_URLS=1")
        try:
            response, file_data = fetch_https_media(file_path)
            filename = os.path.basename(urllib.parse.urlparse(file_path).path) or 'remote-media'
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
        except SafetyError:
            raise
        except Exception as e:
            print(json.dumps({"error": f"Failed to download file: {str(e)}"}), file=sys.stderr)
            sys.exit(1)
    else:
        # Read local file after validating it is inside an allowed root.
        try:
            safe_path = validate_local_file(file_path, purpose="media file")
        except SafetyError:
            raise
        filename = os.path.basename(safe_path)
        content_type, _ = mimetypes.guess_type(safe_path)
        if not content_type:
            content_type = 'application/octet-stream'
        
        try:
            with open(safe_path, 'rb') as f:
                file_data = f.read()
        except Exception as e:
            print(json.dumps({"error": f"Failed to read file: {str(e)}"}), file=sys.stderr)
            sys.exit(1)
    
    # Prepare multipart form data manually
    boundary = '----WebKitFormBoundary' + ''.join([str(x) for x in os.urandom(16)])
    body = []
    
    # Add file
    body.append(f'--{boundary}'.encode())
    body.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode())
    body.append(f'Content-Type: {content_type}'.encode())
    body.append(b'')
    body.append(file_data)
    
    # Add metadata
    if title:
        body.append(f'--{boundary}'.encode())
        body.append(b'Content-Disposition: form-data; name="title"')
        body.append(b'')
        body.append(title.encode('utf-8'))
    
    if alt_text:
        body.append(f'--{boundary}'.encode())
        body.append(b'Content-Disposition: form-data; name="alt_text"')
        body.append(b'')
        body.append(alt_text.encode('utf-8'))
    
    if caption:
        body.append(f'--{boundary}'.encode())
        body.append(b'Content-Disposition: form-data; name="caption"')
        body.append(b'')
        body.append(caption.encode('utf-8'))
    
    body.append(f'--{boundary}--'.encode())
    body.append(b'')
    
    body_bytes = b'\r\n'.join(body)
    
    # Create request
    request = urllib.request.Request(api_url, data=body_bytes, method='POST')
    request.add_header('Authorization', f'Basic {auth_header}')
    request.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    
    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(json.dumps({"error": f"HTTP {e.code}: {error_body}"}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

def set_featured_image(url, username, app_credential, post_id, media_id):
    """Set featured image for a post"""
    api_url = f"{url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
    credentials = f"{username}:{app_credential}".encode('utf-8')
    auth_header = b64encode(credentials).decode('ascii')
    
    data = {'featured_media': media_id}
    
    request = urllib.request.Request(api_url, data=json.dumps(data).encode('utf-8'), method='POST')
    request.add_header('Authorization', f'Basic {auth_header}')
    request.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Upload media to WordPress')
    parser.add_argument('--url', default=os.getenv('WP_URL'))
    parser.add_argument('--username', default=os.getenv('WP_USERNAME'))
    parser.add_argument('--app-password', default=os.getenv('WP_APP_PASSWORD'))
    parser.add_argument('--file', required=True, help='Local file path or URL')
    parser.add_argument('--title', help='Media title')
    parser.add_argument('--alt-text', help='Alt text for images')
    parser.add_argument('--caption', help='Media caption')
    parser.add_argument('--set-featured', action='store_true', help='Set as featured image')
    parser.add_argument('--post-id', type=int, help='Post ID (required with --set-featured)')
    parser.add_argument('--allow-remote-url', action='store_true', help='Explicitly allow fetching HTTPS remote media URLs')

    args = parser.parse_args()

    if not all([args.url, args.username, args.app_password]):
        print(json.dumps({"error": "Missing credentials"}), file=sys.stderr)
        sys.exit(1)
    warn_insecure_wp_url(args.url)

    if args.set_featured and not args.post_id:
        print(json.dumps({"error": "--post-id required when using --set-featured"}), file=sys.stderr)
        sys.exit(1)

    # Upload media
    try:
        result = upload_media(
            args.url,
            args.username,
            args.app_password,
            args.file,
            title=args.title,
            alt_text=args.alt_text,
            caption=args.caption,
            allow_remote_url=args.allow_remote_url,
        )
    except SafetyError as e:
        die_safety(e)

    # Set as featured image if requested
    if args.set_featured and 'id' in result:
        set_featured_image(args.url, args.username, args.app_password, args.post_id, result['id'])
        result['featured_image_set'] = True

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
