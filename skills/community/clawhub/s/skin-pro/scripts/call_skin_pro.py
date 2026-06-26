"""Call RageHealth open API: POST /face/skin-pro.

Generates the platform Signature (AES-CBC + PKCS7, base64) and posts the request
as multipart/form-data. Equivalent to the official JS sample using CryptoJS.

Usage:
    python call_skin_pro.py --access-key AK --secret-key SK \
        --image-url https://example.com/face.jpg [--analyse-strategy 1]
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

DEFAULT_ENDPOINT = "https://facepro.ragehealth.cn/openapi-test/face/skin-pro"


def generate_signature(access_key: str, secret_key: str) -> str:
    """Generate Signature equivalent to the platform's CryptoJS sample.

    content   = ak + "|" + uuid + "|" + now_ms
    key/iv    = utf-8 bytes of sk / ak (sk must be 16/24/32 bytes, ak must be 16 bytes)
    cipher    = AES-CBC + PKCS7
    output    = base64(ciphertext)
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


def call_skin_pro(
    access_key: str,
    secret_key: str,
    image_url: Optional[str] = None,
    image_file: Optional[str] = None,
    face_id_detect: bool = False,
    user_group: Optional[str] = None,
    analyse_strategy: int = 1,
    endpoint: str = DEFAULT_ENDPOINT,
    timeout: int = 60,
) -> dict:
    if not image_url and not image_file:
        raise ValueError("Either image_url or image_file is required.")
    if face_id_detect and not user_group:
        raise ValueError("user_group is required when face_id_detect=True.")

    signature = generate_signature(access_key, secret_key)
    headers = {"AccessKey": access_key, "Signature": signature}

    data = {"analyseStrategy": str(analyse_strategy)}
    if face_id_detect:
        data["faceIdDetect"] = "true"
        data["userGroup"] = user_group
    if image_url and not image_file:
        data["imageUrl"] = image_url

    files = None
    fp = None
    try:
        if image_file:
            fp = open(image_file, "rb")
            files = {"imageFile": (os.path.basename(image_file), fp)}
        resp = requests.post(
            endpoint, headers=headers, data=data, files=files, timeout=timeout
        )
    finally:
        if fp is not None:
            fp.close()

    resp.raise_for_status()
    return resp.json()


def _format_summary(result: dict) -> str:
    """Compact, LLM-friendly digest of the skin-pro response.

    Includes only the fields needed to render a user-facing report:
    image_quality gate, comprehensive scores, skin_type/tone, analyse_result
    list, key counts, and display_img. Drops polygons / landmarks / face_maps.
    """
    if not result.get("success"):
        return json.dumps(result, ensure_ascii=False, indent=2)
    d = result.get("data", {}) or {}
    iq = d.get("image_quality", {}) or {}
    digest = {
        "requestId": result.get("requestId"),
        "image_quality": {
            "brightness_grade": (iq.get("brightness") or {}).get("grade"),
            "blur": iq.get("blur"),
            "face_ratio": iq.get("face_ratio"),
            "hair_occlusion": iq.get("hair_occlusion"),
            "face_orientation": iq.get("face_orientation"),
        },
        "overall": {
            "skin_score": d.get("skin_score"),
            "skin_age": d.get("skin_age"),
            "skin_rank": d.get("skin_rank"),
            "aging_index": d.get("aging_index"),
            "skd": d.get("skd"),
        },
        "skin_type": (d.get("skin_type") or {}).get("skin_type"),
        "skin_tone": (d.get("skin_tone") or {}).get("value"),
        "analyse_result": [
            {
                "type": x.get("type"),
                "score": x.get("score"),
                "label": x.get("label"),
                "leftScore": x.get("leftScore"),
                "rightScore": x.get("rightScore"),
            }
            for x in (d.get("analyse_result") or [])
        ],
        "counts": {
            "blackhead_count": d.get("blackhead_count"),
            "enlarged_pore_count": d.get("enlarged_pore_count"),
            "wrinkle_count": d.get("wrinkle_count"),
        },
        "display_img": d.get("display_img"),
    }
    return json.dumps(digest, ensure_ascii=False, indent=2)


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

    ak = os.getenv("SKIN_PRO_AK")
    sk = os.getenv("SKIN_PRO_SK")
    if not ak or not sk:
        raise SystemExit(
            "Missing credentials. Set env vars SKIN_PRO_AK / SKIN_PRO_SK "
            "(or define them in a .env file). They must NOT be passed as CLI args."
        )
    return ak, sk


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Call skin-pro open API. Credentials (AK/SK) are read from env vars "
            "SKIN_PRO_AK / SKIN_PRO_SK and are intentionally not exposed as CLI flags."
        )
    )
    parser.add_argument("--image-url")
    parser.add_argument("--image-file")
    parser.add_argument("--face-id-detect", action="store_true")
    parser.add_argument("--user-group")
    parser.add_argument("--analyse-strategy", type=int, default=1, choices=[1, 2])
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--output", help="Optional path to write JSON response.")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print compact key-indicator summary instead of full JSON.",
    )
    args = parser.parse_args()

    access_key, secret_key = _load_credentials()

    result = call_skin_pro(
        access_key=access_key,
        secret_key=secret_key,
        image_url=args.image_url,
        image_file=args.image_file,
        face_id_detect=args.face_id_detect,
        user_group=args.user_group,
        analyse_strategy=args.analyse_strategy,
        endpoint=args.endpoint,
    )

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    if args.summary:
        print(_format_summary(result))
    else:
        print(text)
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
