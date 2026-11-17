#!/usr/bin/env python3
"""Read-only PNG/ZIP delivery validation. Requires Pillow. No UV validation."""
import argparse
import hashlib
import io
import json
import re
import struct
import sys
import zipfile
import zlib
from pathlib import Path
from PIL import Image


def check_png(data, name, width, height, limit):
    errors = []
    if len(data) > limit:
        errors.append('file exceeds byte limit')
    stem = Path(name).stem
    if len(stem) > 30 or not re.fullmatch(r'[A-Za-z0-9 _-]+', stem):
        errors.append('filename violates configured conservative naming policy')
    size = None
    try:
        if data[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError('not PNG')
        pos, ended = 8, False
        while pos < len(data):
            if pos + 12 > len(data):
                raise ValueError('truncated chunk header')
            n = struct.unpack('>I', data[pos:pos + 4])[0]
            kind = data[pos + 4:pos + 8]
            end = pos + 12 + n
            if end > len(data):
                raise ValueError('truncated chunk data')
            expected = struct.unpack('>I', data[end - 4:end])[0]
            if zlib.crc32(data[pos + 4:end - 4]) & 0xffffffff != expected:
                raise ValueError('PNG chunk CRC mismatch')
            pos = end
            if kind == b'IEND':
                if n != 0 or pos != len(data):
                    raise ValueError('invalid IEND or trailing bytes')
                ended = True
                break
        if not ended:
            raise ValueError('missing IEND')
        with Image.open(io.BytesIO(data)) as im:
            im.verify()
        with Image.open(io.BytesIO(data)) as im:
            im.load()
            size = list(im.size)
            if im.size != (width, height):
                errors.append('dimensions do not match requested template')
            if getattr(im, 'n_frames', 1) != 1:
                errors.append('animated PNG is not a static wrap')
    except Exception as exc:
        errors.append(str(exc))
    return dict(file=name, bytes=len(data), dimensions=size,
                sha256=hashlib.sha256(data).hexdigest(), errors=errors)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--width', required=True, type=int)
    parser.add_argument('--height', required=True, type=int)
    parser.add_argument('--max-bytes', type=int, default=1000000)
    args = parser.parse_args()
    results, errors = [], []
    try:
        if args.file.suffix.lower() == '.zip':
            with zipfile.ZipFile(args.file) as archive:
                entries = [e for e in archive.infolist() if not e.is_dir()]
                if not entries:
                    errors.append('empty archive')
                seen = set()
                for entry in entries:
                    if entry.filename in seen:
                        errors.append('duplicate archive member: ' + entry.filename)
                    seen.add(entry.filename)
                    if Path(entry.filename).suffix.lower() != '.png':
                        errors.append('unexpected non-PNG member: ' + entry.filename)
                        continue
                    if entry.file_size > max(args.max_bytes * 4, 20000000):
                        errors.append('member too large to decode safely: ' + entry.filename)
                        continue
                    # Reading to EOF checks the ZIP CRC as well as subsequent PNG checks.
                    data = archive.read(entry)
                    results.append(check_png(data, entry.filename, args.width,
                                             args.height, args.max_bytes))
        else:
            results.append(check_png(args.file.read_bytes(), args.file.name,
                                     args.width, args.height, args.max_bytes))
    except Exception as exc:
        errors.append(str(exc))
    passed = bool(results) and not errors and all(not x['errors'] for x in results)
    print(json.dumps(dict(passed=passed, scope='file format only; UV mapping unverified',
                          errors=errors, files=results), ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
