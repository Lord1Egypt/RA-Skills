import os
import sys
import json
import argparse
import requests
try:
    import brotli
except ImportError:
    brotli = None

COOKIES = os.getenv("YOUDAO_COOKIE")
BASE_URL = "https://note.youdao.com"

def extract_cookie_by_name(cookie_string, name):
    import re
    pattern = rf"{re.escape(name)}=([^;]+)"
    match = re.search(pattern, cookie_string)
    return match.group(1).strip() if match else None

def build_headers(extra_cookie=None):
    if not COOKIES:
        print("Error: YOUDAO_COOKIE environment variable is not set.", file=sys.stderr)
        print("Set it to the full cookie string from browser F12 Network panel.", file=sys.stderr)
        sys.exit(1)
    cstk = extract_cookie_by_name(COOKIES, "YNOTE_CSTK")
    login = extract_cookie_by_name(COOKIES, "YNOTE_LOGIN")
    sess = extract_cookie_by_name(COOKIES, "YNOTE_SESS")
    if not all([cstk, login, sess]):
        print("Error: Cookie must contain YNOTE_CSTK, YNOTE_LOGIN, and YNOTE_SESS.", file=sys.stderr)
        sys.exit(1)
    cookie_header = COOKIES.strip()
    if extra_cookie:
        cookie_header += "; " + extra_cookie
    return {
        "Cookie": cookie_header,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://note.youdao.com/",
        "Origin": "https://note.youdao.com",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

def get_cstk():
    return extract_cookie_by_name(COOKIES, "YNOTE_CSTK")

def build_web_context_params(cstk=None):
    if cstk is None:
        cstk = get_cstk()
    return {
        "_system": "windows",
        "_systemVersion": "",
        "_screenWidth": 1920,
        "_screenHeight": 1080,
        "_appName": "ynote",
        "_appuser": "0123456789abcdeffedcba9876543210",
        "_vendor": "official-website",
        "_launch": 16,
        "_firstTime": "",
        "_deviceId": "0123456789abcdef",
        "_platform": "web",
        "_cityCode": 110000,
        "_cityName": "",
        "_product": "YNote-Web",
        "_version": "",
        "sev": "j1",
        "sec": "v1",
        "keyfrom": "web",
        "cstk": cstk,
    }

def get_root_dir():
    # Attempt to get the root directory, but it might fail with 400 for some account types
    cstk = get_cstk()
    url = f"{BASE_URL}/yws/api/personal/file?method=getByPath&keyfrom=web&cstk={cstk}"
    headers = build_headers()
    data = {"file": "/", "method": "getByPath", "keyfrom": "web", "cstk": cstk}
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 400:
        url_get = f"{BASE_URL}/yws/api/personal/file?method=getByPath&keyfrom=web&file=%2F&cstk={cstk}"
        response = requests.get(url_get, headers=headers)
        
    if response.status_code != 200:
        print("Warning: Failed to get root directory via API. You may need to specify --dir explicitly.", file=sys.stderr)
        print("Tip: You can get your directory ID from the web URL (e.g., https://note.youdao.com/web/#/file/DIR_ID/...)", file=sys.stderr)
        sys.exit(1)
        
    response.raise_for_status()
    data = response.json()
    return data.get("fileEntry", {}).get("id")

def list_files(dir_id=None):
    if not dir_id:
        dir_id = get_root_dir()
    cstk = get_cstk()
    url = f"{BASE_URL}/yws/api/personal/file/{dir_id}?all=true&f=true&len=100&sort=1&isReverse=false&method=listPageByParentId&keyfrom=web&cstk={cstk}"
    headers = build_headers()
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error in list_files: {response.text}", file=sys.stderr)
    response.raise_for_status()
    data = response.json()
    files = []
    for entry in data if isinstance(data, list) else data.get("entries", []):
        file_entry = entry.get("fileEntry", {})
        files.append({
            "id": file_entry.get("id"),
            "name": file_entry.get("name"),
            "is_dir": file_entry.get("dir"),
            "parent_id": file_entry.get("parentId"),
            "path": file_entry.get("path"),
        })
    return files

def search_notes(keyword):
    cstk = get_cstk()
    url = f"{BASE_URL}/yws/api/personal/search"
    headers = build_headers()
    headers["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"

    root_dir = None
    try:
        root_dir = get_root_dir()
    except SystemExit:
        root_dir = None
    except Exception:
        root_dir = None

    params = build_web_context_params(cstk)
    params.update({
        "method": "webSearch",
        "kw": keyword,
        "b": 0,
        "l": 15,
        "sortRules": "default",
    })
    if root_dir:
        params["parentId"] = root_dir

    response = requests.post(url, headers=headers, params=params, data={"cstk": cstk})
    if response.status_code != 200:
        print(f"Error in search_notes: status={response.status_code} body={response.text}", file=sys.stderr)
    response.raise_for_status()
    return response.json()

def _normalize_image_url(url):
    if not isinstance(url, str):
        return None
    cleaned = url.strip().strip("`").strip("\"").strip("'").strip("“").strip("”").strip(",")
    if not cleaned:
        return None
    if cleaned.startswith("/yws/res/"):
        return BASE_URL + cleaned
    if cleaned.startswith("http://") or cleaned.startswith("https://"):
        return cleaned
    if "/yws/res/" in cleaned:
        idx = cleaned.find("/yws/res/")
        return BASE_URL + cleaned[idx:]
    return None

def _find_resource_url(node):
    if isinstance(node, dict):
        for key in ("url", "src", "source", "resource", "11", "12"):
            maybe = _normalize_image_url(node.get(key))
            if maybe:
                return maybe
        for value in node.values():
            maybe = _find_resource_url(value)
            if maybe:
                return maybe
    elif isinstance(node, list):
        for item in node:
            maybe = _find_resource_url(item)
            if maybe:
                return maybe
    elif isinstance(node, str):
        return _normalize_image_url(node)
    return None

def _find_numeric_value(node, key_name):
    if isinstance(node, dict):
        value = node.get(key_name)
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, str) and value.isdigit():
            return int(value)
        for sub in node.values():
            found = _find_numeric_value(sub, key_name)
            if found is not None:
                return found
    elif isinstance(node, list):
        for item in node:
            found = _find_numeric_value(item, key_name)
            if found is not None:
                return found
    return None

def _walk_compress_events(node, events):
    if isinstance(node, dict):
        text = node.get("8")
        if isinstance(text, str) and text.strip():
            events.append({"type": "text", "text": text.strip()})
        img_url = _find_resource_url(node)
        if img_url:
            width = _find_numeric_value(node, "width")
            height = _find_numeric_value(node, "height")
            events.append({
                "type": "image",
                "url": img_url,
                "width": width,
                "height": height
            })
        for value in node.values():
            _walk_compress_events(value, events)
    elif isinstance(node, list):
        for item in node:
            _walk_compress_events(item, events)

def _find_context_text(events, start, step):
    idx = start
    while 0 <= idx < len(events):
        current = events[idx]
        if current.get("type") == "text":
            txt = current.get("text", "").strip()
            if txt:
                return txt
        idx += step
    return ""

def _extract_compress_note_payload(parsed):
    if not isinstance(parsed, dict):
        return None
    if not parsed.get("__compress__"):
        return None
    blocks = parsed.get("5")
    if not isinstance(blocks, list):
        return None
    events = []
    for block in blocks:
        _walk_compress_events(block, events)
    text_tokens = []
    images = []
    for idx, event in enumerate(events):
        if event.get("type") == "text":
            text_tokens.append(event.get("text", ""))
        elif event.get("type") == "image":
            images.append({
                "url": event.get("url", ""),
                "width": event.get("width"),
                "height": event.get("height"),
                "context_before": _find_context_text(events, idx - 1, -1),
                "context_after": _find_context_text(events, idx + 1, 1)
            })
    return {
        "__skill_parsed__": "compressed_note_v2",
        "text": "\n".join([t for t in text_tokens if t]),
        "images": images
    }

def process_response_content(response):
    content_encoding = response.headers.get("Content-Encoding", "")
    raw = response.content
    
    if not raw:
        return ""
    
    was_brotli = (content_encoding == "br" and brotli)
    
    if was_brotli:
        try:
            decompressed = brotli.decompress(raw)
            if len(decompressed) > 10:
                raw = decompressed
        except Exception:
            pass
    
    try:
        text = raw.decode('utf-8', errors='ignore')
        text = text.strip()
        
        if text.startswith("{") or text.startswith("["):
            try:
                parsed = json.loads(text)
                payload = _extract_compress_note_payload(parsed)
                if payload is not None:
                    return json.dumps(payload, ensure_ascii=False)
                return json.dumps(parsed, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                if was_brotli and text.startswith("{"):
                    return text
                pass
        return text
    except Exception:
        return response.text

def _build_web_note_body(content):
    import time

    base_ms = int(time.time() * 1000)

    def seq_token(prefix, offset):
        return f"{prefix}-{base_ms + offset}"

    raw_lines = str(content).splitlines()
    lines = [line.rstrip("\r") for line in raw_lines if line.strip()]
    if not lines and str(content).strip():
        lines = [str(content).strip()]

    blocks = []
    if not lines:
        blocks.append({
            "3": seq_token("3060", 1),
            "5": [{
                "2": "2",
                "3": seq_token("p5PQ", 2)
            }]
        })
    else:
        for idx, line in enumerate(lines):
            blocks.append({
                "3": seq_token("3060", idx * 2 + 1),
                "5": [{
                    "2": "2",
                    "3": seq_token("p5PQ", idx * 2 + 2),
                    "8": line
                }]
            })
    return json.dumps({
        "2": "1",
        "3": seq_token("Ju9C", 0),
        "4": {"fv": "0"},
        "5": blocks,
        "__compress__": True
    }, ensure_ascii=False)

def _looks_like_web_note_content(content):
    if isinstance(content, str):
        if '"__skill_parsed__": "compressed_note_v2"' in content:
            return True
        if '"__compress__"' in content and '"5"' in content:
            return True
    if isinstance(content, dict) and content.get("__skill_parsed__") == "compressed_note_v2":
        return True
    return False

def read_note(file_id):
    cstk = get_cstk()
    url = (
        f"{BASE_URL}/yws/api/personal/sync?method=download&_system=windows&_systemVersion=&"
        f"_screenWidth=1920&_screenHeight=1080&_appName=ynote&_appuser=0123456789abcdeffedcba9876543210&"
        f"_vendor=official-website&_launch=16&_firstTime=&_deviceId=0123456789abcdef&_platform=web&"
        f"_cityCode=110000&_cityName=&sev=j1&keyfrom=web&cstk={cstk}"
    )
    headers = build_headers()
    
    # First attempt: standard download with editorType: 1
    data = {
        "fileId": file_id,
        "version": -1,
        "convert": "true",
        "editorType": 1,
        "cstk": cstk
    }
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        content = process_response_content(response)
        if content and "当前客户端版本过低" not in content and "当前笔记内容暂时无法查看" not in content:
            return content
            
    # Second attempt: try without editorType (for new version notes)
    data_no_editor = {
        "fileId": file_id,
        "version": -1,
        "convert": "true",
        "cstk": cstk
    }
    response2 = requests.post(url, headers=headers, data=data_no_editor)
    if response2.status_code == 200:
        content = process_response_content(response2)
        if content and "当前客户端版本过低" not in content and "当前笔记内容暂时无法查看" not in content:
            return content
            
    # Third attempt: try fallback endpoint for new doc formats
    url_new_format = f"{BASE_URL}/yws/api/personal/file/{file_id}?method=download&all=true&f=true&len=30&sort=1&isReverse=false&keyfrom=web&cstk={cstk}"
    response3 = requests.get(url_new_format, headers=headers)
    if response3.status_code == 200:
        content = process_response_content(response3)
        if content and "当前客户端版本过低" not in content and "当前笔记内容暂时无法查看" not in content:
            return content
            
    # Fourth attempt: try basic sync download
    url_get2 = f"{BASE_URL}/yws/api/personal/sync?method=download&keyfrom=web&id={file_id}&cstk={cstk}"
    response4 = requests.get(url_get2, headers=headers)
    if response4.status_code == 200:
        content = process_response_content(response4)
        if content:
            return content
        
    # All attempts exhausted - return error info with details
    print(f"Warning: Failed to read note {file_id} after all 4 attempts", file=sys.stderr)
    print(f"Attempt 1 status: {response.status_code}, content length: {len(response.content)}", file=sys.stderr)
    print(f"Attempt 2 status: {response2.status_code}, content length: {len(response2.content)}", file=sys.stderr)
    print(f"Attempt 3 status: {response3.status_code}, content length: {len(response3.content)}", file=sys.stderr)
    print(f"Attempt 4 status: {response4.status_code}, content length: {len(response4.content)}", file=sys.stderr)
    
    # Try to return any non-empty content even if it contains the version warning
    for r in [response, response2, response3, response4]:
        if r.status_code == 200:
            c = process_response_content(r)
            if c:
                return c
                
    response.raise_for_status()
    return ""

def create_note(title, content, parent_dir=None, note_format="web"):
    cstk = get_cstk()
    if not parent_dir:
        parent_dir = get_root_dir()
    headers = build_headers()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    time_mod = __import__("time")
    now = int(time_mod.time())
    file_id = "WEB" + os.urandom(16).hex().upper()
    note_name = title.strip()
    requested_format = note_format
    if note_format == "web":
        base_name = note_name
        root, ext = os.path.splitext(base_name)
        if ext.lower() in [".md", ".note", ".clip"]:
            base_name = root
        note_name = base_name + ".md"
        note_format = "md"
    elif note_format != "web":
        if not os.path.splitext(note_name)[1]:
            note_name = note_name + ".md"
    push_url = f"{BASE_URL}/yws/api/personal/sync"
    push_params = {"method": "push", "keyfrom": "web", "cstk": cstk}
    last_push_resp = None

    def note_exists_in_parent(expected_name):
        try:
            for item in list_files(parent_dir):
                if item.get("id") == file_id:
                    return True
                if item.get("name") == expected_name:
                    return True
        except Exception:
            return False
        return False

    def parse_push_result(response, expected_name):
        try:
            payload = response.json()
        except Exception:
            payload = {"ok": True, "fileId": file_id, "raw": response.text}
        effected = payload.get("effected")
        has_effect = False
        if isinstance(effected, dict):
            has_effect = bool(effected)
        elif isinstance(effected, list):
            has_effect = len(effected) > 0
        else:
            has_effect = effected not in (None, "", 0, False)
        entry = payload.get("entry")
        real_file_id = None
        if isinstance(entry, dict):
            real_file_id = entry.get("id") or entry.get("fileId")
        if not real_file_id:
            real_file_id = payload.get("fileId") or file_id
        payload["fileId"] = real_file_id
        payload.setdefault("name", expected_name)
        payload.setdefault("noteFormat", note_format)
        payload.setdefault("requestedFormat", requested_format)
        payload.setdefault("pushAccepted", True)
        payload.setdefault("pushHasEntry", isinstance(entry, dict) and bool(entry))
        payload.setdefault("pushHasEffect", has_effect)
        return payload

    push_payload = {
        "fileId": file_id,
        "name": note_name,
        "domain": 1,
        "parentId": parent_dir,
        "rootVersion": -1,
        "sessionId": "",
        "dir": False,
        "createTime": now,
        "modifyTime": now,
        "editorVersion": 1602642730000,
        "bodyString": content,
        "transactionTime": now,
        "transactionId": file_id
    }
    push_resp = requests.post(push_url, headers=headers, params=push_params, data=push_payload)
    last_push_resp = push_resp
    if push_resp.status_code == 200:
        push_result = parse_push_result(push_resp, note_name)
        if push_result.get("pushHasEntry") or push_result.get("pushHasEffect") or note_exists_in_parent(note_name):
            return push_result
    url = f"{BASE_URL}/yws/api/personal/file"
    params = {"method": "create", "keyfrom": "web", "dir": parent_dir, "cstk": cstk}
    payload_candidates = [
        {"title": note_name, "content": content, "author": "ClawHub Agent"},
        {"title": note_name, "content": content, "author": "ClawHub Agent", "cstk": cstk},
        {"title": note_name, "content": content, "cstk": cstk},
        {"title": note_name, "content": content}
    ]
    last_response = last_push_resp
    for payload in payload_candidates:
        response = requests.post(url, headers=headers, params=params, data=payload)
        last_response = response
        if response.status_code == 200 and note_exists_in_parent(note_name):
            result = response.json()
            result.setdefault("name", note_name)
            result.setdefault("noteFormat", note_format)
            result.setdefault("requestedFormat", requested_format)
            return result
    print("Error: create_note failed on both push/create endpoints.", file=sys.stderr)
    print(f"dir={parent_dir}", file=sys.stderr)
    if last_push_resp is not None:
        print(f"push_status={last_push_resp.status_code} push_resp={last_push_resp.text}", file=sys.stderr)
    if last_response is not None:
        print(f"create_status={last_response.status_code} create_resp={last_response.text}", file=sys.stderr)
        last_response.raise_for_status()
    raise RuntimeError("Failed to create note: push/create request did not produce a readable or visible note")

def read_all_in_dir(dir_id):
    files = list_files(dir_id)
    results = []
    for f in files:
        if not f.get("is_dir"):
            try:
                content = read_note(f["id"])
                try:
                    parsed_content = json.loads(content) if isinstance(content, str) else None
                except Exception:
                    parsed_content = None
                if isinstance(parsed_content, dict) and parsed_content.get("__skill_parsed__") == "compressed_note_v2":
                    month = f["name"]
                    if "." in month:
                        month = month.rsplit(".", 1)[0]
                    content = {
                        "month": month,
                        "images": parsed_content.get("images", []),
                        "text": parsed_content.get("text", "")
                    }
                results.append({
                    "title": f["name"],
                    "id": f["id"],
                    "content": content
                })
            except Exception as e:
                results.append({
                    "title": f["name"],
                    "id": f["id"],
                    "error": str(e)
                })
    return results

def main():
    parser = argparse.ArgumentParser(description="Youdao Note CLI for ClawHub Skill (Cookie-based)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List files in a directory")
    list_parser.add_argument("--dir", type=str, help="Directory ID (default: root)", default=None)

    search_parser = subparsers.add_parser("search", help="Search notes by keyword")
    search_parser.add_argument("keyword", type=str, help="Keyword to search for")

    read_parser = subparsers.add_parser("read", help="Read a note by file ID")
    read_parser.add_argument("file_id", type=str, help="File ID of the note")

    read_all_parser = subparsers.add_parser("read_all", help="Read all notes in a directory")
    read_all_parser.add_argument("dir_id", type=str, help="Directory ID")

    create_parser = subparsers.add_parser("create", help="Create a new note")
    create_parser.add_argument("title", type=str, help="Note title")
    create_parser.add_argument("content", type=str, help="Note content")
    create_parser.add_argument("--dir", type=str, help="Parent directory ID", default=None)
    create_parser.add_argument("--format", type=str, choices=["web", "md"], default="web", help="Note format")

    args = parser.parse_args()

    try:
        if args.command == "list":
            result = list_files(args.dir)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.command == "search":
            result = search_notes(args.keyword)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.command == "read":
            result = read_note(args.file_id)
            if isinstance(result, (dict, list)):
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(result)
        elif args.command == "read_all":
            result = read_all_in_dir(args.dir_id)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.command == "create":
            result = create_note(args.title, args.content, args.dir, args.format)
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except requests.HTTPError as e:
        print(f"HTTP Error {e.response.status_code}: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error executing {args.command}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
