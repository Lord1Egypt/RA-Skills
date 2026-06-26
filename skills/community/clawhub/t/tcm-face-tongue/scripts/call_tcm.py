"""Call RageHealth TCM (face / tongue / combined) open APIs.

Three subcommands map to three endpoints under the configured base URL
(default: `facepro.ragehealth.cn/openapi-test`; prod: `gateway.ragehealth.cn/openapi-prod`):
    face      -> POST /face/tcm-analyse                  (望面)
    tongue    -> POST /face/tongue                       (望舌)
    combined  -> POST /face/comprehensive-interpretation (面舌辨证)

Auth identical to skin-pro: AES-CBC + PKCS7 + base64, key=SK, iv=AK,
content = ak|uuid|now_ms; sent as headers AccessKey / Signature; body is
multipart/form-data.

Usage:
    python call_tcm.py face --image-url https://example.com/face.jpg \\
        [--province 广东省 --city 深圳市] [--age 30] [--gender 0]
    python call_tcm.py tongue --image-url https://example.com/tongue.jpg
    python call_tcm.py combined \\
        --face-image-url https://example.com/face.jpg \\
        --tongue-image-url https://example.com/tongue.jpg \\
        [--age 30 --gender 0 --province 广东省 --city 深圳市]

Credentials are read from env vars TCM_AK / TCM_SK and never accepted as
CLI arguments.
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

DEFAULT_BASE_URL = "https://facepro.ragehealth.cn/openapi-test"
ENDPOINTS = {
    "face": "/face/tcm-analyse",
    "tongue": "/face/tongue",
    "combined": "/face/comprehensive-interpretation",
}


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
    return binascii.b2a_base64(encrypted, newline=False).decode("ascii")


def _post(
    access_key: str,
    secret_key: str,
    endpoint_path: str,
    data: dict,
    files: Optional[dict] = None,
    base_url: str = DEFAULT_BASE_URL,
    timeout: int = 60,
) -> dict:
    url = base_url.rstrip("/") + endpoint_path
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
    """Common optional fields shared by face & combined endpoints."""
    data: dict = {}
    if getattr(args, "customer_ip", None):
        data["customerIp"] = args.customer_ip
    if getattr(args, "province", None) and getattr(args, "city", None):
        data["province"] = args.province
        data["city"] = args.city
    if getattr(args, "fallback_province", None) and getattr(args, "fallback_city", None):
        data["fallbackProvince"] = args.fallback_province
        data["fallbackCity"] = args.fallback_city
    if getattr(args, "age", None) is not None:
        data["age"] = str(args.age)
    if getattr(args, "gender", None) is not None:
        data["gender"] = str(args.gender)
    if getattr(args, "skin_info", None):
        data["skinInfo"] = args.skin_info
    if getattr(args, "face_id_detect", False):
        data["faceIdDetect"] = "true"
        if not getattr(args, "user_group", None):
            raise SystemExit("--user-group is required when --face-id-detect is set.")
        data["userGroup"] = args.user_group
    return data


def call_face(args: argparse.Namespace, ak: str, sk: str) -> dict:
    if not args.image_url and not args.image_file:
        raise SystemExit("face: --image-url or --image-file is required.")
    data = _build_optional_fields(args)
    if args.image_url and not args.image_file:
        data["imageUrl"] = args.image_url
    files = None
    fp = None
    try:
        if args.image_file:
            fp = open(args.image_file, "rb")
            files = {"imageFile": (os.path.basename(args.image_file), fp)}
        return _post(ak, sk, ENDPOINTS["face"], data, files, base_url=args.base_url)
    finally:
        if fp is not None:
            fp.close()


def call_tongue(args: argparse.Namespace, ak: str, sk: str) -> dict:
    if not args.image_url and not args.image_file:
        raise SystemExit("tongue: --image-url or --image-file is required.")
    data: dict = {}
    if args.image_url and not args.image_file:
        data["imageUrl"] = args.image_url
    files = None
    fp = None
    try:
        if args.image_file:
            fp = open(args.image_file, "rb")
            files = {"imageFile": (os.path.basename(args.image_file), fp)}
        return _post(ak, sk, ENDPOINTS["tongue"], data, files, base_url=args.base_url)
    finally:
        if fp is not None:
            fp.close()


def call_combined(args: argparse.Namespace, ak: str, sk: str) -> dict:
    """Combined (面舌辨证).

    The official endpoint /face/comprehensive-interpretation requires public
    URLs for both images. To make local files usable we fall back to calling
    /face/tcm-analyse + /face/tongue separately when ANY of the two inputs is
    a local file, then synthesize a response that mirrors the combined shape
    (faceTcm / tongueTcm) but with comprehensiveInterpretation = null.
    """
    face_url = getattr(args, "face_image_url", None)
    tongue_url = getattr(args, "tongue_image_url", None)
    face_file = getattr(args, "face_image_file", None)
    tongue_file = getattr(args, "tongue_image_file", None)

    if not (face_url or face_file):
        raise SystemExit("combined: --face-image-url or --face-image-file is required.")
    if not (tongue_url or tongue_file):
        raise SystemExit("combined: --tongue-image-url or --tongue-image-file is required.")

    # Both URLs -> use the official combined endpoint
    if face_url and tongue_url and not face_file and not tongue_file:
        data = _build_optional_fields(args)
        data["faceImageUrl"] = face_url
        data["tongueImageUrl"] = tongue_url
        return _post(ak, sk, ENDPOINTS["combined"], data, base_url=args.base_url)

    # Otherwise -> client-side fallback: call face + tongue separately
    face_args = argparse.Namespace(**vars(args))
    face_args.image_url = face_url
    face_args.image_file = face_file
    face_resp = call_face(face_args, ak, sk)

    tongue_args = argparse.Namespace(**vars(args))
    tongue_args.image_url = tongue_url
    tongue_args.image_file = tongue_file
    tongue_resp = call_tongue(tongue_args, ak, sk)

    return {
        "success": bool(face_resp.get("success") and tongue_resp.get("success")),
        "data": {
            "faceTcm": face_resp.get("data"),
            "tongueTcm": tongue_resp.get("data"),
            "comprehensiveInterpretation": None,
            "_clientFallback": True,
        },
        "requestId": {
            "face": face_resp.get("requestId"),
            "tongue": tongue_resp.get("requestId"),
        },
    }


def _slim_for_stdout(result: dict) -> dict:
    """Strip large arrays that pollute terminal output (kept in --output file).

    Removed keys:
      - data.landmarks / data.raw_landmarks / data.face_id_keypoints
        (hundreds of [x, y] points; field name varies across API versions)
      - data.detection.polygon (tongue-edge polygons)
      - same fields nested under data.faceTcm / data.tongueTcm in combined mode
    """
    import copy

    slim = copy.deepcopy(result)
    data = slim.get("data") or {}

    _LARGE_FACE_KEYS = ("landmarks", "raw_landmarks", "face_id_keypoints")

    def _strip_face(face_data):
        if isinstance(face_data, dict):
            for k in _LARGE_FACE_KEYS:
                face_data.pop(k, None)

    def _strip_tongue(tongue_data):
        if isinstance(tongue_data, dict):
            det = tongue_data.get("detection")
            if isinstance(det, dict):
                det.pop("polygon", None)

    _strip_face(data)
    _strip_tongue(data)
    _strip_face(data.get("faceTcm"))
    _strip_tongue(data.get("tongueTcm"))
    return slim


def _load_credentials() -> tuple[str, str]:
    """Resolve AK/SK from environment only.

    Following MCP / Coze / ModelScope convention, credentials are NEVER passed
    as tool arguments by the LLM. The host (shell, MCP client, plugin runtime)
    is responsible for injecting them via environment variables.

    Optional: auto-load a sibling `.env` file if `python-dotenv` is available.
    """
    try:  # pragma: no cover - optional dependency
        from dotenv import load_dotenv

        load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
        load_dotenv()  # also pick up CWD .env
    except ImportError:
        pass

    ak = os.getenv("TCM_AK")
    sk = os.getenv("TCM_SK")
    if not ak or not sk:
        raise SystemExit(
            "Missing credentials. Set env vars TCM_AK / TCM_SK "
            "(or define them in a .env file). They must NOT be passed as CLI args."
        )
    return ak, sk


def _add_common_geo_demo_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--customer-ip")
    p.add_argument("--province")
    p.add_argument("--city")
    p.add_argument("--fallback-province")
    p.add_argument("--fallback-city")
    p.add_argument("--age", type=int)
    p.add_argument("--gender", type=int, choices=[0, 1])
    p.add_argument("--skin-info")
    p.add_argument("--face-id-detect", action="store_true")
    p.add_argument("--user-group")


def _add_io_args(p: argparse.ArgumentParser) -> None:
    """IO flags shared by every subcommand. Placed on subparsers so they can
    appear *after* the subcommand name (avoids the common UX trap where
    `tongue --output x.json` errored as 'unrecognized arguments').

    `default=SUPPRESS` ensures these subparser entries do NOT clobber values
    already set by the top-level parser when the user puts the flag before
    the subcommand.
    """
    p.add_argument("--base-url", default=argparse.SUPPRESS)
    p.add_argument(
        "--output",
        default=argparse.SUPPRESS,
        help="Optional path to write full JSON response.",
    )
    p.add_argument(
        "--full-stdout",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Print the full response to stdout. By default large arrays "
             "(face_id_keypoints, detection.polygon) are stripped from stdout "
             "to keep terminal output readable. The --output file always "
             "contains the full response.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Call RageHealth TCM open APIs. Credentials (AK/SK) are read from env vars "
            "TCM_AK / TCM_SK and are intentionally not exposed as CLI flags."
        )
    )
    # Top-level mirrors so flags work both before and after the subcommand.
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--output", help="Optional path to write full JSON response.")
    parser.add_argument("--full-stdout", action="store_true")
    sub = parser.add_subparsers(dest="mode", required=True)

    # face
    pf = sub.add_parser("face", help="望面 face-tcm-analyse")
    pf.add_argument("--image-url")
    pf.add_argument("--image-file")
    _add_common_geo_demo_args(pf)
    _add_io_args(pf)

    # tongue
    pt = sub.add_parser("tongue", help="望舌 tongue-diagnosis")
    pt.add_argument("--image-url")
    pt.add_argument("--image-file")
    _add_io_args(pt)

    # combined
    pc = sub.add_parser(
        "combined", help="面舌辨证 face-tongue-diagnosis"
    )
    pc.add_argument("--face-image-url")
    pc.add_argument("--face-image-file")
    pc.add_argument("--tongue-image-url")
    pc.add_argument("--tongue-image-file")
    _add_common_geo_demo_args(pc)
    _add_io_args(pc)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    ak, sk = _load_credentials()

    if args.mode == "face":
        result = call_face(args, ak, sk)
    elif args.mode == "tongue":
        result = call_tongue(args, ak, sk)
    elif args.mode == "combined":
        result = call_combined(args, ak, sk)
    else:  # pragma: no cover - argparse guards
        parser.error(f"unknown mode: {args.mode}")

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
