#!/usr/bin/env python3
"""
QQ Zone Photos Manager — CLI utility for managing QQ Zone (QQ空间) photo albums.

Supports:
  - QR code login
  - List albums
  - List photos in an album
  - Download a single photo / all photos in an album
  - Upload a photo to an album
  - Create a new album
"""

import os
import re
import sys
import json
import time
import hashlib
import argparse
import random
import string
from urllib.parse import urlencode, quote

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: requests. Install with: pip install requests")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
QZONE_BASE = "https://user.qzone.qq.com"
QZONE_API = "https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin"
UPLOAD_API = "https://up.qzone.qq.com/cgi-bin/upload/cgi_upload_image"
QRCODE_LOGIN_URL = "https://ssl.ptlogin2.qq.com/ptqrshow"
QRCODE_CHECK_URL = "https://ssl.ptlogin2.qq.com/ptqrlogin"
SKEY_URL = "https://ptlogin2.qzone.qq.com/check_sig"

DEFAULT_COOKIES_FILE = "cookies.json"

# Common headers to mimic a browser request
COMMON_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://user.qzone.qq.com/",
    "Origin": "https://user.qzone.qq.com",
}


# ---------------------------------------------------------------------------
# Helper: compute the *g_tk* token from *p_skey*
# ---------------------------------------------------------------------------
def compute_gtk(p_skey: str) -> int:
    """Compute the g_tk (anti-CSRF) token from p_skey cookie."""
    h = 5381
    for ch in p_skey:
        h += (h << 5) + ord(ch)
    return h & 0x7FFFFFFF


# ---------------------------------------------------------------------------
# Cookie management
# ---------------------------------------------------------------------------
def load_cookies(path: str) -> dict:
    """Load cookies from a JSON file."""
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cookies(path: str, cookies: dict) -> None:
    """Save cookies to a JSON file."""
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2, ensure_ascii=False)
    print(f"Cookies saved to {path}")


def build_session(cookies: dict) -> requests.Session:
    """Build a requests.Session pre-loaded with QQ Zone cookies."""
    session = requests.Session()
    session.headers.update(COMMON_HEADERS)

    cookie_mapping = {
        "p_skey": cookies.get("p_skey", ""),
        "skey": cookies.get("skey", ""),
        "uin": cookies.get("uin", ""),
        "p_uin": cookies.get("uin", ""),
    }
    for k, v in cookie_mapping.items():
        session.cookies.set(k, v, domain=".qq.com")
    return session


# ---------------------------------------------------------------------------
# QR Code Login
# ---------------------------------------------------------------------------
def qr_login(cookies_path: str) -> dict:
    """
    Perform QR code login for QQ Zone.
    Returns a dict of cookies on success.
    """
    session = requests.Session()
    session.headers.update(COMMON_HEADERS)

    # Step 1 — fetch the QR code image
    ts = int(time.time() * 1000)
    qr_params = {
        "appid": "549000912",
        "e": "2",
        "l": "M",
        "s": "3",
        "d": "72",
        "v": "4",
        "t": str(random.random()),
        "daid": "5",
        "pt_3rd_aid": "0",
    }
    resp = session.get(QRCODE_LOGIN_URL, params=qr_params)
    if resp.status_code != 200:
        print("Error: Failed to fetch QR code.")
        return {}

    # Try to render the QR code in terminal
    qr_image_path = "/tmp/qq_login_qr.png"
    with open(qr_image_path, "wb") as f:
        f.write(resp.content)

    _display_qr(qr_image_path)

    # Extract qrsig from cookies
    qrsig = session.cookies.get("qrsig", "")
    if not qrsig:
        print("Error: No qrsig cookie received.")
        return {}

    # Step 2 — poll for scan result
    print("\nWaiting for QR code scan...")
    ptqrtoken = _hash33(qrsig)

    for attempt in range(120):  # 2 min timeout
        time.sleep(2)
        check_params = {
            "u1": "https://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
            "ptqrtoken": str(ptqrtoken),
            "ptredirect": "0",
            "h": "1",
            "t": "1",
            "g": "1",
            "from_ui": "1",
            "ptlang": "2052",
            "action": f"0-0-{int(time.time() * 1000)}",
            "js_ver": "24042516",
            "js_type": "1",
            "login_sig": "",
            "pt_uistyle": "40",
            "aid": "549000912",
            "daid": "5",
            "pt_3rd_aid": "0",
        }
        resp = session.get(QRCODE_CHECK_URL, params=check_params)
        text = resp.text

        if "'登录成功'" in text or "登录成功" in text:
            print("QR code login successful!")
            # Extract redirect URL
            redirect_match = re.search(r"'(https?://[^']+)'", text)
            if redirect_match:
                redirect_url = redirect_match.group(1)
                # Follow redirect to get p_skey / skey
                resp2 = session.get(redirect_url, allow_redirects=False)
                # Collect cookies
                all_cookies = {c.name: c.value for c in session.cookies}
                # Also capture from the redirect response
                for c in resp2.cookies:
                    all_cookies[c.name] = c.value

                # Extract QQ number from uin cookie
                uin = all_cookies.get("uin", "")
                qq_number = uin.lstrip("o").lstrip("0") if uin else ""

                result = {
                    "qq_number": qq_number,
                    "p_skey": all_cookies.get("p_skey", ""),
                    "skey": all_cookies.get("skey", ""),
                    "uin": uin,
                }
                save_cookies(cookies_path, result)
                return result

        if "'二维码已失效'" in text:
            print("QR code expired. Please restart login.")
            return {}

        status_match = re.search(r"ptuiCB\('(\d+)'", text)
        if status_match:
            code = status_match.group(1)
            if code == "66":
                # QR code not yet scanned
                if attempt % 10 == 0:
                    print("Waiting for QR code scan...")
            elif code == "67":
                # QR code scanned, waiting for confirmation on phone
                print("QR code scanned, waiting for confirmation...")
            elif code == "65":
                print("QR code expired. Please restart login.")
                return {}

    print("QR code login timed out.")
    return {}


def _hash33(s: str) -> int:
    """Hash function used by QQ for ptqrtoken."""
    e = 0
    for ch in s:
        e += (e << 5) + ord(ch)
    return 2147483647 & e


def _display_qr(image_path: str) -> None:
    """Display QR code — opens in system viewer and renders in terminal."""
    import subprocess
    import platform

    print(f"\nQR code image saved to: {image_path}")
    print("Scan with your QQ mobile app.\n")

    # Try to open the QR image in the system's default image viewer
    try:
        system = platform.system()
        if system == "Darwin":
            subprocess.Popen(["open", image_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("(QR code image opened in Preview)")
        elif system == "Linux":
            subprocess.Popen(["xdg-open", image_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("(QR code image opened in default viewer)")
        elif system == "Windows":
            os.startfile(image_path)
            print("(QR code image opened in default viewer)")
    except Exception:
        pass

    # Also try to render a compact QR in terminal using half-block characters
    try:
        from PIL import Image

        img = Image.open(image_path).convert("L")
        # Find the QR code bounds (crop white border)
        pixels = img.load()
        w, h = img.size

        # Threshold to binary
        threshold = 128
        binary = [[1 if pixels[x, y] < threshold else 0 for x in range(w)] for y in range(h)]

        # Find bounding box of the QR modules
        top, bottom, left, right = h, 0, w, 0
        for y in range(h):
            for x in range(w):
                if binary[y][x]:
                    top = min(top, y)
                    bottom = max(bottom, y)
                    left = min(left, x)
                    right = max(right, x)

        if top >= bottom or left >= right:
            return

        # Crop to QR area with small padding
        pad = 2
        top = max(0, top - pad)
        bottom = min(h - 1, bottom + pad)
        left = max(0, left - pad)
        right = min(w - 1, right + pad)

        qr_h = bottom - top + 1
        qr_w = right - left + 1

        # Determine module size (find the smallest run of same-color pixels)
        # Sample the top finder pattern to estimate module size
        module_size = 1
        run = 0
        first_color = binary[top][left]
        for x in range(left, right + 1):
            if binary[top + qr_h // 4][x] == first_color:
                run += 1
            else:
                if run > 1:
                    module_size = run
                    break
                first_color = binary[top + qr_h // 4][x]
                run = 1

        if module_size < 1:
            module_size = 1

        # Sample one pixel per module to get a clean grid
        modules_x = qr_w // module_size
        modules_y = qr_h // module_size

        # Use Unicode half-block rendering: each character = 2 rows
        # ▀ (upper half) = top black, bottom white
        # ▄ (lower half) = top white, bottom black
        # █ (full block) = both black
        # ' ' (space)    = both white
        print("")
        for row in range(0, modules_y, 2):
            line = "  "  # left margin
            for col in range(modules_x):
                py1 = top + row * module_size + module_size // 2
                py2 = top + (row + 1) * module_size + module_size // 2 if row + 1 < modules_y else -1
                px = left + col * module_size + module_size // 2

                if px > right:
                    break

                top_black = binary[py1][px] if 0 <= py1 < h and 0 <= px < w else 0
                bottom_black = binary[py2][px] if 0 <= py2 < h and 0 <= px < w and py2 >= 0 else 0

                if top_black and bottom_black:
                    line += "█"
                elif top_black and not bottom_black:
                    line += "▀"
                elif not top_black and bottom_black:
                    line += "▄"
                else:
                    line += " "
            print(line)
        print("")
    except Exception as e:
        print(f"(Terminal QR rendering failed: {e})")
        print(f"Please open the QR code image manually: {image_path}")


# ---------------------------------------------------------------------------
# Album operations
# ---------------------------------------------------------------------------
def list_albums(session: requests.Session, qq: str, g_tk: int) -> dict:
    """List all photo albums for a QQ user."""
    url = f"{QZONE_API}/fcg_list_album_v3"
    params = {
        "g_tk": g_tk,
        "callback": "_Callback",
        "t": str(int(time.time() * 1000)),
        "hostUin": qq,
        "uin": qq,
        "appid": "4",
        "inCharset": "utf-8",
        "outCharset": "utf-8",
        "source": "qzone",
        "plat": "qzone",
        "format": "jsonp",
        "notice": "0",
        "filter": "1",
        "handset": "4",
        "pageNumModeSort": "40",
        "pageNumModeClass": "15",
        "needUserInfo": "1",
        "idcNum": "4",
    }
    resp = session.get(url, params=params)
    data = _parse_jsonp(resp.text)
    if not data:
        return {"error": "Failed to parse response", "raw": resp.text[:500]}

    albums = []
    album_list = data.get("data", {}).get("albumListModeSort", [])
    if not album_list:
        album_list = data.get("data", {}).get("albumListModeClass", [])

    for album in album_list:
        albums.append({
            "id": album.get("id", ""),
            "name": album.get("name", ""),
            "total": album.get("total", 0),
            "createtime": album.get("createtime", ""),
            "modifytime": album.get("modifytime", ""),
            "desc": album.get("desc", ""),
        })

    return {"total": len(albums), "albums": albums}


def create_album(session: requests.Session, qq: str, g_tk: int, title: str, desc: str = "") -> dict:
    """Create a new photo album."""
    url = f"{QZONE_API}/fcg_create_album"
    params = {
        "g_tk": g_tk,
        "callback": "_Callback",
        "t": str(int(time.time() * 1000)),
        "hostUin": qq,
        "uin": qq,
        "appid": "4",
        "inCharset": "utf-8",
        "outCharset": "utf-8",
        "source": "qzone",
        "plat": "qzone",
        "format": "jsonp",
        "notice": "0",
    }
    form_data = {
        "qzonetoken": "",
        "albumname": title,
        "albumdesc": desc,
        "priv": "1",  # 1=public, 3=friends, 4=private
        "question": "",
        "answer": "",
    }
    resp = session.post(url, params=params, data=form_data)
    data = _parse_jsonp(resp.text)
    if not data:
        return {"error": "Failed to parse response", "raw": resp.text[:500]}
    return data


def list_photos(session: requests.Session, qq: str, g_tk: int, album_id: str, page: int = 0, page_size: int = 500) -> dict:
    """List photos in a given album."""
    url = f"{QZONE_API}/cgi_list_photo"
    params = {
        "g_tk": g_tk,
        "callback": "_Callback",
        "t": str(int(time.time() * 1000)),
        "mode": "0",
        "idcNum": "4",
        "hostUin": qq,
        "topicId": album_id,
        "noTopic": "0",
        "uin": qq,
        "pageStart": str(page),
        "pageNum": str(page_size),
        "skipCmt498": "0",
        "singleurl": "1",
        "batchId": "",
        "notice": "0",
        "appid": "4",
        "inCharset": "utf-8",
        "outCharset": "utf-8",
        "source": "qzone",
        "plat": "qzone",
        "outstyle": "json",
        "format": "jsonp",
        "json_compat": "1",
        "need_private_comment": "1",
    }
    resp = session.get(url, params=params)
    data = _parse_jsonp(resp.text)
    if not data:
        return {"error": "Failed to parse response", "raw": resp.text[:500]}

    photos = []
    photo_list = data.get("data", {}).get("photoList", [])
    for photo in photo_list:
        # Prefer the largest resolution URL available
        url_candidates = [
            photo.get("raw", ""),
            photo.get("url", ""),
            photo.get("custom_url", ""),
            photo.get("origin_url", ""),
        ]
        best_url = ""
        for u in url_candidates:
            if u:
                best_url = u
                break

        photos.append({
            "lloc": photo.get("lloc", ""),
            "name": photo.get("name", ""),
            "desc": photo.get("desc", ""),
            "url": best_url,
            "width": photo.get("width", 0),
            "height": photo.get("height", 0),
            "uploadtime": photo.get("uploadtime", ""),
        })

    return {
        "album_id": album_id,
        "total": data.get("data", {}).get("totalInPage", len(photos)),
        "photos": photos,
    }


# ---------------------------------------------------------------------------
# Download operations
# ---------------------------------------------------------------------------
def download_photo(session: requests.Session, photo_url: str, output_dir: str, filename: str = "") -> str:
    """Download a single photo to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    if not filename:
        filename = photo_url.split("/")[-1].split("?")[0]
        if not filename:
            filename = f"photo_{int(time.time() * 1000)}.jpg"

    filepath = os.path.join(output_dir, filename)
    resp = session.get(photo_url, stream=True)
    if resp.status_code != 200:
        print(f"Error downloading {photo_url}: HTTP {resp.status_code}")
        return ""

    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    # Auto-detect file extension if missing
    _, ext = os.path.splitext(filepath)
    if not ext:
        content_type = resp.headers.get("Content-Type", "")
        ext_map = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "image/bmp": ".bmp",
        }
        detected_ext = ext_map.get(content_type.split(";")[0].strip(), "")
        if not detected_ext:
            # Detect from file magic bytes
            try:
                with open(filepath, "rb") as f:
                    header = f.read(8)
                if header[:3] == b'\xff\xd8\xff':
                    detected_ext = ".jpg"
                elif header[:8] == b'\x89PNG\r\n\x1a\n':
                    detected_ext = ".png"
                elif header[:6] in (b'GIF87a', b'GIF89a'):
                    detected_ext = ".gif"
                elif header[:4] == b'RIFF' and header[8:12] == b'WEBP':
                    detected_ext = ".webp"
            except Exception:
                pass
        if detected_ext:
            new_filepath = filepath + detected_ext
            os.rename(filepath, new_filepath)
            filepath = new_filepath

    print(f"Downloaded: {filepath}")
    return filepath


def download_album(session: requests.Session, qq: str, g_tk: int, album_id: str, output_dir: str) -> list:
    """Download all photos from an album."""
    result = list_photos(session, qq, g_tk, album_id)
    if "error" in result:
        print(f"Error listing photos: {result['error']}")
        return []

    photos = result.get("photos", [])
    if not photos:
        print("No photos found in this album.")
        return []

    album_dir = os.path.join(output_dir, album_id)
    os.makedirs(album_dir, exist_ok=True)

    downloaded = []
    total = len(photos)
    for idx, photo in enumerate(photos, 1):
        url = photo.get("url", "")
        if not url:
            print(f"[{idx}/{total}] Skipping photo with no URL: {photo.get('name', 'unknown')}")
            continue

        name = photo.get("name", "") or f"photo_{idx}.jpg"
        print(f"[{idx}/{total}] Downloading: {name}")
        path = download_photo(session, url, album_dir, name)
        if path:
            downloaded.append(path)

        # Polite delay to avoid rate limiting
        time.sleep(0.5)

    print(f"\nDownloaded {len(downloaded)}/{total} photos to {album_dir}")
    return downloaded


# ---------------------------------------------------------------------------
# Upload operations
# ---------------------------------------------------------------------------
def upload_photo(session: requests.Session, qq: str, g_tk: int, photo_path: str, album_id: str = "") -> dict:
    """Upload a photo to QQ Zone."""
    if not os.path.exists(photo_path):
        return {"error": f"File not found: {photo_path}"}

    filename = os.path.basename(photo_path)
    filesize = os.path.getsize(photo_path)

    # Build upload URL with g_tk in query string
    url = f"{UPLOAD_API}?g_tk={g_tk}"

    # Authentication and upload parameters go in the multipart form data body
    form_data = {
        "filename": "filename",
        "zzpaneluin": qq,
        "zzpanelkey": "",
        "p_uin": qq,
        "uin": qq,
        "p_skey": session.cookies.get("p_skey", ""),
        "skey": session.cookies.get("skey", ""),
        "qzone_token": "",
        "backUrls": f"http://user.qzone.qq.com/{qq}",
        "o_uin": qq,
        "uploadtype": "1",
        "albumtype": "7",
        "phototype": "0",
        "uploadHd": "1",
        "hd": "1",
        "compatible": "1",
        "output_type": "jsonhtml",
        "output_charset": "utf-8",
        "charset": "utf-8",
        "jsonhtml_callback": "callback",
    }
    if album_id:
        form_data["albumid"] = album_id

    with open(photo_path, "rb") as f:
        files = {"filename": (filename, f, "image/jpeg")}
        resp = session.post(url, data=form_data, files=files)

    # Parse the response
    text = resp.text
    # The response is wrapped in HTML: <script>...frameElement._Callback({...});</script>
    # First try to extract the _Callback JSON payload
    cb_match = re.search(r'_Callback\((.*?)\)\s*;?\s*</script>', text, re.DOTALL)
    if cb_match:
        try:
            data = json.loads(cb_match.group(1))
            if data.get("ret") == 0 and "data" in data:
                upload_data = data["data"]
                return {
                    "success": True,
                    "ret": 0,
                    "url": upload_data.get("url", ""),
                    "origin_url": upload_data.get("origin_url", ""),
                    "album_id": upload_data.get("albumid", ""),
                    "lloc": upload_data.get("lloc", ""),
                    "width": upload_data.get("width", 0),
                    "height": upload_data.get("height", 0),
                    "contentlen": upload_data.get("contentlen", 0),
                }
            return data
        except json.JSONDecodeError:
            pass

    # Fallback: try to find any JSON object in the response
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group())
            return data
        except json.JSONDecodeError:
            pass

    return {"success": False, "raw_response": text[:500]}


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------
def _parse_jsonp(text: str) -> dict:
    """Parse a JSONP response into a Python dict."""
    if not text:
        return {}
    # Remove JSONP callback wrapper: _Callback({...})
    match = re.search(r'_Callback\((.*)\)', text, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # Try plain JSON
        json_str = text.strip()

    # Clean up non-standard JSON
    json_str = json_str.strip().rstrip(";")

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Try to fix common issues
        try:
            # Replace single quotes with double quotes as a fallback
            fixed = json_str.replace("'", '"')
            return json.loads(fixed)
        except json.JSONDecodeError:
            return {}


def _get_qq_from_cookies(cookies: dict) -> str:
    """Extract QQ number from cookies."""
    qq = cookies.get("qq_number", "")
    if not qq:
        uin = cookies.get("uin", "")
        qq = uin.lstrip("o").lstrip("0") if uin else ""
    return qq


# ---------------------------------------------------------------------------
# Main CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="QQ Zone Photos Manager — CLI utility for QQ空间 photo albums"
    )
    parser.add_argument(
        "--action",
        choices=["login", "list", "photos", "download", "download-album", "upload", "create"],
        required=True,
        help="Action to perform",
    )
    parser.add_argument("--qq", help="QQ number of the target user")
    parser.add_argument("--title", help="Album title (for create action)")
    parser.add_argument("--desc", default="", help="Album description (for create action)")
    parser.add_argument("--photo", help="Photo file path (for upload action)")
    parser.add_argument("--album-id", help="Album ID")
    parser.add_argument("--url", help="Photo URL (for download action)")
    parser.add_argument("--output", default="./downloads", help="Output directory for downloads")
    parser.add_argument(
        "--cookies",
        default=DEFAULT_COOKIES_FILE,
        help="Path to cookies JSON file",
    )

    args = parser.parse_args()

    # ----- Login action (no cookies required) -----
    if args.action == "login":
        result = qr_login(args.cookies)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("Login failed.")
            sys.exit(1)
        return

    # ----- All other actions require cookies -----
    cookies = load_cookies(args.cookies)
    if not cookies or not cookies.get("p_skey"):
        print(f"Error: Valid cookies not found at {args.cookies}")
        print("Please run with --action login first, or provide a valid cookies.json file.")
        sys.exit(1)

    session = build_session(cookies)
    g_tk = compute_gtk(cookies["p_skey"])
    qq = args.qq or _get_qq_from_cookies(cookies)

    if not qq:
        print("Error: QQ number is required. Provide --qq or include qq_number in cookies.")
        sys.exit(1)

    # ----- Dispatch actions -----
    if args.action == "list":
        result = list_albums(session, qq, g_tk)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.action == "photos":
        if not args.album_id:
            print("Error: --album-id is required for photos action")
            sys.exit(1)
        result = list_photos(session, qq, g_tk, args.album_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.action == "download":
        if not args.url:
            print("Error: --url is required for download action")
            sys.exit(1)
        path = download_photo(session, args.url, args.output)
        if path:
            print(json.dumps({"downloaded": path}, indent=2))
        else:
            print("Download failed.")
            sys.exit(1)

    elif args.action == "download-album":
        if not args.album_id:
            print("Error: --album-id is required for download-album action")
            sys.exit(1)
        downloaded = download_album(session, qq, g_tk, args.album_id, args.output)
        print(json.dumps({"downloaded_count": len(downloaded), "files": downloaded}, indent=2))

    elif args.action == "upload":
        if not args.photo:
            print("Error: --photo path is required for upload action")
            sys.exit(1)
        result = upload_photo(session, qq, g_tk, args.photo, args.album_id or "")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.action == "create":
        if not args.title:
            print("Error: --title is required for create action")
            sys.exit(1)
        result = create_album(session, qq, g_tk, args.title, args.desc)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
