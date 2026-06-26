#!/usr/bin/env python3
import argparse
import binascii
import hashlib
import json
import os
import re
import struct
import sys
import zlib

ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")

FULL_BLACK = set("█■▓▒▉▊▋▍▎▏")
FULL_WHITE = set(" 　░□")
UPPER_HALF = "▀"
LOWER_HALF = "▄"

def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)

def normalize_line(line: str) -> str:
    return line.rstrip("\r\n")

def qr_char_score(line: str) -> float:
    s = normalize_line(line)
    if not s.strip():
        return 0.0
    good = 0
    for ch in s:
        if ch in FULL_BLACK or ch in FULL_WHITE or ch == UPPER_HALF or ch == LOWER_HALF:
            good += 1
    return good / max(len(s), 1)

def find_all_qr_blocks(lines):
    blocks = []
    i = 0
    n = len(lines)

    while i < n:
      score = qr_char_score(lines[i])
      if score >= 0.35 and len(normalize_line(lines[i]).strip()) >= 8:
          start = i
          block = []
          while i < n and qr_char_score(lines[i]) >= 0.22:
              block.append(normalize_line(lines[i]))
              i += 1

          width = max((len(x) for x in block), default=0)
          height = len(block)
          if width >= 8 and height >= 8:
              block_text = "\n".join(block)
              blocks.append(
                  {
                      "start_idx": start,
                      "end_idx": i - 1,
                      "start_line": start + 1,
                      "end_line": i,
                      "width": width,
                      "height": height,
                      "area": width * height,
                      "hash": hashlib.sha256(block_text.encode("utf-8")).hexdigest(),
                      "block": block,
                  }
              )
      else:
          i += 1

    return blocks

def choose_latest_block(blocks):
    if not blocks:
        return None
    return blocks[-1]

def block_to_matrix(block):
    width = max(len(row) for row in block)
    matrix = []

    for row in block:
        row = row.ljust(width, " ")
        top = []
        bottom = []

        for ch in row:
            if ch in FULL_WHITE:
                top.append(0)
                bottom.append(0)
            elif ch == UPPER_HALF:
                top.append(1)
                bottom.append(0)
            elif ch == LOWER_HALF:
                top.append(0)
                bottom.append(1)
            elif ch in FULL_BLACK:
                top.append(1)
                bottom.append(1)
            else:
                top.append(0)
                bottom.append(0)

        matrix.append(top)
        matrix.append(bottom)

    quiet = 4
    padded_w = len(matrix[0]) + quiet * 2
    padded = []

    for _ in range(quiet):
        padded.append([0] * padded_w)

    for row in matrix:
        padded.append(([0] * quiet) + row + ([0] * quiet))

    for _ in range(quiet):
        padded.append([0] * padded_w)

    return padded

def write_png_bw(matrix, out_path, scale=12):
    h = len(matrix)
    w = len(matrix[0])
    out_w = w * scale
    out_h = h * scale

    raw_rows = []
    for row in matrix:
        expanded = bytearray()
        for cell in row:
            pixel = 0 if cell else 255
            expanded.extend([pixel] * scale)
        expanded = bytes(expanded)
        for _ in range(scale):
            raw_rows.append(b"\x00" + expanded)

    raw = b"".join(raw_rows)
    compressed = zlib.compress(raw, 9)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + tag
            + data
            + struct.pack(">I", binascii.crc32(tag + data) & 0xFFFFFFFF)
        )

    png = bytearray()
    png.extend(b"\x89PNG\r\n\x1a\n")
    png.extend(chunk(b"IHDR", struct.pack(">IIBBBBB", out_w, out_h, 8, 0, 0, 0, 0)))
    png.extend(chunk(b"IDAT", compressed))
    png.extend(chunk(b"IEND", b""))

    with open(out_path, "wb") as f:
        f.write(png)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="input log path")
    parser.add_argument("--png", required=True, help="output png path")
    parser.add_argument("--txt", required=True, help="output txt path")
    parser.add_argument("--json", required=True, help="output json path")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print("input log does not exist", file=sys.stderr)
        sys.exit(2)

    with open(args.input, "r", encoding="utf-8", errors="ignore") as f:
        raw = f.read()

    clean = strip_ansi(raw)
    lines = clean.splitlines(True)

    blocks = find_all_qr_blocks(lines)
    selected = choose_latest_block(blocks)

    if not selected:
        print("qr block not found", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(args.png), exist_ok=True)

    with open(args.txt, "w", encoding="utf-8") as f:
        f.write("\n".join(selected["block"]) + "\n")

    matrix = block_to_matrix(selected["block"])
    write_png_bw(matrix, args.png, scale=12)

    payload = {
        "ok": True,
        "qr_found": True,
        "blocks_found": len(blocks),
        "selected": "latest",
        "selected_start_line": selected["start_line"],
        "selected_end_line": selected["end_line"],
        "selected_hash": selected["hash"],
        "png_path": args.png,
        "txt_path": args.txt,
        "rows": len(matrix),
        "cols": len(matrix[0]),
    }

    with open(args.json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)

    print(json.dumps(payload, ensure_ascii=False))

if __name__ == "__main__":
    main()
