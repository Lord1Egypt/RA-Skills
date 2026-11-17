"""Call the RageHealth skin-pro open API.

Single endpoint under the configured base URL
(default: `gateway.ragehealth.cn/openapi-prod`):
    POST /face/skin-pro

Auth identical to tcm-face-tongue: AES-CBC + PKCS7 + base64, key=SK, iv=AK,
content = ak|uuid|now_ms; sent as headers AccessKey / Signature; body is
multipart/form-data.

Usage:
    python call_skin_pro.py \\
        --image-url https://example.com/face.jpg \\
        [--analyse-strategy 1] [--face-id-detect --user-group demo]

Credentials are read from env vars SKIN_PRO_AK / SKIN_PRO_SK and never accepted
as CLI arguments.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import uuid
from typing import Optional

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

DEFAULT_BASE_URL = "https://gateway.ragehealth.cn/openapi-prod"
ENDPOINT = "/face/skin-pro"

# Detection objects whose polygon / landmark-index arrays dwarf the summary.
_POLYGON_PARENTS = ("acne", "acne_mark", "brown_spot", "mole", "wrinkle_details")
_LARGE_KEYS = ("display_landmarks", "raw_landmarks", "landmarks")


def generate_signature(access_key: str, secret_key: str) -> str:
    """Generate Signature equivalent to the platform's CryptoJS sample.

    content = ak + "|" + uuid + "|" + now_ms
    key/iv  = utf-8 bytes of sk / ak (sk must be 16/24/32 bytes, ak 16 bytes)
    cipher  = AES-CBC + PKCS7
    output  = base64(ciphertext)
    """
    ak_bytes = access_key.encode("utf-8")
    sk_bytes = secret_key.encode("utf-8")
    if len(ak_bytes) != 16:
        raise ValueError(
            f"AccessKey must be 16 bytes for AES IV, got {len(ak_bytes)} bytes."
        )
    if len(sk_bytes) not in (16, 24, 32):
        raise ValueError(
            f"SecretKey must be 16/24/32 bytes for AES key, got {len(sk_bytes)} bytes."
        )

    content = f"{access_key}|{uuid.uuid4()}|{int(time.time() * 1000)}"
    cipher = AES.new(sk_bytes, AES.MODE_CBC, iv=ak_bytes)
    encrypted = cipher.encrypt(pad(content.encode("utf-8"), AES.block_size))
    return base64.b64encode(encrypted).decode("utf-8")


def _post(
    access_key: str,
    secret_key: str,
    data: dict,
    files: Optional[dict] = None,
    base_url: str = DEFAULT_BASE_URL,
    timeout: int = 120,
) -> dict:
    url = base_url.rstrip("/") + ENDPOINT
    headers = {
        "AccessKey": access_key,
        "Signature": generate_signature(access_key, secret_key),
    }
    resp = requests.post(
        url, headers=headers, data=data, files=files, timeout=timeout
    )
    resp.raise_for_status()
    return resp.json()


def _build_optional_fields(args: argparse.Namespace) -> dict:
    data: dict = {}
    if args.analyse_strategy is not None:
        data["analyseStrategy"] = str(args.analyse_strategy)
    if args.display_res is not None:
        data["displayRes"] = str(args.display_res)
    if args.alpha_channel is not None:
        data["alphaChannel"] = str(args.alpha_channel)
    if args.face_id_detect:
        if not args.user_group:
            raise SystemExit("--user-group is required when --face-id-detect is set.")
        data["faceIdDetect"] = "true"
        data["userGroup"] = args.user_group
    return data


def call_skin_pro(args: argparse.Namespace, ak: str, sk: str) -> dict:
    """imageFile > imageBase64 > imageUrl, matching the server."""
    if not args.image_url and not args.image_file and not args.image_base64:
        raise SystemExit(
            "--image-url, --image-file, or --image-base64 is required."
        )
    data = _build_optional_fields(args)
    files = None
    fp = None
    try:
        if args.image_file:
            fp = open(args.image_file, "rb")
            files = {"imageFile": (os.path.basename(args.image_file), fp)}
        elif args.image_base64:
            data["imageBase64"] = args.image_base64
        else:
            data["imageUrl"] = args.image_url
        return _post(
            ak, sk, data, files, base_url=args.base_url, timeout=args.timeout
        )
    finally:
        if fp is not None:
            fp.close()


def _slim_for_stdout(result: dict) -> dict:
    """Strip large arrays that pollute terminal output (kept in --output file).

    Removed keys:
      - data.display_landmarks / data.raw_landmarks / data.landmarks
      - polygon and pos_indexes under acne / acne_mark / brown_spot / mole /
        wrinkle_details
    """
    import copy

    slim = copy.deepcopy(result)
    data = slim.get("data") or {}
    if not isinstance(data, dict):
        return slim

    for key in _LARGE_KEYS:
        data.pop(key, None)

    for parent in _POLYGON_PARENTS:
        obj = data.get(parent)
        if isinstance(obj, dict):
            obj.pop("polygon", None)
            obj.pop("pos_indexes", None)
    return slim


def _load_credentials() -> tuple[str, str]:
    """Resolve AK/SK from environment only.

    Credentials are NEVER passed as tool arguments by the LLM. The host is
    responsible for injecting them via environment variables.

    Optional: auto-load a sibling `.env` file if `python-dotenv` is available.
    """
    try:  # pragma: no cover - optional dependency
        from dotenv import load_dotenv

        load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
        load_dotenv()  # also pick up CWD .env
    except ImportError:
        pass

    ak = os.getenv("SKIN_PRO_AK")
    sk = os.getenv("SKIN_PRO_SK")
    if not ak or not sk:
        raise SystemExit(
            "Missing credentials. Set env vars SKIN_PRO_AK / SKIN_PRO_SK "
            "(or define them in a .env file). They must NOT be passed as CLI args."
        )
    return ak, sk


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Call the RageHealth skin-pro API. Credentials (AK/SK) are read from "
            "env vars SKIN_PRO_AK / SKIN_PRO_SK and are intentionally not exposed "
            "as CLI flags."
        )
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--image-url")
    parser.add_argument("--image-file")
    parser.add_argument("--image-base64")
    parser.add_argument("--analyse-strategy", type=int, choices=[1, 2])
    parser.add_argument("--display-res", type=int, choices=[0, 1])
    parser.add_argument("--alpha-channel", type=int, choices=[0, 1])
    parser.add_argument("--face-id-detect", action="store_true")
    parser.add_argument("--user-group")
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="HTTP timeout in seconds. The server waits for the detector.",
    )
    parser.add_argument("--output", help="Optional path to write full JSON response.")
    parser.add_argument(
        "--full-stdout",
        action="store_true",
        help="Print the full response to stdout. By default landmark arrays and "
             "detection polygons are stripped from stdout. The --output file always "
             "contains the full response.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    ak, sk = _load_credentials()
    result = call_skin_pro(args, ak, sk)

    full_text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(full_text)

    if args.full_stdout:
        print(full_text)
    else:
        slim = _slim_for_stdout(result)
        print(json.dumps(slim, ensure_ascii=False, indent=2))
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
