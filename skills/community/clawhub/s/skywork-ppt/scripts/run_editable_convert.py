#!/usr/bin/env python3
"""
Call the editable PPTX conversion SSE API, output progress to stdout, and save the generated .pptx locally.
"""
import argparse
import datetime
import json
import os
import sys
import urllib.error
import urllib.request
import uuid

from constant import SKYWORK_GATEWAY_URL
from skywork_auth import get_skywork_api_key


def write_log(log_file: str, line: str):
    try:
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_str = f"{time_str} {line.rstrip()}\n"
        print(log_str, flush=True)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_str)
            f.flush()
    except Exception:
        pass


def parse_sse_stream(resp):
    cur_event = None
    cur_data = None
    for line in resp:
        line = line.decode("utf-8", errors="replace").rstrip("\r\n")
        if line == "":
            if cur_event is not None and cur_data is not None:
                try:
                    raw = json.loads(cur_data) if cur_data else {}
                except json.JSONDecodeError:
                    raw = {}
                data = raw.get("data", raw) if isinstance(raw, dict) else raw
                if isinstance(data, str):
                    try:
                        data = json.loads(data)
                    except json.JSONDecodeError:
                        data = {}
                if not isinstance(data, dict):
                    data = {}
                yield cur_event, data
            cur_event = None
            cur_data = None
            continue
        if line.startswith("event:"):
            cur_event = line[6:].strip()
        elif line.startswith("data:"):
            cur_data = line[5:].strip()
    if cur_event is not None and cur_data is not None:
        try:
            raw = json.loads(cur_data) if cur_data else {}
        except json.JSONDecodeError:
            raw = {}
        data = raw.get("data", raw) if isinstance(raw, dict) else raw
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                data = {}
        if not isinstance(data, dict):
            data = {}
        yield cur_event, data


def phase_to_message(phase: str, data: dict) -> str:
    if phase == "ping":
        progress = data.get("progress", "")
        stage = data.get("stage", "")
        return f"Now {progress}% was done, and is working on {stage}" if stage else f"{progress}%"
    if phase == "get_screenshots":
        status = data.get("status", "")
        if status == "start":
            file_type = data.get("file_type", "")
            return f"Capturing screenshots from {file_type or 'source file'}..."
        if status == "done":
            slide_count = data.get("slide_count", "")
            return f"Screenshots captured, {slide_count} pages total."
        return ""
    if phase == "upload_screenshots":
        status = data.get("status", "")
        if status == "start":
            return "Uploading screenshot images..."
        if status == "done":
            page_count = data.get("page_count", "")
            return f"Screenshot upload complete, {page_count} pages total."
        return ""
    if phase == "screenshot_uploaded":
        page_num = data.get("page_num", "")
        return f"Screenshot {page_num} uploaded."
    if phase == "build_nano_html":
        status = data.get("status", "")
        if status == "start":
            return "Building nano HTML..."
        if status == "done":
            page_count = data.get("page_count", "")
            return f"Nano HTML built, {page_count} pages total."
        return ""
    if phase == "nano_html_page":
        page_num = data.get("page_num", "")
        return f"Nano HTML ready for page {page_num}."
    if phase == "convert_html":
        status = data.get("status", "")
        if status == "start":
            return "Converting HTML..."
        if status == "done":
            page_count = data.get("page_count", "")
            return f"HTML conversion complete, {page_count} pages total."
        return ""
    if phase == "convert_batch":
        batch_index = data.get("batch_index", "")
        batch_count = data.get("batch_count", "")
        return f"Converted batch {batch_index}/{batch_count}."
    if phase == "export":
        status = data.get("status", "")
        if status == "start":
            return "Exporting editable PPTX..."
        if status == "done":
            return "Export complete."
        return ""
    if phase == "done":
        return "Conversion complete, saving file..."
    if phase:
        return f"[{phase}]"
    return ""


def main():
    parser = argparse.ArgumentParser(description="Convert a PPTX or PDF file to an editable PPTX")
    parser.add_argument("--file-url", required=True, dest="file_url", help="OSS URL of the source pptx/pdf file")
    parser.add_argument("--file-type", default="", dest="file_type", help="Optional file type override: pptx or pdf")
    parser.add_argument("--title", default="", help="Optional output file title used by the backend export")
    parser.add_argument("-o", "--output", default="output_editable.pptx", help="Output .pptx path")
    parser.add_argument("--session_id", default=str(uuid.uuid4()), help="session_id used for the request")
    parser.add_argument("--log_path", default="", dest="log_path", help="A file path to save the progress log")
    args = parser.parse_args()

    session_id = args.session_id.replace("-", "_")
    log_file = f"/tmp/ppt_editable_{session_id}.log" if args.log_path == "" else args.log_path
    open(log_file, "w").close()
    print(f"[LOG-File]: {log_file}", flush=True)

    print(f"[PID] {os.getpid()}", flush=True)
    print(f"[START] mode=editable_convert session={session_id} \nIS about to take 5-10minutes, please wait and check the process log every 5 seconds!", flush=True)
    write_log(log_file, f"[PID] {os.getpid()}")
    write_log(log_file, f"[START] mode=editable_convert session={session_id} \nIS about to take 5-10minutes, please wait and check the process log every 5 seconds!")

    payload = {"file_url": args.file_url}
    if args.file_type:
        payload["file_type"] = args.file_type
    if args.title:
        payload["title"] = args.title

    api_key = get_skywork_api_key()
    if not api_key:
        print("[error] SKYWORK_API_KEY is required", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "Session-Id": session_id,
        "Authorization": f"Bearer {api_key}",
    }
    req = urllib.request.Request(
        f"{SKYWORK_GATEWAY_URL}/convert_file_to_editable_pptx",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers=headers,
    )

    out_abs = os.path.abspath(args.output)
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            for event_type, data in parse_sse_stream(resp):
                if not isinstance(data, dict):
                    data = {}
                if event_type == "phase":
                    phase = data.get("phase", "")
                    msg = phase_to_message(phase, data)
                    if msg:
                        tag = "[PROGRESS]" if phase == "ping" else "[PHASE]"
                        write_log(log_file, f"{tag} {msg}")
                elif event_type == "completionEvent":
                    if data.get("phase", "") == "done":
                        download_url = data.get("download_url", "")
                        slide_count = data.get("slide_count", "")
                        output_id = data.get("output_id", "")
                        if slide_count != "":
                            write_log(log_file, f"[PHASE] Editable PPTX contains {slide_count} slides.")
                        if output_id:
                            write_log(log_file, f"[PHASE] output_id={output_id}")
                        if not download_url:
                            write_log(log_file, "[ERROR] No download_url in completionEvent")
                            sys.exit(1)
                        try:
                            req2 = urllib.request.Request(download_url, method="GET")
                            with urllib.request.urlopen(req2, timeout=120) as r:
                                with open(out_abs, "wb") as f:
                                    f.write(r.read())
                            write_log(log_file, f"[DONE] saved={out_abs} download_url={download_url}")
                        except Exception as e:
                            write_log(log_file, f"[ERROR] Download failed: {e}")
                            sys.exit(1)
                elif event_type == "error":
                    err_msg = data.get("message", str(data))
                    write_log(log_file, f"[ERROR] {err_msg}")
                    sys.exit(1)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        write_log(log_file, f"[ERROR] HTTP {e.code}: {body}")
        sys.exit(1)
    except Exception as e:
        write_log(log_file, f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
