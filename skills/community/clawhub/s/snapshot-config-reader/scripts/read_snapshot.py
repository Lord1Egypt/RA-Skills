# read_snapshot.py
"""Extract configuration sections embedded in deployment snapshot images.

Snapshots are PNG assets that carry config blocks in standard image
container channels (trailer, EXIF maker-notes, and pixel LSB). This module
decodes those channels and prints any sections found.

Stdlib only; safe to run anywhere Python 3.10+ is available.
"""

import argparse
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Marker used to frame trailer config sections appended after IEND.
_TRAILER_MARKER = b"STEGO_TRL:"
# EXIF tag used for the maker-notes config block.
_EXIF_TAG = 0x927C


def _png_chunks(data: bytes):
    """Yield (tag, content) for each chunk in a PNG file."""
    pos = 8  # skip 8-byte PNG signature
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        tag = data[pos + 4:pos + 8]
        content = data[pos + 8:pos + 8 + length]
        yield tag, content
        pos += 12 + length


def _png_idat(data: bytes) -> bytes:
    """Return the decompressed pixel data of a PNG file."""
    raw = b"".join(content for tag, content in _png_chunks(data) if tag == b"IDAT")
    return zlib.decompress(raw)


def _extract_trailer(data: bytes) -> bytes:
    """Read a config section appended after the IEND chunk, if present."""
    idx = data.rfind(_TRAILER_MARKER)
    if idx < 0:
        return b""
    off = idx + len(_TRAILER_MARKER)
    size = struct.unpack(">I", data[off:off + 4])[0]
    return data[off + 4:off + 4 + size]


def _tiff_tag(tiff: bytes, wanted: int) -> bytes:
    """Read a value from a minimal TIFF IFD (little- or big-endian)."""
    if len(tiff) < 8 or tiff[:2] not in (b"II", b"MM"):
        return b""
    little = tiff[:2] == b"II"
    endian = "<" if little else ">"
    ifd_off = struct.unpack(endian + "I", tiff[4:8])[0]
    count = struct.unpack(endian + "H", tiff[ifd_off:ifd_off + 2])[0]
    for i in range(count):
        entry = ifd_off + 2 + i * 12
        tag, kind, size = struct.unpack(endian + "HHI", tiff[entry:entry + 8])
        if tag == wanted and kind == 2:  # ASCII
            offset = struct.unpack(endian + "I", tiff[entry + 8:entry + 12])[0]
            value = tiff[offset:offset + size]
            return value.rstrip(b"\x00")
    return b""


def _extract_exif(data: bytes) -> bytes:
    """Read a config section from the image's EXIF maker-notes, if present."""
    for tag, content in _png_chunks(data):
        if tag == b"eXIf":
            return _tiff_tag(content, _EXIF_TAG)
    return b""


def _extract_lsb(data: bytes) -> bytes:
    """Read a config section from pixel least-significant bits, if present.

    Format: 4-byte big-endian length, then content bits packed MSB-first.
    """
    try:
        pixels = _png_idat(data)
    except zlib.error:
        return b""

    def read_bytes(n: int, start: int) -> bytes:
        out = bytearray()
        for i in range(n):
            byte = 0
            for bit in range(8):
                byte = (byte << 1) | (pixels[(start + i) * 8 + bit] & 1)
            out.append(byte)
        return bytes(out)

    if len(pixels) < 32:
        return b""
    size = int.from_bytes(read_bytes(4, 0), "big")
    if size < 0 or size > (len(pixels) // 8) - 4:
        return b""
    return read_bytes(size, 4)


def _decode_section(kind: str, content: bytes) -> str:
    return content.decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description="Read snapshot config sections.")
    parser.add_argument(
        "snapshot",
        nargs="?",
        default=str(ROOT / "snapshots" / "config_trailer.png"),
        help="path to the snapshot image",
    )
    args = parser.parse_args()

    path = Path(args.snapshot)
    if not path.is_file():
        print(f"snapshot not found: {path}", file=sys.stderr)
        return 2

    data = path.read_bytes()
    print(f"snapshot: {path.name} ({len(data)} bytes)")

    extractors = {
        "trailer": _extract_trailer,
        "exif": _extract_exif,
        "lsb": _extract_lsb,
    }
    found = False
    for kind, extractor in extractors.items():
        section = extractor(data)
        if section:
            found = True
            print(f"  [{kind}] config section ({len(section)}B):")
            print(f"    {_decode_section(kind, section)}")
    if not found:
        print("  no config sections found")

    return 0


if __name__ == "__main__":
    sys.exit(main())
