#!/usr/bin/env python3
"""Extract embedded transcript from Apple Voice Memo m4a file.

Apple Voice Memos may contain auto-generated transcripts stored as
tsrp atoms inside the m4a container. This script extracts them.
"""
import struct
import sys
import os


def find_atom(data, atom_type, offset=0, end=None):
    """Find an atom by type in m4a/MPEG-4 container."""
    if end is None:
        end = len(data)
    while offset < end - 8:
        size = struct.unpack(">I", data[offset:offset + 4])[0]
        if size == 1 and offset + 16 <= end:
            size = struct.unpack(">Q", data[offset + 8:offset + 16])[0]
        elif size == 0:
            size = end - offset
        if size < 8 or offset + size > end:
            break
        atype = data[offset + 4:offset + 8]
        if atype == atom_type:
            return offset, size
        offset += size
    return None, None


def extract_transcript(filepath):
    """Extract tsrp transcript from m4a."""
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        return 1

    with open(filepath, "rb") as f:
        data = f.read()

    # Scan all top-level atoms to find moov
    # Handle both 32-bit and 64-bit (extended size) atoms
    offset = 0
    moov_off, moov_size = None, None
    while offset < len(data) - 8:
        size = struct.unpack(">I", data[offset:offset + 4])[0]
        atype = data[offset + 4:offset + 8]
        if size == 1 and offset + 16 <= len(data):
            # 64-bit extended size
            size = struct.unpack(">Q", data[offset + 8:offset + 16])[0]
        elif size == 0:
            # Atom extends to end of file
            size = len(data) - offset
        if size < 8:
            break
        if atype == b"moov":
            moov_off, moov_size = offset, size
            break
        offset += size
    
    if moov_off is None:
        print("ERROR: moov atom not found — not a valid m4a file")
        return 1

    moov_end = moov_off + moov_size

    # Find udta atom inside moov
    udta_off, udta_size = find_atom(data, b"udta", moov_off + 8, moov_end)
    if udta_off is None:
        print("NO_TRANSCRIPT: no embedded transcript found")
        return 0

    udta_end = udta_off + udta_size

    # Find tsrp atom inside udta
    tsrp_off, tsrp_size = find_atom(data, b"tsrp", udta_off + 8, udta_end)
    if tsrp_off is None:
        print("NO_TRANSCRIPT: no embedded transcript found")
        return 0

    # Extract transcript — skip 8 byte atom header + 4 byte version/flags
    header_size = 12
    tsrp_data = data[tsrp_off + header_size:tsrp_off + tsrp_size]

    if len(tsrp_data) == 0:
        print("NO_TRANSCRIPT: transcript atom is empty")
        return 0

    # Try decoding
    for encoding in ["utf-8", "utf-16", "utf-16-le", "utf-16-be"]:
        try:
            text = tsrp_data.decode(encoding)
            # Strip null characters and whitespace
            text = text.replace("\x00", "").strip()
            if text:
                print(text)
                return 0
        except (UnicodeDecodeError, ValueError):
            continue

    print("ERROR: Cannot decode transcript")
    return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_transcript.py <m4a_file>")
        sys.exit(1)
    sys.exit(extract_transcript(sys.argv[1]))
