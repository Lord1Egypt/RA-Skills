#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen


def write_json(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="generic skill entry")
    parser.add_argument("--input", default="")
    parser.add_argument("--output", default="output.json")
    parser.add_argument("--url", default="")
    parser.add_argument("--endpoint", default="")
    parser.add_argument("--payload", default="")
    parser.add_argument("--template", default="")
    parser.add_argument("--data", default="")
    parser.add_argument("--archive", default="")
    parser.add_argument("--target", default="")
    parser.add_argument("--top-k", type=int, default=20)
    args = parser.parse_args()

    result = {"status": "ok"}

    if args.url:
      req = Request(args.url, headers={"User-Agent": "skill-agent/1.0"})
      with urlopen(req, timeout=10) as resp:
        html = resp.read(200000).decode("utf-8", errors="ignore")
      result["fetched_chars"] = len(html)
      result["url"] = args.url
      write_json(args.output, result)
      print(json.dumps(result, ensure_ascii=False))
      return

    if args.endpoint and args.payload:
      payload_text = Path(args.payload).read_text(encoding="utf-8")
      req = Request(args.endpoint, data=payload_text.encode("utf-8"), headers={"Content-Type": "application/json"})
      with urlopen(req, timeout=10) as resp:
        result["http_status"] = resp.status
      write_json(args.output, result)
      print(json.dumps(result, ensure_ascii=False))
      return

    if args.input:
      p = Path(args.input)
      if p.exists():
        text = p.read_text(encoding="utf-8", errors="ignore")
        result["input_chars"] = len(text)
      else:
        result["note"] = "input path not found"

    write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
