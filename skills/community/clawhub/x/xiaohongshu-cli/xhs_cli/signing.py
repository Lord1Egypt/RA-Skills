"""
Main API signing for edith.xiaohongshu.com

Generates x-s, x-s-common, x-t, x-b3-traceid, x-xray-traceid headers.

Algorithm overview (v4.3.1, 144-byte payload):
  1. MD5 hash of content string (URI + params/body)
  2. Build 144-byte binary payload array (with a3 hash segment)
  3. XOR with static 144-byte hex key
  4. Custom Base64 encode (shuffled alphabet)
  5. Wrap in JSON envelope → another custom Base64 → XYS_ prefix

Ported from: ~/readers/redbook/src/lib/signing.ts (Cloxl/xhshow, MIT license)
"""

import hashlib
import json
import os
import random
import struct
import time
from typing import Any

from .constants import APP_ID, PLATFORM, SDK_VERSION, USER_AGENT

# ─── Constants ──────────────────────────────────────────────────────────────

STANDARD_BASE64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
CUSTOM_BASE64 = "ZmserbBoHQtNP+wOcza/LpngG8yJq42KWYj0DSfdikx3VT16IlUAFM97hECvuRX5"
X3_BASE64 = "MfgqrsbcyzPQRStuvC7mn501HIJBo2DEFTKdeNOwxWXYZap89+/A4UVLhijkl63G"

HEX_KEY = (
    "71a302257793271ddd273bcee3e4b98d9d7935e1da33f5765e2ea8afb6dc77a5"
    "1a499d23b67c20660025860cbf13d4540d92497f58686c574e508f46e1956344"
    "f39139bf4faf22a3eef120b79258145b2feb5193b6478669961298e79bedca64"
    "6e1a693a926154a5a7a1bd1cf0dedb742f917a747a1e388b234f2277516db711"
    "6035439730fa61e9822a0eca7bff72d8"
)

VERSION_BYTES = [121, 104, 96, 41]
PAYLOAD_LENGTH = 144

# Environment detection constants (part11)
ENV_TABLE = [115, 248, 83, 102, 103, 201, 181, 131, 99, 94, 4, 68, 250, 132, 21]
ENV_CHECKS_DEFAULT = [0, 1, 18, 1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0]

# A3 hash segment constants
A3_PREFIX = [2, 97, 51, 16]
HASH_IV = (1831565813, 461845907, 2246822507, 3266489909)
MAX_32BIT = 0xFFFFFFFF

X3_PREFIX = "mns0301_"
XYS_PREFIX = "XYS_"

B1_SECRET_KEY = "xhswebmplfbt"
HEX_CHARS = "abcdef0123456789"

XSCOMMON_TEMPLATE = {
    "s0": 5,
    "s1": "",
    "x0": "1",
    "x1": SDK_VERSION,
    "x2": PLATFORM,
    "x3": APP_ID,
    "x4": "4.86.0",
    "x5": "",  # a1 cookie
    "x6": "",
    "x7": "",
    "x8": "",  # b1 fingerprint
    "x9": -596800761,
    "x10": 0,
    "x11": "normal",
}

SIGNATURE_DATA_TEMPLATE = {
    "x0": SDK_VERSION,
    "x1": APP_ID,
    "x2": PLATFORM,
    "x3": "",  # x3 signature
    "x4": "",
}

# GPU vendors for fingerprint — macOS-appropriate entries
GPU_VENDORS = [
    "Apple|Apple M1",
    "Apple|Apple M1 Pro",
    "Apple|Apple M1 Max",
    "Apple|Apple M2",
    "Apple|Apple M2 Pro",
    "Apple|Apple M3",
    "Apple|Apple M3 Pro",
    "Google Inc. (Intel)|ANGLE (Intel, Intel(R) Iris(TM) Plus Graphics 655 OpenGL Engine)",
    "Google Inc. (Intel)|ANGLE (Intel, Intel(R) UHD Graphics 630 OpenGL Engine)",
    "Google Inc. (AMD)|ANGLE (AMD, AMD Radeon Pro 5500M OpenGL Engine)",
]

# macOS-typical screen resolutions (Retina-heavy)
SCREEN_RESOLUTIONS = [
    ("2560;1600", 0.30),  # MacBook Pro 14"
    ("3024;1964", 0.15),  # MacBook Pro 14" Retina
    ("3456;2234", 0.10),  # MacBook Pro 16" Retina
    ("2560;1440", 0.15),  # External display
    ("1920;1080", 0.10),  # External display
    ("1440;900",  0.10),  # MacBook Air 13"
    ("2880;1800", 0.05),  # Older MacBook Pro Retina
    ("5120;2880", 0.05),  # Apple Studio Display
]

FINGERPRINT_PLUGINS = (
    "PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf;"
    "Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf;"
    "Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf;"
    "Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf;"
    "WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf"
)

FINGERPRINT_FONTS = (
    "Arial,Arial Black,Arial Narrow,Book Antiqua,Bookman Old Style,"
    "Calibri,Cambria,Cambria Math,Century,Century Gothic,Century Schoolbook,"
    "Comic Sans MS,Consolas,Courier,Courier New,Georgia,Helvetica,"
    "Impact,Lucida Bright,Lucida Calligraphy,Lucida Console,Lucida Fax,"
    "Lucida Handwriting,Lucida Sans,Lucida Sans Typewriter,Lucida Sans Unicode,"
    "Microsoft Sans Serif,Monotype Corsiva,MS Gothic,MS PGothic,MS Reference Sans Serif,"
    "MS Sans Serif,MS Serif,Palatino Linotype,Segoe Print,Segoe Script,"
    "Segoe UI,Segoe UI Light,Segoe UI Semibold,Segoe UI Symbol,"
    "Tahoma,Times,Times New Roman,Trebuchet MS,Verdana,Wingdings,Wingdings 3"
)


# ─── Base64 Encoding ─────────────────────────────────────────────────────────

def _make_translate_table(from_chars: str, to_chars: str) -> dict[int, int]:
    return str.maketrans(from_chars, to_chars)


_custom_encode_table = _make_translate_table(STANDARD_BASE64, CUSTOM_BASE64)
_x3_encode_table = _make_translate_table(STANDARD_BASE64, X3_BASE64)


def _custom_base64_encode(data: bytes | str) -> str:
    """Custom Base64 encode with shuffled alphabet."""
    import base64
    if isinstance(data, str):
        data = data.encode("utf-8")
    standard = base64.b64encode(data).decode("ascii")
    return standard.translate(_custom_encode_table)


def _x3_base64_encode(data: bytes) -> str:
    """X3 Base64 encode with alternate shuffled alphabet."""
    import base64
    standard = base64.b64encode(data).decode("ascii")
    return standard.translate(_x3_encode_table)


# ─── Utility Functions ───────────────────────────────────────────────────────

def _hex_to_bytes(hex_str: str) -> bytes:
    return bytes.fromhex(hex_str)


def _int_to_le_bytes(val: int, length: int = 4) -> list[int]:
    """Convert integer to little-endian byte list."""
    if length <= 4:
        return list(struct.pack("<I", val & 0xFFFFFFFF)[:length])
    else:
        return list(struct.pack("<Q", val & 0xFFFFFFFFFFFFFFFF)[:length])


def _rotate_left(val: int, n: int) -> int:
    """32-bit left rotation."""
    return ((val << n) | (val >> (32 - n))) & MAX_32BIT


# ─── A3 Hash Functions ──────────────────────────────────────────────────────

def _custom_hash_v2(input_bytes: list[int]) -> list[int]:
    """Custom hash function for A3 segment."""
    s0, s1, s2, s3 = HASH_IV
    length = len(input_bytes)

    s0 = (s0 ^ length) & MAX_32BIT
    s1 = (s1 ^ ((length << 8) & MAX_32BIT)) & MAX_32BIT
    s2 = (s2 ^ ((length << 16) & MAX_32BIT)) & MAX_32BIT
    s3 = (s3 ^ ((length << 24) & MAX_32BIT)) & MAX_32BIT

    buf = bytes(input_bytes)
    for i in range(len(buf) // 8):
        v0 = struct.unpack_from("<I", buf, i * 8)[0]
        v1 = struct.unpack_from("<I", buf, i * 8 + 4)[0]

        s0 = _rotate_left(((s0 + v0) & MAX_32BIT) ^ s2, 7)
        s1 = _rotate_left(((v0 ^ s1) + s3) & MAX_32BIT, 11)
        s2 = _rotate_left(((s2 + v1) & MAX_32BIT) ^ s0, 13)
        s3 = _rotate_left(((s3 ^ v1) + s1) & MAX_32BIT, 17)

    t0 = (s0 ^ length) & MAX_32BIT
    t1 = (s1 ^ t0) & MAX_32BIT
    t2 = (s2 + t1) & MAX_32BIT
    t3 = (s3 ^ t2) & MAX_32BIT

    rot_t0 = _rotate_left(t0, 9)
    rot_t1 = _rotate_left(t1, 13)
    rot_t2 = _rotate_left(t2, 17)
    rot_t3 = _rotate_left(t3, 19)

    s0 = (rot_t0 + rot_t2) & MAX_32BIT
    s1 = (rot_t1 ^ rot_t3) & MAX_32BIT
    s2 = (rot_t2 + s0) & MAX_32BIT
    s3 = (rot_t3 ^ s1) & MAX_32BIT

    result: list[int] = []
    for s in [s0, s1, s2, s3]:
        result.extend(_int_to_le_bytes(s, 4))
    return result


def _extract_api_path(uri_with_data: str) -> str:
    """Extract API path from URI, stripping query params and body."""
    brace_pos = uri_with_data.find("{")
    question_pos = uri_with_data.find("?")

    if brace_pos != -1 and question_pos != -1:
        return uri_with_data[:min(brace_pos, question_pos)]
    elif brace_pos != -1:
        return uri_with_data[:brace_pos]
    elif question_pos != -1:
        return uri_with_data[:question_pos]
    return uri_with_data


# ─── Payload Builder ────────────────────────────────────────────────────────

def _build_payload_array(
    hex_parameter: str,
    a1_value: str,
    content_string: str,
    timestamp: float | None = None,
) -> list[int]:
    """Build 144-byte payload array for signing."""
    payload: list[int] = []

    # Version bytes [0-3]
    payload.extend(VERSION_BYTES)

    # Random seed [4-7]
    seed = struct.unpack("<I", os.urandom(4))[0]
    seed_bytes = _int_to_le_bytes(seed, 4)
    payload.extend(seed_bytes)
    seed_byte0 = seed_bytes[0]

    # Timestamp
    ts = timestamp if timestamp is not None else time.time()
    ts_ms = int(ts * 1000)

    # Timestamp bytes [8-15]
    ts_bytes = _int_to_le_bytes(ts_ms, 8)
    payload.extend(ts_bytes)

    # Page load timestamp [16-23]
    time_offset = random.randint(10, 50)
    page_load_ts = int((ts - time_offset) * 1000)
    payload.extend(_int_to_le_bytes(page_load_ts, 8))

    # Sequence counter [24-27]
    payload.extend(_int_to_le_bytes(random.randint(15, 50), 4))

    # Window props length [28-31]
    payload.extend(_int_to_le_bytes(random.randint(1000, 1200), 4))

    # URI content length [32-35] — UTF-8 byte length
    payload.extend(_int_to_le_bytes(len(content_string.encode("utf-8")), 4))

    # MD5 XOR segment [36-43]
    md5_bytes = _hex_to_bytes(hex_parameter)
    for i in range(8):
        payload.append(md5_bytes[i] ^ seed_byte0)

    # A1 length marker [44]
    payload.append(52)

    # A1 content [45-96] (52 bytes, padded/truncated)
    a1_bytes = a1_value.encode("utf-8")
    for i in range(52):
        payload.append(a1_bytes[i] if i < len(a1_bytes) else 0)

    # Source length marker [97]
    payload.append(10)

    # Source content [98-107] ("xhs-pc-web", 10 bytes)
    source_bytes = APP_ID.encode("utf-8")
    for i in range(10):
        payload.append(source_bytes[i] if i < len(source_bytes) else 0)

    # Part 11: Environment detection [108-123] (16 bytes)
    payload.append(1)  # env marker
    payload.append(seed_byte0 ^ ENV_TABLE[0])
    for i in range(1, 15):
        payload.append(ENV_TABLE[i] ^ ENV_CHECKS_DEFAULT[i])

    # A3 segment [124-143] (20 bytes)
    api_path = _extract_api_path(content_string)
    api_path_md5 = hashlib.md5(api_path.encode("utf-8")).hexdigest()
    md5_path_bytes: list[int] = []
    for i in range(0, 32, 2):
        md5_path_bytes.append(int(api_path_md5[i:i + 2], 16))

    hash_input = list(ts_bytes) + md5_path_bytes  # 8 + 16 = 24 bytes
    hash_output = _custom_hash_v2(hash_input)
    payload.extend(A3_PREFIX)
    for b in hash_output:
        payload.append(b ^ seed_byte0)

    return payload


# ─── XOR Transform ──────────────────────────────────────────────────────────

def _xor_transform(source: list[int]) -> bytes:
    """XOR payload with static hex key."""
    key_bytes = _hex_to_bytes(HEX_KEY)
    result = bytearray(len(source))
    for i in range(len(source)):
        if i < len(key_bytes):
            result[i] = (source[i] ^ key_bytes[i]) & 0xFF
        else:
            result[i] = source[i] & 0xFF
    return bytes(result)


# ─── CRC32 (JS-compatible variant) ──────────────────────────────────────────

_CRC32_POLY = 0xEDB88320
_crc32_table: list[int] | None = None


def _ensure_crc32_table() -> list[int]:
    global _crc32_table
    if _crc32_table is not None:
        return _crc32_table

    table = [0] * 256
    for d in range(256):
        r = d
        for _ in range(8):
            if r & 1:
                r = (r >> 1) ^ _CRC32_POLY
            else:
                r = r >> 1
        table[d] = r & MAX_32BIT
    _crc32_table = table
    return table


def _crc32_js_int(data: str) -> int:
    """CRC32 in JS-compatible mode (charCodeAt & 0xFF)."""
    table = _ensure_crc32_table()
    c = 0xFFFFFFFF

    for ch in data:
        b = ord(ch) & 0xFF
        c = (table[(c & 0xFF) ^ b] ^ (c >> 8)) & MAX_32BIT

    # JS-compatible final XOR
    u = (0xFFFFFFFF ^ c ^ _CRC32_POLY) & MAX_32BIT
    return u - 0x100000000 if u > 0x7FFFFFFF else u


# ─── RC4 Encryption ─────────────────────────────────────────────────────────

def _rc4_encrypt(key: str, data: str) -> bytes:
    """RC4 stream cipher."""
    key_bytes = key.encode("utf-8")
    data_bytes = data.encode("utf-8")

    # KSA
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) & 0xFF
        S[i], S[j] = S[j], S[i]

    # PRGA
    result = bytearray(len(data_bytes))
    i2 = 0
    j2 = 0
    for k in range(len(data_bytes)):
        i2 = (i2 + 1) & 0xFF
        j2 = (j2 + S[i2]) & 0xFF
        S[i2], S[j2] = S[j2], S[i2]
        result[k] = data_bytes[k] ^ S[(S[i2] + S[j2]) & 0xFF]

    return bytes(result)


# ─── Fingerprint Generation ─────────────────────────────────────────────────

def _weighted_choice(options: list, weights: list[float]) -> Any:
    """Weighted random selection."""
    return random.choices(options, weights=weights, k=1)[0]


def _generate_fingerprint(cookies: dict[str, str], user_agent: str) -> dict[str, Any]:
    """Generate browser fingerprint for x-s-common."""
    cookie_string = "; ".join(f"{k}={v}" for k, v in cookies.items())

    gpu_entry = random.choice(GPU_VENDORS)
    vendor, renderer = gpu_entry.split("|")

    resolutions, weights = zip(*SCREEN_RESOLUTIONS, strict=True)
    screen_res = _weighted_choice(list(resolutions), list(weights))
    width_str, height_str = screen_res.split(";")
    width = int(width_str)
    height = int(height_str)

    avail_width = width - _weighted_choice([0, 30, 60, 80], [0.1, 0.4, 0.3, 0.2]) if random.random() > 0.5 else width
    avail_height = (
        height - _weighted_choice([30, 60, 80, 100], [0.2, 0.5, 0.2, 0.1]) if random.random() > 0.5 else height
    )

    color_depth = _weighted_choice([16, 24, 30, 32], [0.05, 0.6, 0.05, 0.3])
    device_memory = _weighted_choice([1, 2, 4, 8, 12, 16], [0.1, 0.25, 0.4, 0.2, 0.03, 0.01])
    cores = _weighted_choice([2, 4, 6, 8, 12, 16, 24, 32], [0.1, 0.4, 0.2, 0.15, 0.08, 0.04, 0.02, 0.01])

    webgl_hash = hashlib.md5(os.urandom(32)).hexdigest()
    canvas_hash = "742cc32c"
    is_incognito = "true" if random.random() > 0.95 else "false"
    x78y = random.randint(2350, 2450)

    return {
        "x1": user_agent,
        "x2": "false",
        "x3": "zh-CN",
        "x4": str(color_depth),
        "x5": str(device_memory),
        "x6": "24",
        "x7": f"{vendor},{renderer}",
        "x8": str(cores),
        "x9": f"{width};{height}",
        "x10": f"{avail_width};{avail_height}",
        "x11": "-480",
        "x12": "Asia/Shanghai",
        "x13": is_incognito,
        "x14": is_incognito,
        "x15": is_incognito,
        "x16": "false",
        "x17": "false",
        "x18": "un",
        "x19": "MacIntel",
        "x20": "",
        "x21": FINGERPRINT_PLUGINS,
        "x22": webgl_hash,
        "x23": "false",
        "x24": "false",
        "x25": "false",
        "x26": "false",
        "x27": "false",
        "x28": "0,false,false",
        "x29": "4,7,8",
        "x30": "swf object not loaded",
        "x33": "0",
        "x34": "0",
        "x35": "0",
        "x36": str(random.randint(1, 20)),
        "x37": "0|0|0|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|1|0|0|0|0|0",
        "x38": "0|0|1|0|1|0|0|0|0|0|1|0|1|0|1|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0",
        "x39": 0,
        "x40": "0",
        "x41": "0",
        "x42": "3.4.4",
        "x43": canvas_hash,
        "x44": str(int(time.time() * 1000)),
        "x45": "__SEC_CAV__1-1-1-1-1|__SEC_WSA__|",
        "x46": "false",
        "x47": "1|0|0|0|0|0",
        "x48": "",
        "x49": "{list:[],type:}",
        "x50": "",
        "x51": "",
        "x52": "",
        "x55": "380,380,360,400,380,400,420,380,400,400,360,360,440,420",
        "x56": f"{vendor}|{renderer}|{webgl_hash}|35",
        "x57": cookie_string,
        "x58": "180",
        "x59": "2",
        "x60": "63",
        "x61": "1291",
        "x62": "2047",
        "x63": "0",
        "x64": "0",
        "x65": "0",
        "x66": {
            "referer": "",
            "location": "https://www.xiaohongshu.com/explore",
            "frame": 0,
        },
        "x67": "1|0",
        "x68": "0",
        "x69": "326|1292|30",
        "x70": ["location"],
        "x71": "true",
        "x72": "complete",
        "x73": "1191",
        "x74": "0|0|0",
        "x75": "Apple Inc.",
        "x76": "true",
        "x77": "1|1|1|1|1|1|1|1|1|1",
        "x78": {
            "x": 0,
            "y": x78y,
            "left": 0,
            "right": 290.828125,
            "bottom": x78y + 18,
            "height": 18,
            "top": x78y,
            "width": 290.828125,
            "font": FINGERPRINT_FONTS,
        },
        "x82": "_0x17a2|_0x1954",
        "x31": "124.04347527516074",
        "x79": "144|599565058866",
        "x53": hashlib.md5(os.urandom(32)).hexdigest(),
        "x54": "10311144241322244122",
        "x80": "1|[object FileSystemDirectoryHandle]",
    }


def _generate_b1(fp: dict[str, Any]) -> str:
    """Generate b1 field from fingerprint via RC4 encryption."""
    b1_keys = [
        "x33", "x34", "x35", "x36", "x37", "x38", "x39",
        "x42", "x43", "x44", "x45", "x46", "x48", "x49",
        "x50", "x51", "x52", "x82",
    ]
    b1_fields = {k: fp[k] for k in b1_keys}
    b1_json = json.dumps(b1_fields, separators=(",", ":"))

    ciphertext = _rc4_encrypt(B1_SECRET_KEY, b1_json)

    # URL-encode the ciphertext (latin1 interpretation), then parse byte values
    # This matches the JS behavior: encode to latin1, then encodeURIComponent
    from urllib.parse import quote
    latin1_str = ciphertext.decode("latin1")
    encoded = quote(latin1_str, safe="!'()*~._-")

    # Parse URL-encoded bytes — walk character by character to avoid
    # dropping leading ASCII chars that precede the first '%'.
    result_bytes = bytearray()
    i = 0
    while i < len(encoded):
        if encoded[i] == "%" and i + 2 < len(encoded):
            result_bytes.append(int(encoded[i + 1 : i + 3], 16))
            i += 3
        else:
            result_bytes.append(ord(encoded[i]))
            i += 1

    return _custom_base64_encode(bytes(result_bytes))


# ─── Trace ID Generation ────────────────────────────────────────────────────

def _generate_b3_trace_id() -> str:
    return os.urandom(8).hex()


def _generate_xray_trace_id(timestamp_ms: int | None = None) -> str:
    ts = timestamp_ms if timestamp_ms is not None else int(time.time() * 1000)
    seq = random.randint(0, 8388607)  # 2^23 - 1
    part1 = format((ts << 23) | seq, "016x")
    part2 = os.urandom(8).hex()
    return part1 + part2


# ─── Content String Builder ─────────────────────────────────────────────────

def _build_content_string(
    method: str,
    uri: str,
    payload: dict | None = None,
) -> str:
    if method == "POST":
        if payload is None:
            return uri
        return uri + json.dumps(payload, separators=(",", ":"))
    return uri


def build_get_uri(
    uri: str,
    params: dict[str, str | int | list[str]] | None = None,
) -> str:
    """Build URI with query parameters for GET requests."""
    if not params:
        return uri
    from urllib.parse import quote
    parts = []
    for key, value in params.items():
        str_val = ",".join(value) if isinstance(value, list) else str(value)
        encoded = quote(str_val, safe="")
        parts.append(f"{key}={encoded}")
    return f"{uri}?{'&'.join(parts)}"


def extract_uri(url: str) -> str:
    """Extract path from URL."""
    from urllib.parse import urlparse
    try:
        parsed = urlparse(url)
        return parsed.path
    except Exception:
        return url.split("?")[0]


# ─── Public API ─────────────────────────────────────────────────────────────

# ─── Session Fingerprint Cache ──────────────────────────────────────────────
# A real browser keeps the same fingerprint for the entire session.
# We cache (fingerprint, b1, x9) keyed by a1, only regenerating when the
# cookie identity changes.

_session_fp_cache: dict[str, tuple[dict[str, Any], str, int]] = {}


def _get_session_fingerprint(cookies: dict[str, str]) -> tuple[dict[str, Any], str, int]:
    """Return (fingerprint, b1, x9), cached per a1 cookie value."""
    a1 = cookies.get("a1", "")
    if a1 in _session_fp_cache:
        fp, b1, x9 = _session_fp_cache[a1]
        # Update x44 (timestamp) — this changes per request in real browsers
        fp["x44"] = str(int(time.time() * 1000))
        return fp, b1, x9

    fp = _generate_fingerprint(cookies, USER_AGENT)
    b1 = _generate_b1(fp)
    x9 = _crc32_js_int(b1)
    _session_fp_cache[a1] = (fp, b1, x9)
    return fp, b1, x9


def sign_main_api(
    method: str,
    uri: str,
    cookies: dict[str, str],
    params: dict[str, str | int | list[str]] | None = None,
    payload: dict | None = None,
    timestamp: float | None = None,
) -> dict[str, str]:
    """
    Generate all signing headers for a main API (edith.xiaohongshu.com) request.

    Returns dict with keys: x-s, x-s-common, x-t, x-b3-traceid, x-xray-traceid
    """
    a1 = cookies.get("a1", "")
    if not a1:
        raise ValueError("Missing 'a1' in cookies")

    ts = timestamp if timestamp is not None else time.time()
    ts_ms = int(ts * 1000)

    # Build URI with query params for GET
    uri_path = extract_uri(uri)
    full_uri = build_get_uri(uri_path, params) if method == "GET" else uri_path

    # Build content string for signature
    content_string = _build_content_string(method, full_uri, payload)

    # MD5 hash
    d_value = hashlib.md5(content_string.encode("utf-8")).hexdigest()

    # Build payload array and sign
    payload_array = _build_payload_array(d_value, a1, content_string, ts)
    xor_result = _xor_transform(payload_array)
    x3_signature = _x3_base64_encode(xor_result[:PAYLOAD_LENGTH])

    # Build x-s
    signature_data = dict(SIGNATURE_DATA_TEMPLATE)
    signature_data["x3"] = X3_PREFIX + x3_signature
    signature_json = json.dumps(signature_data, separators=(",", ":"))
    xs = XYS_PREFIX + _custom_base64_encode(signature_json)

    # Build x-s-common — uses session-cached fingerprint
    _fp, b1, x9 = _get_session_fingerprint(cookies)
    xs_common_struct = dict(XSCOMMON_TEMPLATE)
    xs_common_struct["x5"] = a1
    xs_common_struct["x8"] = b1
    xs_common_struct["x9"] = x9
    xs_common_json = json.dumps(xs_common_struct, separators=(",", ":"))
    xs_common = _custom_base64_encode(xs_common_json)

    return {
        "x-s": xs,
        "x-s-common": xs_common,
        "x-t": str(ts_ms),
        "x-b3-traceid": _generate_b3_trace_id(),
        "x-xray-traceid": _generate_xray_trace_id(ts_ms),
    }
