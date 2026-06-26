#!/usr/bin/env python3
import json, os, re, subprocess, sys, urllib.parse, datetime
from pathlib import Path

BITABLE_APP_TOKEN = "KMuEbR5b5aLXFosyxGlc7kTenpb"
BITABLE_TABLE_ID = "tblz1kx1SjpO9QnV"
BASE_DIR = os.path.expanduser("~/Downloads/yt-dlp")
YTFETCH = "/home/jianhao/.openclaw/workspace/scripts/ytfetch.sh"


def fail(msg, code=1):
    print(json.dumps({"ok": False, "error": msg}, ensure_ascii=False))
    sys.exit(code)


def run(cmd):
    p = subprocess.run(cmd, text=True, capture_output=True)
    return p.returncode, p.stdout, p.stderr


def valid_url(url):
    try:
        u = urllib.parse.urlparse(url)
        return u.scheme in {"http", "https"} and bool(u.netloc)
    except Exception:
        return False


def slug_site(extractor):
    if not extractor:
        return "video"
    e = extractor.lower()
    if "youtube" in e:
        return "youtube"
    return re.sub(r"[^a-z0-9._-]+", "-", e).strip("-") or "video"


def dedupe_keep_order(items):
    seen = set()
    out = []
    for x in items or []:
        if not x:
            continue
        s = str(x).strip()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def first(*vals):
    for v in vals:
        if v not in (None, "", "NA"):
            return v
    return ""


def safe_name(s):
    s = re.sub(r"[\\/:*?\"<>|]", "_", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:180] if s else "video"


def parse_yyyymmdd_to_ms(v):
    if not v or not re.fullmatch(r"\d{8}", str(v)):
        return None
    dt = datetime.datetime(int(v[:4]), int(v[4:6]), int(v[6:8]), 0, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=8)))
    return int(dt.timestamp() * 1000)


def probe_media(path):
    rc, out, err = run([
        "ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,width,height,r_frame_rate,bit_rate,codec_name:format=bit_rate",
        "-of", "json", path,
    ])
    if rc != 0 or not out.strip():
        return {}
    try:
        data = json.loads(out)
    except Exception:
        return {}
    streams = data.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), {})
    fmt = data.get("format", {})
    width = v.get("width")
    height = v.get("height")
    fps = None
    raw = v.get("r_frame_rate")
    if raw and raw != "0/0" and "/" in raw:
        try:
            a, b = raw.split("/", 1)
            a = float(a); b = float(b)
            if b:
                fps = round(a / b, 3)
        except Exception:
            fps = None
    bitrate = v.get("bit_rate") or fmt.get("bit_rate")
    kbps = round(int(bitrate) / 1000, 3) if bitrate else None
    return {
        "resolution": f"{width}x{height}" if width and height else "",
        "fps": fps,
        "codec": first(v.get("codec_name")),
        "kbps": kbps,
    }


def parse_meta(url):
    rc, out, err = run(["yt-dlp", "--dump-single-json", "--no-warnings", url])
    if rc != 0 or not out.strip():
        fail("不是可下载视频，或 yt-dlp 无法提取元数据")
    try:
        data = json.loads(out)
    except Exception:
        fail("视频元数据解析失败")
    vid = first(data.get("id"))
    if not vid:
        fail("未提取到视频ID")
    site = slug_site(first(data.get("extractor_key"), data.get("extractor")))
    key = f"{site}-{vid}"
    title = first(data.get("title"))
    handle = first(data.get("channel_handle"), data.get("uploader_id"))
    uploader_url = first(data.get("uploader_url"), data.get("channel_url"))
    display = first(data.get("channel"), data.get("uploader"), handle)
    tags = dedupe_keep_order(data.get("tags") or [])
    if handle and not str(handle).startswith("@") and site == "youtube":
        handle = "@" + str(handle)
    folder = handle or display or site
    final_name = f"{safe_name(title)} [{vid}].mkv"
    return {
        "site": site,
        "video_id": vid,
        "video_key": key,
        "url": url,
        "title": title,
        "uploader": display,
        "uploader_handle": handle,
        "uploader_url": uploader_url,
        "tags_text": " ".join(tags),
        "upload_date": first(data.get("upload_date")),
        "description": first(data.get("description")),
        "duration": data.get("duration") or 0,
        "thumbnail": first(data.get("thumbnail")),
        "folder": folder,
        "file_name": final_name,
    }


def find_existing(meta):
    target_dir = os.path.join(BASE_DIR, meta["folder"])
    if not os.path.isdir(target_dir):
        return None, None
    vid = meta["video_id"]
    candidates = []
    for p in Path(target_dir).iterdir():
        if not p.is_file():
            continue
        if vid in p.name and not re.search(r"\.(info\.json|jpg|jpeg|png|webp|vtt|srt|ass|lrc)$", p.name, re.I):
            candidates.append(str(p))
    info_json = None
    for p in Path(target_dir).iterdir():
        if p.is_file() and vid in p.name and p.name.endswith(".info.json"):
            info_json = str(p)
            break
    return (candidates[0] if candidates else None), info_json


def do_download(url):
    rc, out, err = run([YTFETCH, url])
    text = (out or "") + "\n" + (err or "")
    pairs = {}
    for line in text.splitlines():
        if "=" in line and re.match(r"^[A-Z0-9_]+=", line):
            k, v = line.split("=", 1)
            pairs[k.strip()] = v.strip()
    existing = pairs.get("EXISTING_FILE")
    updated = pairs.get("UPDATED_FILE")
    target_dir = pairs.get("TARGET_DIR")
    vid = pairs.get("VIDEO_ID")
    chosen = updated or existing
    if not chosen and target_dir and vid:
        chosen, _ = find_existing({"folder": os.path.basename(target_dir), "video_id": vid})
    if rc not in (0, 11, 12) and not chosen:
        fail("下载失败")
    info_json = None
    if target_dir and vid:
        _, info_json = find_existing({"folder": os.path.basename(target_dir), "video_id": vid})
    return {"file": chosen, "info_json": info_json, "raw": text, "status_code": rc}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail("用法: run_video_archive.py <url>")
    url = sys.argv[1].strip()
    if not valid_url(url):
        fail("不是合法 URL")

    meta = parse_meta(url)
    existing_file, existing_json = find_existing(meta)
    result = do_download(url) if not existing_file else {"file": existing_file, "info_json": existing_json, "raw": "", "status_code": 0}
    file_path = result.get("file") or existing_file
    info_json = result.get("info_json") or existing_json
    if not file_path:
        fail("下载后未定位到本地文件")

    stat = os.stat(file_path)
    media = probe_media(file_path)
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    now_ms = int(now.timestamp() * 1000)

    fields = {
        "视频主键": meta["video_key"],
        "视频标题": meta["title"],
        "视频唯一ID": meta["video_key"],
        "上传者": meta["uploader"],
        "上传者@handle": meta["uploader_handle"],
        "上传者主页URL": {"text": meta["uploader_url"], "link": meta["uploader_url"]} if meta["uploader_url"] else None,
        "时长(秒)": float(meta["duration"]) if meta["duration"] else None,
        "文件大小(字节)": float(stat.st_size),
        "分辨率": media.get("resolution") or None,
        "帧率(FPS)": media.get("fps"),
        "视频编码": media.get("codec") or None,
        "总码率(kbps)": media.get("kbps"),
        "来源": meta["site"],
        "标签": meta["tags_text"] or None,
        "简介描述": meta["description"] or None,
        "下载的URL": {"text": meta["url"], "link": meta["url"]},
        "下载时间": now_ms,
        "下载地址": file_path,
        "备注": None,
    }
    up_ms = parse_yyyymmdd_to_ms(meta.get("upload_date"))
    if up_ms:
        fields["上传日期"] = up_ms
    fields = {k: v for k, v in fields.items() if v is not None}

    output = {
        "ok": True,
        "meta": meta,
        "file_path": file_path,
        "file_size": stat.st_size,
        "info_json": info_json,
        "bitable": {"app_token": BITABLE_APP_TOKEN, "table_id": BITABLE_TABLE_ID},
        "record_fields": fields,
    }
    print(json.dumps(output, ensure_ascii=False))
