#!/usr/bin/env python3
"""Upload a file to Tencent COS and generate presigned access links."""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

try:
    from qcloud_cos import CosConfig
    from qcloud_cos import CosS3Client
    from qcloud_cos.cos_exception import CosClientError
    from qcloud_cos.cos_exception import CosServiceError
    _IMPORT_ERROR = None
except Exception as exc:  # noqa: BLE001
    CosConfig = None
    CosS3Client = None
    CosClientError = Exception
    CosServiceError = Exception
    _IMPORT_ERROR = exc


def _pick_value(cli_value: str | None, env_names: list[str], field_name: str, required: bool) -> str:
    if cli_value:
        return cli_value
    for env_name in env_names:
        value = os.getenv(env_name)
        if value:
            return value
    if required:
        joined = ", ".join(env_names)
        raise ValueError(f"Missing {field_name}. Set CLI arg or env var: {joined}")
    return ""


def _normalize_key(path: Path, key: str | None) -> str:
    if key:
        normalized = key.strip().replace("\\", "/").lstrip("/")
        if normalized:
            return normalized
    return path.name


def _content_disposition(disposition_type: str, filename: str) -> str:
    encoded = quote(filename, safe="")
    return f"{disposition_type}; filename=\"{filename}\"; filename*=UTF-8''{encoded}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Upload local file to Tencent COS and generate presigned view/download URLs."
    )
    parser.add_argument(
        "--region",
        help="COS region, e.g. ap-guangzhou. Fallback env: COS_REGION",
    )
    parser.add_argument(
        "--bucket",
        help="Bucket name, e.g. my-bucket-1250000000. Fallback env: COS_BUCKET",
    )
    parser.add_argument("--file", required=True, help="Local file path to upload")
    parser.add_argument("--key", help="Object key in bucket. Default: local filename")
    parser.add_argument("--expires", type=int, default=3600, help="Presigned URL expiration in seconds")
    parser.add_argument("--scheme", default="https", choices=["https", "http"], help="Request scheme")

    parser.add_argument("--secret-id", help="Tencent Cloud SecretId")
    parser.add_argument("--secret-key", help="Tencent Cloud SecretKey")
    parser.add_argument("--session-token", help="Tencent Cloud session token (STS)")

    parser.add_argument(
        "--download-filename",
        help="Optional filename shown in browser download prompt",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if _IMPORT_ERROR is not None:
        print(
            "[ERROR] Missing Tencent COS SDK. Install with: pip install cos-python-sdk-v5",
            file=sys.stderr,
        )
        print(f"[ERROR] Import detail: {_IMPORT_ERROR}", file=sys.stderr)
        return 2

    local_path = Path(args.file).expanduser().resolve()
    if not local_path.exists() or not local_path.is_file():
        print(f"[ERROR] File not found: {local_path}", file=sys.stderr)
        return 2

    if args.expires <= 0:
        print("[ERROR] --expires must be > 0", file=sys.stderr)
        return 2

    try:
        region = _pick_value(args.region, ["COS_REGION"], "region", True)
        bucket = _pick_value(args.bucket, ["COS_BUCKET"], "bucket", True)
        secret_id = _pick_value(
            args.secret_id,
            ["COS_SECRET_ID"],
            "secret id",
            True,
        )
        secret_key = _pick_value(
            args.secret_key,
            ["COS_SECRET_KEY"],
            "secret key",
            True,
        )
        session_token = _pick_value(
            args.session_token,
            ["COS_SESSION_TOKEN"],
            "session token",
            False,
        )

        key = _normalize_key(local_path, args.key)
        config = CosConfig(
            Region=region,
            SecretId=secret_id,
            SecretKey=secret_key,
            Token=session_token or None,
            Scheme=args.scheme,
        )
        client = CosS3Client(config)

        upload_result = client.upload_file(
            Bucket=bucket,
            LocalFilePath=str(local_path),
            Key=key,
        )

        view_url = client.get_presigned_url(
            Method="GET",
            Bucket=bucket,
            Key=key,
            Expired=args.expires,
        )

        download_params = None
        if args.download_filename:
            download_params = {
                "response-content-disposition": _content_disposition(
                    "attachment",
                    args.download_filename,
                )
            }

        download_url = client.get_presigned_download_url(
            Bucket=bucket,
            Key=key,
            Expired=args.expires,
            Params=download_params,
        )

    except (ValueError, CosClientError, CosServiceError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Unexpected failure: {exc}", file=sys.stderr)
        return 1

    output = {
        "bucket": bucket,
        "region": region,
        "key": key,
        "local_file": str(local_path),
        "size_bytes": local_path.stat().st_size,
        "expires_in": args.expires,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "view_url": view_url,
        "download_url": download_url,
        "upload_result": upload_result,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
