#!/usr/bin/env python3
"""
WiseOCR  CLI - Convert PDF / Image to Markdown (powered by WiseDiag)

Usage:
    export WISEDIAG_API_KEY=your_api_key
    python3 wiseocr.py -i report.pdf
    python3 wiseocr.py -i scan.png
    python3 wiseocr.py -i a.pdf --dpi 300

Get API key: https://console.wisediag.com/apiKeyManage
"""

import argparse
import os
import sys
import time
import threading
from pathlib import Path

import requests
from pypdf import PdfReader


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_SERVICE_URL = "https://openapi.wisediag.com"
DEFAULT_DPI         = 200
MAX_RETRIES         = 3
RETRY_DELAY         = 5       # seconds between retries
MAX_FILE_SIZE_MB    = 50
MAX_PAGES           = 200
REQUEST_TIMEOUT     = 600     # seconds

IMAGE_EXTENSIONS = {
    "jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff", "tif",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mime(filename: str) -> str:
    ext = Path(filename).suffix.lstrip(".").lower()
    if ext == "pdf":
        return "application/pdf"
    if ext in ("jpg", "jpeg"):
        return "image/jpeg"
    return f"image/{ext}"


def _get_api_key() -> str:
    key = os.environ.get("WISEDIAG_API_KEY", "")
    if not key:
        print("""
[!] Error: WISEDIAG_API_KEY is not set.

    export WISEDIAG_API_KEY=your_api_key

Get a key at: https://s.wisediag.com/xsu9x0jq
""")
        raise SystemExit(1)
    return key


class ProgressIndicator:
    """Show elapsed time while waiting for OCR processing."""

    def __init__(self):
        self._stop   = threading.Event()
        self._thread = None

    def start(self):
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join()
        sys.stdout.write("\r" + " " * 70 + "\r")
        sys.stdout.flush()

    def _run(self):
        t0 = time.time()
        while not self._stop.is_set():
            elapsed = int(time.time() - t0)
            m, s = divmod(elapsed, 60)
            sys.stdout.write(f"\r[*] OCR processing... {m:02d}:{s:02d} elapsed")
            sys.stdout.flush()
            self._stop.wait(1)


# ---------------------------------------------------------------------------
# Upload with retry
# ---------------------------------------------------------------------------

def _upload_with_retry(
    endpoint: str,
    file_path: Path,
    headers: dict,
    params: dict,
    max_retries: int = MAX_RETRIES,
):
    """Upload a single file to /v1/ocr/pdf with automatic retry."""
    last_error = None

    for attempt in range(1, max_retries + 1):
        fh = None
        try:
            fh = open(file_path, "rb")
            multipart = [("file", (file_path.name, fh, _mime(file_path.name)))]

            resp = requests.post(
                endpoint,
                files=multipart,
                params=params,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )

            fh.close()
            fh = None

            if resp.status_code == 401:
                print("\n[!] Authentication failed. Check your API key.")
                return None

            if resp.status_code == 504:
                print("\n[!] Server timed out (504). Try a lower --dpi value.")
                return None

            if resp.status_code == 200:
                return resp

            last_error = f"HTTP {resp.status_code}: {resp.text[:200]}"

        except requests.Timeout:
            last_error = f"Timed out after {REQUEST_TIMEOUT}s"

        except requests.ConnectionError:
            last_error = "Connection refused"

        except Exception as e:
            last_error = str(e)

        finally:
            if fh:
                try:
                    fh.close()
                except Exception:
                    pass

        if attempt < max_retries:
            print(f"\n[!] Attempt {attempt}/{max_retries} failed: {last_error}")
            print(f"    Retrying in {RETRY_DELAY}s ...")
            time.sleep(RETRY_DELAY)
        else:
            print(f"\n[!] All {max_retries} attempts failed. Last error: {last_error}")

    return None


# ---------------------------------------------------------------------------
# Save result
# ---------------------------------------------------------------------------

def _save_result(data: dict, output_dir: Path, stem: str) -> None:
    """Save OcrResult to a markdown file."""
    markdown    = data.get("markdown", "")
    total_pages = data.get("total_pages", 1)
    elapsed     = data.get("elapsed_seconds", 0)
    usage       = data.get("usage") or {}

    print(f"[*] Total pages: {total_pages}")
    print(f"[*] Processing time: {elapsed:.1f}s")
    if usage:
        print(f"[*] Usage: prompt_tokens={usage.get('prompt_tokens')}, "
              f"completion_tokens={usage.get('completion_tokens')}, "
              f"ocr_pic_size={usage.get('ocr_pic_size')}, "
              f"total_tokens={usage.get('total_tokens')}")

    out_path = output_dir / f"{stem}.md"
    out_path.write_text(markdown, encoding="utf-8")
    print(f"[+] Markdown saved: {out_path}")


# ---------------------------------------------------------------------------
# Main processing
# ---------------------------------------------------------------------------

def process_file(
    input_path: str,
    output_dir: str | None = None,
    dpi:        int        = DEFAULT_DPI,
    name:       str | None = None,
) -> bool:
    """Process a single PDF or image file via the WiseOCR API."""
    p = Path(input_path)

    # Validate
    if not p.exists():
        print(f"[!] File not found: {p}")
        return False
    ext = p.suffix.lstrip(".").lower()
    if ext != "pdf" and ext not in IMAGE_EXTENSIONS:
        print(f"[!] Unsupported format: {p}  (supported: pdf, {', '.join(sorted(IMAGE_EXTENSIONS))})")
        return False
    size_mb = p.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        print(f"[!] File too large: {p.name} ({size_mb:.1f} MB, limit {MAX_FILE_SIZE_MB} MB)")
        return False
    if ext == "pdf":
        try:
            page_count = len(PdfReader(str(p)).pages)
        except Exception as e:
            print(f"[!] Failed to read PDF: {e}")
            return False
        if page_count > MAX_PAGES:
            print(f"[!] Too many pages: {p.name} ({page_count} pages, limit {MAX_PAGES})")
            return False

    if output_dir is None:
        out_dir = Path.home() / ".openclaw" / "workspace" / "WiseOCR"
    else:
        out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    key      = _get_api_key()
    headers  = {"Authorization": f"Bearer {key}"}
    params   = {"dpi": dpi}
    endpoint = f"{DEFAULT_SERVICE_URL}/v1/ocr/pdf"

    print(f"[*] Processing: {p.name}  (DPI={dpi})")

    progress = ProgressIndicator()
    progress.start()
    resp = _upload_with_retry(endpoint, p, headers, params)
    progress.stop()

    if resp is None:
        print(f"[!] Failed: {p.name}")
        return False

    stem = name if name else p.stem
    _save_result(resp.json(), out_dir, stem)
    return True


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="WiseOCR  CLI — Convert a PDF or Image to Markdown (powered by WiseDiag)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 wiseocr.py -i report.pdf
  python3 wiseocr.py -i scan.png
  python3 wiseocr.py -i a.pdf --dpi 300
        """,
    )
    parser.add_argument(
        "-i", "--input", required=True, metavar="FILE",
        help="Input file: PDF or image (jpg/png/webp/gif/bmp/tiff) — single file only",
    )
    parser.add_argument("-o", "--output", help="Output directory (default: ~/.openclaw/workspace/WiseOCR)")
    parser.add_argument("-n", "--name",   help="Output filename stem (recommended when input file is renamed/copied)")
    parser.add_argument("--dpi", type=int, default=DEFAULT_DPI, help=f"PDF render DPI (default: {DEFAULT_DPI})")
    args = parser.parse_args()

    success = process_file(
        input_path = args.input,
        output_dir = args.output,
        dpi        = args.dpi,
        name       = args.name,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
