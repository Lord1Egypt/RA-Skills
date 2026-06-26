import logging
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from bot.ig_config import R2_ACCESS_KEY, R2_BUCKET, R2_ENDPOINT, R2_PUBLIC_URL, R2_SECRET_KEY

logger = logging.getLogger(__name__)


def _get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=R2_ENDPOINT,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
    )


def upload_to_r2(file_path: Path, max_retries: int = 2) -> str:
    client = _get_s3_client()
    key = file_path.name

    for attempt in range(1, max_retries + 1):
        try:
            logger.info("Uploading %s to R2 (attempt %d/%d)", key, attempt, max_retries)
            client.upload_file(
                str(file_path),
                R2_BUCKET,
                key,
                ExtraArgs={"ContentType": "video/mp4"},
            )
            public_url = f"{R2_PUBLIC_URL.rstrip('/')}/{key}"
            logger.info("Upload successful: %s", public_url)
            return public_url
        except ClientError as e:
            logger.error("Upload attempt %d failed: %s", attempt, e)
            if attempt == max_retries:
                raise

    raise RuntimeError("Upload failed after all retries")
