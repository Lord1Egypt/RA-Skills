#!/usr/bin/env python3
import argparse
import os
import re
import sys
import uuid
from datetime import datetime
import urllib.request
from html import unescape

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_jobs, save_jobs, OUTPUT_DIR

def slugify(value):
    value = value.lower().strip()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return value.strip('-') or 'page'

def strip_html(html):
    html = re.sub(r'(?is)<script.*?>.*?</script>', ' ', html)
    html = re.sub(r'(?is)<style.*?>.*?</style>', ' ', html)
    html = re.sub(r'(?i)<br\\s*/?>', '\\n', html)
    html = re.sub(r'(?i)</p>', '\\n', html)
    text = re.sub(r'(?s)<.*?>', ' ', html)
    text = unescape(text)
    text = re.sub(r'\r', '', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def main():
    parser = argparse.ArgumentParser(description="Save cleaned output from a public page")
    parser.add_argument("--url", required=True, help="Public URL")
    parser.add_argument("--title", required=True, help="Local title")
    args = parser.parse_args()

    req = urllib.request.Request(
        args.url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; ScraperSkill/1.0)"
        }
    )

    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    text = strip_html(html)

    job_id = f"JOB-{str(uuid.uuid4())[:6].upper()}"
    filename = f"{slugify(args.title)}.txt"
    output_path = os.path.join(OUTPUT_DIR, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    jobs = load_jobs()
    jobs["jobs"][job_id] = {
        "id": job_id,
        "title": args.title,
        "url": args.url,
        "saved_to": output_path,
        "created_at": datetime.now().isoformat()
    }
    save_jobs(jobs)

    print(f"✓ Saved {job_id}")
    print(f"  {output_path}")

if __name__ == "__main__":
    main()
