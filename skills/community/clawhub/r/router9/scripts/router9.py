#!/usr/bin/env python3
"""Router9 Skills CLI — ASR, TTS, Image Description, OCR, Image Generation, and Storage."""

import argparse, json, os, sys, urllib.request, urllib.error
from pathlib import Path

BASE_URL = "https://api.router9.com"
API_KEY = os.environ.get("ROUTER9_API_KEY", "")


def _headers(content_type=None):
    h = {"Authorization": f"Bearer {API_KEY}"}
    if content_type:
        h["Content-Type"] = content_type
    return h


def _multipart(fields: dict, files: dict):
    """Build multipart/form-data body using only stdlib."""
    import uuid
    boundary = uuid.uuid4().hex
    lines = []
    for k, v in fields.items():
        lines += [
            f"--{boundary}".encode(),
            f'Content-Disposition: form-data; name="{k}"'.encode(),
            b"", v.encode(),
        ]
    for k, (filename, data, mime) in files.items():
        lines += [
            f"--{boundary}".encode(),
            f'Content-Disposition: form-data; name="{k}"; filename="{filename}"'.encode(),
            f"Content-Type: {mime}".encode(),
            b"", data,
        ]
    lines += [f"--{boundary}--".encode(), b""]
    body = b"\r\n".join(lines)
    content_type = f"multipart/form-data; boundary={boundary}"
    return body, content_type


def _post_json(path, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{BASE_URL}{path}", data=data, headers=_headers("application/json")
    )
    with urllib.request.urlopen(req) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def _post_multipart(path, fields=None, files=None):
    body, ct = _multipart(fields or {}, files or {})
    req = urllib.request.Request(
        f"{BASE_URL}{path}", data=body, headers={**_headers(), "Content-Type": ct}
    )
    with urllib.request.urlopen(req) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def _get(path):
    req = urllib.request.Request(f"{BASE_URL}{path}", headers=_headers())
    with urllib.request.urlopen(req) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def _delete(path):
    req = urllib.request.Request(f"{BASE_URL}{path}", method="DELETE", headers=_headers())
    with urllib.request.urlopen(req) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def _image_mime(filepath):
    return {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
            "webp": "image/webp", "gif": "image/gif"}.get(
        filepath.suffix.lstrip(".").lower(), "application/octet-stream"
    )


def cmd_transcribe(args):
    audio = Path(args.file).read_bytes()
    mime = {"mp3": "audio/mpeg", "wav": "audio/wav", "m4a": "audio/m4a",
            "webm": "audio/webm", "mp4": "video/mp4"}.get(
        Path(args.file).suffix.lstrip("."), "application/octet-stream"
    )
    fields = {}
    if args.language:
        fields["language"] = args.language
    body, _ = _post_multipart(
        "/v1/audio/transcribe", fields, {"file": (Path(args.file).name, audio, mime)}
    )
    print(body.decode())


def cmd_tts(args):
    payload = {"input": args.text, "voice": args.voice, "format": args.format}
    body, _ = _post_json("/v1/audio/synthesize", payload)
    Path(args.output).write_bytes(body)
    print(json.dumps({"status": "ok", "file": args.output}))


def cmd_describe(args):
    filepath = Path(args.file)
    import base64
    encoded = base64.b64encode(filepath.read_bytes()).decode()
    payload = {"mediaBase64": encoded}
    if args.prompt:
        payload["prompt"] = args.prompt
    body, _ = _post_json("/v1/vision/describe", payload)
    print(body.decode())


def cmd_ocr(args):
    filepath = Path(args.file)
    image = filepath.read_bytes()
    import base64
    encoded = base64.b64encode(image).decode()
    payload = {"mediaBase64": encoded}
    body, _ = _post_json("/v1/vision/ocr", payload)
    print(body.decode())


def cmd_generate(args):
    import base64
    payload = {"prompt": args.prompt}
    body, _ = _post_json("/v1/image/generations", payload)
    result = json.loads(body)
    for i, item in enumerate(result.get("data", [])):
        suffix = "-" + str(i + 1) if len(result.get("data", [])) > 1 else ""
        out = Path(args.output)
        dest = out.with_stem(out.stem + suffix) if suffix else out
        if "b64_json" in item:
            dest.write_bytes(base64.b64decode(item["b64_json"]))
            print(json.dumps({"file": str(dest)}))
        elif "content" in item:
            print(json.dumps({"content": item["content"]}))


def _guess_mime(path):
    ext = path.suffix.lstrip(".").lower()
    return {
        "pdf": "application/pdf", "txt": "text/plain", "json": "application/json",
        "csv": "text/csv", "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "gif": "image/gif", "webp": "image/webp", "mp3": "audio/mpeg", "wav": "audio/wav",
        "mp4": "video/mp4", "zip": "application/zip",
    }.get(ext, "application/octet-stream")


def cmd_upload(args):
    filepath = Path(args.file)
    if not filepath.exists():
        print(json.dumps({"error": "File not found", "file": args.file}), file=sys.stderr)
        sys.exit(1)

    size = filepath.stat().st_size
    mime = _guess_mime(filepath)

    # Step 1: Request presigned upload URL
    payload = {"filename": filepath.name, "contentType": mime, "sizeBytes": size}
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/v1/storage/presigned-upload",
        data=data,
        headers=_headers("application/json"),
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    upload_url = result["data"]["uploadUrl"]
    file_id = result["data"]["id"]

    # Step 2: PUT file directly to S3
    file_data = filepath.read_bytes()
    put_req = urllib.request.Request(upload_url, data=file_data, method="PUT")
    put_req.add_header("Content-Type", mime)
    try:
        with urllib.request.urlopen(put_req) as _resp:
            pass
    except urllib.error.HTTPError as e:
        # Clean up orphan DB record
        try:
            del_req = urllib.request.Request(
                f"{BASE_URL}/v1/storage/files/{file_id}",
                method="DELETE", headers=_headers(),
            )
            urllib.request.urlopen(del_req)
        except Exception:
            pass
        print(json.dumps({"error": e.code, "message": "Upload to storage failed"}),
              file=sys.stderr)
        sys.exit(1)

    print(json.dumps({
        "id": file_id,
        "filename": result["data"]["filename"],
        "sizeBytes": result["data"]["sizeBytes"],
    }))


def cmd_download(args):
    # Step 1: Get presigned download URL
    req = urllib.request.Request(
        f"{BASE_URL}/v1/storage/files/{args.file_id}/url",
        headers=_headers(),
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())

    download_url = result["data"]["url"]
    filename = result["data"].get("filename", "download")

    # Step 2: Download from S3
    output = args.output or filename
    urllib.request.urlretrieve(download_url, output)
    print(json.dumps({"status": "ok", "file": output}))


def cmd_list(args):
    params = f"?page={args.page}&limit={args.limit}"
    body, _ = _get(f"/v1/storage/files{params}")
    print(body.decode())


def cmd_delete(args):
    body, _ = _delete(f"/v1/storage/files/{args.file_id}")
    print(body.decode())


def cmd_usage(args):
    body, _ = _get("/v1/storage/quota")
    print(body.decode())


def main():
    if not API_KEY:
        print("Error: ROUTER9_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    p = argparse.ArgumentParser(prog="router9", description="Router9 Skills CLI")
    sub = p.add_subparsers(dest="command", required=True)

    t = sub.add_parser("transcribe", help="Transcribe audio to text")
    t.add_argument("file", help="Audio file path")
    t.add_argument("--language", help="ISO 639-1 language code")

    s = sub.add_parser("tts", help="Text-to-speech")
    s.add_argument("text", help="Text to synthesize")
    s.add_argument("-o", "--output", required=True, help="Output file path")
    s.add_argument("--voice", default="alloy", help="Voice ID")
    s.add_argument("--format", default="mp3", choices=["mp3", "wav", "opus"])

    d = sub.add_parser("describe", help="Describe an image")
    d.add_argument("file", help="Image file path")
    d.add_argument("--prompt", help="Specific question about the image")

    o = sub.add_parser("ocr", help="Extract text from an image")
    o.add_argument("file", help="Image file path")

    g = sub.add_parser("generate", help="Generate image from prompt")
    g.add_argument("prompt", help="Text description")
    g.add_argument("-o", "--output", required=True, help="Output file path")

    u = sub.add_parser("upload", help="Upload a file to agent storage")
    u.add_argument("file", help="Local file path to upload")

    dl = sub.add_parser("download", help="Download a file from agent storage")
    dl.add_argument("file_id", help="File ID to download")
    dl.add_argument("-o", "--output", help="Output file path (default: original filename)")

    ls = sub.add_parser("list", help="List files in agent storage")
    ls.add_argument("--page", type=int, default=1, help="Page number")
    ls.add_argument("--limit", type=int, default=50, help="Items per page")

    rm = sub.add_parser("delete", help="Delete a file from agent storage")
    rm.add_argument("file_id", help="File ID to delete")

    sub.add_parser("usage", help="Check storage usage and quota")

    args = p.parse_args()
    try:
        {
            "transcribe": cmd_transcribe, "tts": cmd_tts,
            "describe": cmd_describe, "ocr": cmd_ocr, "generate": cmd_generate,
            "upload": cmd_upload, "download": cmd_download,
            "list": cmd_list, "delete": cmd_delete, "usage": cmd_usage,
        }[args.command](args)
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": e.code, "message": e.read().decode()}),
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
