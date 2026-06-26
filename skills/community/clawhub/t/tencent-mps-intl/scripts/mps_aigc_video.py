#!/usr/bin/env python3
"""
Tencent Cloud MPS AIGC Intelligent Video Generation Script

Features:
  Uses MPS AIGC intelligent content creation to generate video results
  from input text, images, video, and other content.
  Aggregates capabilities from multiple large models (Hunyuan / Hailuo / Kling / Vidu / OS / GV / Mingmou / PixVerse),
  providing a one-stop API integration.
  Wraps the CreateAigcVideoTask + DescribeAigcVideoTask APIs,
  supporting task creation + automatic polling for results.

Supported Models:
  - Hunyuan (Tencent Hunyuan)
  - Hailuo (version 02 / 2.3 / 2.3-fast)
  - Kling (version 1.6 / 2.0 / 2.1 / 2.5 / O1 / 2.6 / 3.0 / 3.0-Omni)
  - Vidu (version q2 / q2-pro / q2-turbo / q3 / q3-pro / q3-turbo / q3-mix)
  - OS (version 2.0)
  - GV (version 3.1 / 3.1-fast)
  - PixVerse (version v5.6 / v6 / c1, duration 1~15s, supports 8 aspect ratios + quality 360p/540p/720p/1080p)

Core Capabilities:
  - Text-to-Video: Generate video from a text description
  - Image-to-Video: Generate video from a first-frame image + text description
  - First/Last Frame Video: Generate video from specified first and last frame images (supported by select models)
  - Multi-image Reference Video (GV/Vidu): Up to 3 reference images
  - Reference Video Generation (Kling): Edit or reference features from a source video
  - Special Effects Scenes (Kling motion control / Mingmou landscape to portrait / Vidu effect templates, etc.)
  - Storyboard Generation (Kling exclusive): Supports single and multi-shot automatic generation
  - Custom duration, resolution, and aspect ratio
  - Watermark control, audio generation, and background music
  - Store results to COS

COS Storage Configuration (optional):
  Specify the bucket via --cos-bucket-name / --cos-bucket-region / --cos-bucket-path parameters,
  or via the TENCENTCLOUD_COS_BUCKET / TENCENTCLOUD_COS_REGION environment variables.
  If not configured, MPS default temporary storage is used (videos stored for 12 hours, pre-signed link);
  if configured, videos are written to your COS bucket (permanent), and the script auto-generates a 24-hour signed link.

Usage:
  # Text-to-video: simplest usage (Hunyuan model)
  python mps_aigc_video.py --prompt "A cute orange cat stretching in the sunlight"

  # Specify model and version
  python mps_aigc_video.py --prompt "Cyberpunk city at night" --model Kling --model-version 2.5

  # Image-to-video: first-frame image + description
  python mps_aigc_video.py --prompt "Bring the scene to life" \
      --image-url https://example.com/photo.jpg

  # Kling storyboard: single shot (automatic intelligent splitting)
  python mps_aigc_video.py --prompt "Travel diary capturing beautiful moments" --model Kling --multi-shot

  # Kling storyboard: multi-shot (custom per-shot prompts)
  python mps_aigc_video.py --model Kling --multi-shot --duration 12 \
      --multi-prompts-json '[
        {"index": 1, "prompt": "City skyline viewed from a hotel window at sunrise", "duration": "3"},
        {"index": 2, "prompt": "Enjoying breakfast at a cafe, pedestrians outside the window", "duration": "4"},
        {"index": 3, "prompt": "Walking in the park, sunlight filtering through the leaves", "duration": "5"}
      ]'

  # First/last frame video (GV / Kling 2.1 / Vidu q2-pro)
  python mps_aigc_video.py --prompt "Transition animation" --model GV \
      --image-url https://example.com/start.jpg \
      --last-image-url https://example.com/end.jpg

  # GV multi-image reference (up to 3 images, specify asset/style)
  python mps_aigc_video.py --prompt "Blend elements" --model GV \
      --ref-image-url https://example.com/img1.jpg --ref-image-type asset \
      --ref-image-url https://example.com/img2.jpg --ref-image-type style

  # Kling O1 reference video (source video to edit + preserve original audio)
  python mps_aigc_video.py --prompt "Stylize the video" --model Kling --model-version O1 \
      --ref-video-url https://example.com/video.mp4 --ref-video-type base --keep-original-sound yes

  # Mingmou landscape to portrait
  python mps_aigc_video.py --prompt "Landscape to portrait conversion" --model Mingmou --scene-type land2port

  # Specify duration, resolution, and aspect ratio
  python mps_aigc_video.py --prompt "Sunrise time-lapse" --model Kling --duration 10 \
      --resolution 1080P --aspect-ratio 16:9

  # Kling motion control scene
  python mps_aigc_video.py --prompt "Character walking" --model Kling --scene-type motion_control

  # Remove watermark + generate audio + background music
  python mps_aigc_video.py --prompt "Product showcase" --model Kling \
      --no-logo --enable-audio true --enable-bgm

  # Vidu off-peak mode (generated within 48 hours)
  python mps_aigc_video.py --prompt "Natural scenery" --model Vidu --off-peak

  # Additional parameters (JSON format, e.g., camera control)
  python mps_aigc_video.py --prompt "Fly over the city" --model Kling \
      --additional-params '{"camera_control":{"type":"simple"}}'

  # Store to COS
  python mps_aigc_video.py --prompt "Promotional video" \
      --cos-bucket-name mybucket-125xxx --cos-bucket-region ap-guangzhou

  # Create task only (do not wait for result)
  python mps_aigc_video.py --prompt "Time-lapse photography" --no-wait

  # Query an existing task result
  python mps_aigc_video.py --task-id 1234567890-xxxxxxxxxxxxx

  # Dry run (print request parameters only, do not call the API)
  python mps_aigc_video.py --prompt "Test video" --dry-run

Environment Variables:
  TENCENTCLOUD_SECRET_ID   - Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  - Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET       - COS bucket name (optional, for result storage)
  TENCENTCLOUD_COS_REGION       - COS bucket region (default: ap-guangzhou)
"""

import argparse
import json
import os
import sys
from mps_auto_upgrade import check_sdk_version
import time

check_sdk_version()
try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.mps.v20190612 import mps_client, models
except ImportError:
    print("Error: Please install the Tencent Cloud SDK first: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)

# COS SDK (optional, for generating temporary URLs)
try:
    from qcloud_cos import CosConfig, CosS3Client
    _COS_SDK_AVAILABLE = True
except ImportError:
    _COS_SDK_AVAILABLE = False

# =============================================================================
# Model Information
# =============================================================================
SUPPORTED_MODELS = {
    "Hunyuan": {
        "description": "Tencent Hunyuan large model",
        "versions": [],
        "duration_options": [],
        "default_duration": None,
        "supports_multishot": False,
    },
    "Hailuo": {
        "description": "Hailuo video model",
        "versions": ["02", "2.3", "2.3-fast"],
        "duration_options": [6, 10],
        "default_duration": 6,
        "supports_multishot": False,
    },
    "Kling": {
        "description": "Kling video model",
        "versions": ["1.6", "2.0", "2.1", "2.5", "O1", "2.6", "3.0", "3.0-Omni"],
        "duration_options": [5, 10],
        "default_duration": 5,
        "supports_multishot": True,  # supports storyboard
    },
    "Vidu": {
        "description": "Vidu video model",
        "versions": ["q2", "q2-pro", "q2-turbo", "q3", "q3-pro", "q3-turbo", "q3-mix"],
        "duration_options": list(range(1, 11)),
        "default_duration": 4,
        "supports_multishot": False,
    },
    "OS": {
        "description": "OS video model",
        "versions": ["2.0"],
        "duration_options": [4, 8, 12],
        "default_duration": 8,
        "supports_multishot": False,
    },
    "GV": {
        "description": "GV video model",
        "versions": ["3.1", "3.1-fast"],
        "duration_options": [8],
        "default_duration": 8,
        "supports_multishot": False,
    },
    "Mingmou": {
        "description": "Mingmou landscape-to-portrait model",
        "versions": [],
        "duration_options": [],
        "default_duration": None,
        "supports_multishot": False,
    },
    "PixVerse": {
        "description": "PixVerse video model (v5.6 / v6 / c1)",
        "versions": ["v5.6", "v6", "c1"],
        "duration_options": list(range(1, 16)),  # 1~15 seconds
        "default_duration": 5,
        "supports_multishot": False,
        "aspect_ratios": ["16:9", "4:3", "1:1", "3:4", "9:16", "2:3", "3:2", "21:9"],
        "quality_options": ["360p", "540p", "720p", "1080p"],
        "default_quality": "540p",
    },
}

# Scene types
SCENE_TYPES = {
    "motion_control": "Kling — Motion Control",
    "land2port": "Mingmou — Landscape to Portrait",
    "template_effect": "Vidu — Effect Template",
    "3d_scene": "Hunyuan — 3D Scene (auto-applies ModelVersion=3d_2.0)",
}

# =============================================================================
# COS Temporary URL Generation
# =============================================================================


def get_cos_presigned_url(bucket: str, region: str, key: str,
                          secret_id: str = None, secret_key: str = None,
                          expired: int = 3600) -> str:
    """
    Generate a COS temporary access URL (pre-signed URL).

    Args:
        bucket: COS bucket name
        region: COS bucket region
        key: COS object key
        secret_id: Tencent Cloud SecretId (defaults to environment variable)
        secret_key: Tencent Cloud SecretKey (defaults to environment variable)
        expired: URL validity period in seconds (default: 3600, i.e., 1 hour)

    Returns:
        Pre-signed URL, or None on failure
    """
    if not _COS_SDK_AVAILABLE:
        print("Warning: COS SDK is not installed; cannot generate temporary URL. Install with: pip install cos-python-sdk-v5",  # NOCA:line-too-long(line cannot be shortened)
              file=sys.stderr)
        return None

    secret_id = secret_id or os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = secret_key or os.environ.get("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        print("Warning: Tencent Cloud credentials are missing; cannot generate temporary URL", file=sys.stderr)
        return None

    try:
        config = CosConfig(
            Region=region,
            SecretId=secret_id,
            SecretKey=secret_key
        )
        client = CosS3Client(config)

        url = client.get_presigned_url(
            Method='GET',
            Bucket=bucket,  # NOCA:E302(function structure required for CLI)
            Key=key,
            Expired=expired  # NOCA:broad-except(intentional)
        )
        return url
    except Exception as e:  # NOCA:broad-except(CLI script needs to handle all exceptions)
        print(f"Warning: Failed to generate temporary URL: {e}", file=sys.stderr)
        return None


def upload_to_cos(local_path: str, bucket: str, region: str,
                  cos_key: str = None,
                  secret_id: str = None, secret_key: str = None) -> str:
    """
    Upload a local file to COS and return a presigned URL.

    Args:
        local_path: Local file path
        bucket: COS Bucket name
        region: COS Region
        cos_key: Target key (auto-generated as aigc_input/{timestamp}_{filename} if not provided)
        secret_id/secret_key: Tencent Cloud credentials (default: read from environment variables)

    Returns:
        Presigned URL (valid for 1 hour); calls sys.exit(1) on failure
    """
    import uuid as _uuid

    if not _COS_SDK_AVAILABLE:
        print("❌ Error: COS SDK is not installed; cannot upload local file. Install with: pip install cos-python-sdk-v5",
              file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(local_path):
        print(f"❌ Error: Local file does not exist: {local_path}", file=sys.stderr)
        sys.exit(1)

    ext = os.path.splitext(local_path)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        print(f"❌ Error: Unsupported image format {ext}; supported formats: jpeg/png/webp/gif", file=sys.stderr)
        sys.exit(1)

    secret_id = secret_id or os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = secret_key or os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print("❌ Error: Uploading local files requires TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
        sys.exit(1)

    if not cos_key:
        ts = int(time.time())
        uid = str(_uuid.uuid4())[:8]
        filename = os.path.basename(local_path)
        cos_key = f"aigc_input/{ts}_{uid}_{filename}"

    cos_key = cos_key.lstrip("/")

    try:
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
        client = CosS3Client(config)
        print(f"⬆️  Uploading local file to COS: {local_path} → {bucket}/{cos_key}", file=sys.stderr)
        client.upload_file(
            Bucket=bucket,
            LocalFilePath=local_path,
            Key=cos_key,
            PartSize=10,
            MAXThread=5,
            EnableMD5=False
        )
    except Exception as e:  # NOCA:broad-except(CLI script needs to handle all exceptions)
        print(f"❌ COS upload failed: {e}", file=sys.stderr)
        sys.exit(1)

    url = get_cos_presigned_url(bucket, region, cos_key, secret_id, secret_key, expired=3600)
    if not url:
        url = f"https://{bucket}.cos.{region}.myqcloud.com/{cos_key}"
        print(f"⚠️  Presigning failed; using public URL (bucket must have public-read ACL): {url}", file=sys.stderr)
    else:
        print(f"✅ Upload successful; presigned URL generated", file=sys.stderr)
    return url


def resolve_cos_input(cos_bucket: str, cos_region: str, cos_key: str,  # NOCA:E302(function structure required for CLI)
                      secret_id: str = None, secret_key: str = None) -> str:
    """
    Resolve a COS path to an accessible URL.

    Args:
        cos_bucket: COS bucket name
        cos_region: COS bucket region
        cos_key: COS object key
        secret_id: Tencent Cloud SecretId
        secret_key: Tencent Cloud SecretKey

    Returns:
        Accessible URL (pre-signed URL or permanent URL)
    """
    if not cos_bucket or not cos_region or not cos_key:
        return None

    # Attempt to generate a pre-signed URL
    presigned_url = get_cos_presigned_url(cos_bucket, cos_region, cos_key,
                                          secret_id, secret_key)
    if presigned_url:
        return presigned_url

    # Fall back to a permanent URL if generation fails (may not be accessible)
    return f"https://{cos_bucket}.cos.{cos_region}.myqcloud.com/{cos_key.lstrip('/')}"


def ensure_signed_url(url: str, expired: int = 86400) -> tuple:
    """
    If the URL is a bare COS URL (starts with http(s):// but has no query string),
    automatically re-sign it as a temporary signed URL.
    For other cases (not a URL / already signed / non-COS host / signing failed),
    return the URL unchanged.

    Returns:
        (final_url, status):
            status ∈ {
                'not_url':         not a URL (None/empty/not http(s))
                'already_signed':  URL has query parameters (e.g., MPS default hosting)
                'auto_signed':     bare COS URL successfully re-signed (BYO bucket mode)
                'sign_failed':     bare COS URL but signing failed (missing SDK / wrong key)
                'not_cos':         http URL but not a COS host (3rd-party CDN, etc.)
            }
    """
    if not url or not isinstance(url, str):
        return url, 'not_url'
    if not url.startswith(("http://", "https://")):
        return url, 'not_url'
    # Already signed: any query parameters are treated as signed
    # (compatible with q-sign / token / KSS / X-Amz, etc.)
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if parsed.query:
        return url, 'already_signed'
    # Parse bare COS URL: https://<bucket>.cos.<region>.myqcloud.com/<key>
    import re
    m = re.match(
        r"https?://([\w\-]+)\.cos\.([\w\-]+)\.(?:myqcloud\.com|tencentcos\.cn)/(.+)",
        url,
    )
    if not m:
        return url, 'not_cos'
    bucket, region, key = m.group(1), m.group(2), m.group(3)
    signed = get_cos_presigned_url(bucket, region, key, expired=expired)
    if signed and '?' in signed:
        return signed, 'auto_signed'
    return url, 'sign_failed'


def print_storage_hint(statuses: list):
    """Print the storage/expiry hint based on a list of ensure_signed_url statuses."""
    if not statuses:
        return
    modes = set(statuses)
    if modes == {'already_signed'}:
        # All MPS default hosting (platform pre-signed)
        print("\n⚠️  MPS temporary storage. Links are valid for 12 hours. Please download promptly.")
    elif 'auto_signed' in modes and 'sign_failed' not in modes:
        # BYO bucket + all successfully re-signed
        print("\n💡 Videos are stored in your COS bucket (permanent); a 24-hour temporary signed link has been auto-generated. Please re-sign after expiry.")  # NOCA:line-too-long
    elif 'sign_failed' in modes:
        # At least one signing failure
        print("\n⚠️  Videos are stored in your COS bucket, but temporary signing failed (please check cos-python-sdk-v5 and TENCENTCLOUD_SECRET_ID/KEY);")  # NOCA:line-too-long
        print("    if the bucket has private read ACL, you must sign manually before access.")
    elif modes == {'not_cos'}:
        print("\n💡 Video URLs are provided by a third-party origin; expiry follows the origin's policy.")
    else:
        # Mixed or unrecognized — give a conservative hint
        print("\n💡 Video links may come from different sources. Please verify their validity as needed.")


# Polling configuration
DEFAULT_POLL_INTERVAL = 10   # seconds (video generation is slow)
DEFAULT_MAX_WAIT = 1800       # maximum wait time: 30 minutes


def get_cos_bucket():
    """Get the COS Bucket name from environment variables."""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")

def get_cos_region():  # NOCA:E302(function structure required for CLI)
    """Get the COS Bucket region from environment variables, default is ap-guangzhou."""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "ap-guangzhou")

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False


def get_credentials():
    """Get Tencent Cloud credentials from environment variables. If missing, attempt to auto-load from system files and retry."""  # NOCA:line-too-long(line cannot be shortened)
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        # Attempt to auto-load from system environment variable files
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] Environment variables not set, attempting to auto-load from system files...", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from mps_load_env import _print_setup_hint, _TARGET_VARS
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print(
                    "\nError: TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY is not set.\n"
                    "Please add these variables to /etc/environment, ~/.profile, or similar files.\n",
                    file=sys.stderr,
                )
            sys.exit(1)
    return credential.Credential(secret_id, secret_key)

def create_mps_client(cred, region):  # NOCA:E302(function structure required for CLI)
    """Create an MPS client."""
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    http_profile.reqMethod = "POST"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return mps_client.MpsClient(cred, region, client_profile)


def build_multishot_params(args):
    """
    Build multi-shot parameters (only supported by the Kling model)

    Rules:
    - Single-shot mode: multi_shot=true, shot_type=intelligence, multi_prompt not specified
    - Multi-shot mode: multi_shot=true, shot_type=intelligence, multi_prompt is an array
    - In multi-shot mode, the ModelVersion parameter is required (value is 3.0 or 3.0-Omni), set by the caller in the
    top-level params

    Args:
        args: command-line arguments

    Returns:
        Multi-shot parameter dict, or None on failure
    """
    if not args.multi_shot:
        return None

    # Multi-shot feature is only supported by the Kling model
    if args.model != "Kling":
        print(f"❌ Error: Multi-shot feature currently only supports the Kling model", file=sys.stderr)
        return None

    multishot_params = {
        "multi_shot": True,  # Note: it's multi_shot, not multi_shots
        "shot_type": "intelligence"  # Both single-shot and multi-shot use "intelligence"
    }

    # If a multi-shot JSON configuration is provided
    if args.multi_prompts_json:
        try:
            multi_prompts = json.loads(args.multi_prompts_json)
        except json.JSONDecodeError as e:
            print(f"❌ Error: --multi-prompts-json must be valid JSON format: {e}", file=sys.stderr)
            return None

        # Validate multi-shot configuration and get the computed total duration
        total_shots_duration = validate_multi_prompts(multi_prompts, args.duration, parser=None)
        if total_shots_duration is None:
            return None  # Validation failed

        # Ensure the duration field is an integer type (required by the API)
        for shot in multi_prompts:
            if isinstance(shot.get("duration"), str):
                shot["duration"] = int(shot["duration"])

        # multi_prompt as an array object (not a JSON string)
        multishot_params["multi_prompt"] = multi_prompts

        # If the user did not specify a total duration, automatically use the sum of shot durations
        if args.duration is None:
            print(f"ℹ️  Total duration not specified, automatically set to the sum of shot durations: {total_shots_duration} seconds")  # NOCA:line-too-long(line cannot be shortened)
            multishot_params["duration"] = total_shots_duration
    # Otherwise use single-shot mode (multi_prompt not specified, system splits automatically)
    # In this case only multi_shot=True and shot_type=intelligence are set

    return multishot_params
def validate_multi_prompts(multi_prompts, total_duration, parser=None):  # NOCA:E302(function structure required for CLI)  # NOCA:line-too-long(line cannot be shortened)
    """
    Validate multi-shot configuration

    Args:
        multi_prompts: list of shot configurations
        total_duration: total duration
        parser: ArgumentParser object (for error messages)

    Returns:
        Returns True if validation passes, otherwise returns False
    """
    if not isinstance(multi_prompts, list):
        print("❌ Error: multi_prompt must be in array format", file=sys.stderr)
        return False

    if len(multi_prompts) == 0:
        print("❌ Error: multi_prompt cannot be empty", file=sys.stderr)
        return False

    if len(multi_prompts) > 6:
        print("❌ Error: a maximum of 6 shots are supported, currently {} shots are configured".format(len(multi_prompts)), file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
        return False

    if len(multi_prompts) < 1:
        print("❌ Error: at least 1 shot is required", file=sys.stderr)
        return False

    # Check the format of each shot
    for i, shot in enumerate(multi_prompts):
        if not isinstance(shot, dict):
            print(f"❌ Error: shot {i+1} must be in object format", file=sys.stderr)
            return False

        # Check required fields
        if "index" not in shot:
            print(f"❌ Error: shot {i+1} is missing the index field", file=sys.stderr)
            return False
        if "prompt" not in shot:
            print(f"❌ Error: shot {i+1} is missing the prompt field", file=sys.stderr)
            return False
        if "duration" not in shot:
            print(f"❌ Error: shot {i+1} is missing the duration field", file=sys.stderr)
            return False

        # Check field types
        if not isinstance(shot["index"], int):
            print(f"❌ Error: the index of shot {i+1} must be an integer", file=sys.stderr)
            return False
        if not isinstance(shot["prompt"], str):
            print(f"❌ Error: the prompt of shot {i+1} must be a string", file=sys.stderr)
            return False
        if not isinstance(shot["duration"], (int, str)):
            print(f"❌ Error: the duration of shot {i+1} must be a number", file=sys.stderr)
            return False

        # Check prompt length
        if len(shot["prompt"]) > 512:
            print(f"❌ Error: the prompt of shot {i+1} cannot exceed 512 characters (current: {len(shot['prompt'])} characters)", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
            return False

        # Check duration range
        try:
            duration = int(shot["duration"])
            if duration < 1:
                print(f"❌ Error: the duration of shot {i+1} cannot be less than 1 second (current: {duration} seconds)", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
                return False
            # Check that the shot duration does not exceed the total duration
            if total_duration is not None and duration > total_duration:
                print(f"❌ Error: the duration of shot {i+1} ({duration} seconds) cannot exceed the total duration ({total_duration} seconds)", file=sys.stderr)  # NOCA:line-too-long(line cannot be shortened)
                return False
        except ValueError:
            print(f"❌ Error: the duration of shot {i+1} must be a valid number", file=sys.stderr)
            return False

    # Calculate the sum of all shot durations
    total_shots_duration = sum(int(shot["duration"]) for shot in multi_prompts)

    # Check whether the duration equals the total duration (only validated when total_duration is specified)
    if total_duration is not None and total_shots_duration != total_duration:
        print(f"❌ Error: the sum of all shot durations ({total_shots_duration} seconds) must equal the total duration ({total_duration} seconds)", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
        return False

    # Return the total duration (for automatic setting)
    return total_shots_duration


def build_create_params(args):
    """Build CreateAigcVideoTask request parameters."""
    params = {}

    # Model name (required)
    params["ModelName"] = args.model

    # Model version (optional)
    if args.model_version:
        params["ModelVersion"] = args.model_version

    # Scene type (optional)
    if args.scene_type:
        params["SceneType"] = args.scene_type

    # Prompt
    if args.prompt:
        params["Prompt"] = args.prompt

    # Negative prompt
    if args.negative_prompt:
        params["NegativePrompt"] = args.negative_prompt

    # Prompt enhancement
    if args.enhance_prompt:
        params["EnhancePrompt"] = True

    # First frame image (simple mode) - supports URL, COS path, or local file
    if args.image_url:
        params["ImageUrl"] = args.image_url
    elif args.image_cos_key:
        # CreateAigcVideoTask does not support CosInputInfo; generate a presigned URL and pass as ImageUrl
        bucket = args.image_cos_bucket or get_cos_bucket()
        region = args.image_cos_region or get_cos_region()
        if not bucket:
            print("❌ Error: --image-cos-bucket must be specified or environment variable set when using --image-cos-key", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
            sys.exit(1)
        key = args.image_cos_key.lstrip("/")
        url = get_cos_presigned_url(bucket, region, key)
        if not url:
            url = f"https://{bucket}.cos.{region}.myqcloud.com/{key}"
            print(f"⚠️  COS presigning failed; using public URL (bucket must have public-read ACL): {url}", file=sys.stderr)
        params["ImageUrl"] = url
    elif getattr(args, 'image_local', None):
        # Local file: upload to COS then pass as ImageUrl
        upload_bucket = args.cos_bucket_name or get_cos_bucket()
        upload_region = args.cos_bucket_region or get_cos_region()
        if not upload_bucket:
            print("❌ Error: --image-local requires a COS Bucket (--cos-bucket-name or TENCENTCLOUD_COS_BUCKET)", file=sys.stderr)
            sys.exit(1)
        params["ImageUrl"] = upload_to_cos(args.image_local, upload_bucket, upload_region)

    # Last frame image - supports URL, COS path, or local file
    if args.last_image_url:
        params["LastImageUrl"] = args.last_image_url
    elif args.last_image_cos_key:
        # CreateAigcVideoTask does not support LastImageCosInputInfo; generate a presigned URL and pass as LastImageUrl
        bucket = args.last_image_cos_bucket or get_cos_bucket()
        region = args.last_image_cos_region or get_cos_region()
        if not bucket:
            print("❌ Error: --last-image-cos-bucket must be specified or environment variable set when using --last-image-cos-key", file=sys.stderr)  # NOCA:line-too-long(line cannot be shortened)
            sys.exit(1)
        key = args.last_image_cos_key.lstrip("/")
        url = get_cos_presigned_url(bucket, region, key)
        if not url:
            url = f"https://{bucket}.cos.{region}.myqcloud.com/{key}"
            print(f"⚠️  COS presigning failed; using public URL (bucket must have public-read ACL): {url}", file=sys.stderr)
        params["LastImageUrl"] = url
    elif getattr(args, 'last_image_local', None):
        # Local file: upload to COS then pass as LastImageUrl
        upload_bucket = args.cos_bucket_name or get_cos_bucket()
        upload_region = args.cos_bucket_region or get_cos_region()
        if not upload_bucket:
            print("❌ Error: --last-image-local requires a COS Bucket (--cos-bucket-name or TENCENTCLOUD_COS_BUCKET)", file=sys.stderr)
            sys.exit(1)
        params["LastImageUrl"] = upload_to_cos(args.last_image_local, upload_bucket, upload_region)

    # Multi-image reference (Image Infos) - supports URL or COS path
    image_infos = []
    ref_types = args.ref_image_type or []
    # 1. Process directly passed URLs
    if args.ref_image_url:
        for i, url in enumerate(args.ref_image_url):
            info = {"ImageUrl": url}
            if i < len(ref_types):
                info["ReferenceType"] = ref_types[i]
            image_infos.append(info)

    # 2. COS path input: generate presigned URL then pass as ImageUrl
    # Note: CreateAigcVideoTask ImageInfos does not support CosInputInfo
    if args.ref_image_cos_key:
        cos_buckets = args.ref_image_cos_bucket or []
        cos_regions = args.ref_image_cos_region or []

        for i, key in enumerate(args.ref_image_cos_key):
            bucket = cos_buckets[i] if i < len(cos_buckets) else (cos_buckets[0] if cos_buckets else get_cos_bucket())
            region = cos_regions[i] if i < len(cos_regions) else (cos_regions[0] if cos_regions else get_cos_region())

            if not bucket:
                print(f"❌ Error: --ref-image-cos-key[{i}] is missing the corresponding bucket", file=sys.stderr)
                sys.exit(1)

            url = get_cos_presigned_url(bucket, region, key.lstrip("/"))
            if not url:
                url = f"https://{bucket}.cos.{region}.myqcloud.com/{key.lstrip('/')}"
                print(f"⚠️  ref-image-cos-key[{i}] presigning failed; using public URL (bucket must have public-read ACL): {url}", file=sys.stderr)

            info = {"ImageUrl": url}
            url_idx = len(args.ref_image_url) if args.ref_image_url else 0
            ref_type_idx = url_idx + i
            if ref_type_idx < len(ref_types):
                info["ReferenceType"] = ref_types[ref_type_idx]
            image_infos.append(info)

    if image_infos:
        params["ImageInfos"] = image_infos

    # 3. Local file input (multi-image reference): upload to COS then pass as ImageUrl
    if getattr(args, 'ref_image_local', None):
        upload_bucket = args.cos_bucket_name or get_cos_bucket()
        upload_region = args.cos_bucket_region or get_cos_region()
        if not upload_bucket:
            print("❌ Error: --ref-image-local requires a COS Bucket (--cos-bucket-name or TENCENTCLOUD_COS_BUCKET)", file=sys.stderr)
            sys.exit(1)
        url_count = len(args.ref_image_url) if args.ref_image_url else 0
        cos_count = len(args.ref_image_cos_key) if args.ref_image_cos_key else 0
        ref_types_local = args.ref_image_type or []
        for i, local_path in enumerate(args.ref_image_local):
            url = upload_to_cos(local_path, upload_bucket, upload_region)
            info = {"ImageUrl": url}
            ref_type_idx = url_count + cos_count + i
            if ref_type_idx < len(ref_types_local):
                info["ReferenceType"] = ref_types_local[ref_type_idx]
            image_infos.append(info)
        params["ImageInfos"] = image_infos

    # Reference video (Video Infos) - supports URL or COS path
    # Note: AigcVideoReferenceVideoInfo does not support CosInputInfo; COS paths must be converted to pre-signed URLs
    video_infos = []
    ref_types = args.ref_video_type or []
    keep_sounds = args.keep_original_sound or []

    # 1. Process directly passed URLs
    if args.ref_video_url:
        for i, url in enumerate(args.ref_video_url):
            info = {"VideoUrl": url}
            if i < len(ref_types):
                info["ReferType"] = ref_types[i]
            if i < len(keep_sounds):
                info["KeepOriginalSound"] = keep_sounds[i]
            video_infos.append(info)
    
    # 2. Process COS path input - generate pre-signed URL and fill into VideoUrl
    if args.ref_video_cos_key:
        cos_buckets = args.ref_video_cos_bucket or []
        cos_regions = args.ref_video_cos_region or []
        secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
        secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
        
        for i, key in enumerate(args.ref_video_cos_key):
            bucket = cos_buckets[i] if i < len(cos_buckets) else (cos_buckets[0] if cos_buckets else get_cos_bucket())
            region = cos_regions[i] if i < len(cos_regions) else (cos_regions[0] if cos_regions else get_cos_region())

            if not bucket:
                print(f"❌ Error: --ref-video-cos-key[{i}] is missing the corresponding bucket", file=sys.stderr)
                sys.exit(1)
            
            # Generate a pre-signed URL and fill into VideoUrl (AigcVideoReferenceVideoInfo does not support CosInputInfo)
            presigned_url = resolve_cos_input(bucket, region, key, secret_id, secret_key)
            if not presigned_url:
                print(f"❌ Error: Failed to generate pre-signed URL for --ref-video-cos-key[{i}]", file=sys.stderr)
                sys.exit(1)
            
            info = {"VideoUrl": presigned_url}
            url_idx = len(args.ref_video_url) if args.ref_video_url else 0
            ref_type_idx = url_idx + i
            keep_sound_idx = url_idx + i
            if ref_type_idx < len(ref_types):
                info["ReferType"] = ref_types[ref_type_idx]
            if keep_sound_idx < len(keep_sounds):
                info["KeepOriginalSound"] = keep_sounds[keep_sound_idx]
            video_infos.append(info)

    if video_infos:
        params["VideoInfos"] = video_infos
    # Duration
    if args.duration is not None:
        params["Duration"] = args.duration

    # Storyboard parameters (Additional Parameters)
    multishot_params = build_multishot_params(args)
    if multishot_params:
        # In multi-storyboard mode, Model Version is required (value must be 3.0 or 3.0-Omni)
        if not params.get("ModelVersion"):
            params["ModelVersion"] = "3.0-Omni"
            print(f"ℹ️  Auto-set ModelVersion in multi-storyboard mode: {params['ModelVersion']}")
        # Extract duration to top-level parameter (if present)
        if "duration" in multishot_params:
            duration_value = multishot_params.pop("duration")
            # Prefer user-specified duration
            if params.get("Duration") is None:
                params["Duration"] = duration_value

        # Storyboard parameters need to be merged into Additional Parameters
        # Note: Additional Parameters remains a dict structure; the SDK will automatically serialize it to a JSON string
        if args.additional_params:
            try:
                # Parse user-provided additional_params
                existing_additional = json.loads(args.additional_params)
                # Merge storyboard parameters
                existing_additional.update(multishot_params)
                # Use dict structure directly (SDK's from_json_string will auto-serialize)
                params["AdditionalParameters"] = existing_additional
            except json.JSONDecodeError:
                print("❌ Error: --additional-params must be valid JSON format", file=sys.stderr)
                sys.exit(1)
        else:
            # No user-provided additional_params, use storyboard parameters directly (dict structure)
            params["AdditionalParameters"] = multishot_params
    # Extra parameters (Extra Parameters)
    extra = {}
    if args.resolution:
        extra["Resolution"] = args.resolution
    if args.aspect_ratio:
        extra["AspectRatio"] = args.aspect_ratio
    if args.no_logo:
        extra["LogoAdd"] = 0
    if args.enable_audio is not None:
        # Convert string to boolean
        extra["EnableAudio"] = args.enable_audio.lower() in ["true", "1", "yes"]
    if args.off_peak:
        extra["OffPeak"] = True
    if args.enable_bgm:
        extra["EnableBgm"] = True
    # PixVerse-specific parameters — unified into ExtraParameters
    # - quality: video quality (360p/540p/720p/1080p)
    # - generate_audio: whether to generate sound effects (mapped to ExtraParameters.EnableAudio;
    #   MPS backend translates this into PixVerse's native `generate_audio_switch`)
    # PixVerse reference: https://docs.platform.pai.video/300925802e0
    if args.model == "PixVerse":
        if args.quality:
            extra["Quality"] = args.quality
        if args.generate_audio is not None:
            extra["EnableAudio"] = (args.generate_audio.lower() == "true")
    if extra:
        params["ExtraParameters"] = extra

    # COS storage
    cos_param = build_store_cos_param(args)
    if cos_param:
        params["StoreCosParam"] = cos_param

    # Additional parameters (Additional Parameters)
    # Note: If storyboard parameters exist, they have already been merged and handled in the block above
    # Only in non-storyboard mode does additional_params need to be set separately here
    if args.additional_params and not multishot_params:
        try:
            # Parse as dict structure, do not use the string directly
            params["AdditionalParameters"] = json.loads(args.additional_params)
        except json.JSONDecodeError as e:
            print(f"❌ Error: --additional-params must be valid JSON format: {e}", file=sys.stderr)
            sys.exit(1)

    # Operator
    if args.operator:
        params["Operator"] = args.operator

    return params

def build_store_cos_param(args):  # NOCA:E302(function structure required for CLI)
    """Build COS storage parameters."""
    bucket_name = args.cos_bucket_name or get_cos_bucket()
    bucket_region = args.cos_bucket_region or get_cos_region()

    if not bucket_name:
        return None

    cos_param = {
        "CosBucketName": bucket_name,
        "CosBucketRegion": bucket_region,
    }
    if args.cos_bucket_path:
        cos_param["CosBucketPath"] = args.cos_bucket_path

    return cos_param


def create_aigc_video_task(client, params):
    """Call the CreateAigc_video_task API to create a video generation task."""
    req = models.CreateAigcVideoTaskRequest()


    # Additional Parameters must be a JSON string and needs to be serialized first
    if "AdditionalParameters" in params and isinstance(params["AdditionalParameters"], dict):
        params["AdditionalParameters"] = json.dumps(params["AdditionalParameters"], ensure_ascii=False)

    req.from_json_string(json.dumps(params))
    resp = client.CreateAigcVideoTask(req)
    return json.loads(resp.to_json_string())

def describe_aigc_video_task(client, task_id):  # NOCA:E302(function structure required for CLI)
    """Call the DescribeAigcVideoTask API to query task status."""
    req = models.DescribeAigcVideoTaskRequest()
    req.from_json_string(json.dumps({"TaskId": task_id}))
    resp = client.DescribeAigcVideoTask(req)
    return json.loads(resp.to_json_string())


def poll_task_result(client, task_id, poll_interval, max_wait):
    """Poll and wait for task completion."""
    elapsed = 0


    while elapsed < max_wait:
        result = describe_aigc_video_task(client, task_id)
        status = result.get("Status", "")

        if status == "DONE":
            return result
        elif status == "FAIL":
            message = result.get("Message", "Unknown error")
            print(f"\n❌ Task failed: {message}", file=sys.stderr)
            sys.exit(1)

        # Print progress
        status_text = {"WAIT": "Waiting", "RUN": "Running"}.get(status, status)
        print(f"\r⏳ Task status: {status_text} (elapsed {elapsed}s / max {max_wait}s)", end="", flush=True)

        time.sleep(poll_interval)
        elapsed += poll_interval

    print(f"\n⚠️  Wait timed out (elapsed {max_wait}s), task is still in progress.", file=sys.stderr)
    print(f"   Please query the result later using --task-id {task_id}.", file=sys.stderr)
    sys.exit(1)

def validate_args(args, parser):  # NOCA:E302(function structure required for CLI)
    """Validate arguments."""
    # In query mode, no other arguments are required
    if args.task_id:
        return

    # Create mode: at least prompt, image_url/cos_key/local, ref_image, or multi-prompts-json is required
    has_image_input = (bool(args.image_url) or bool(args.image_cos_key)
                       or bool(getattr(args, 'image_local', None)))
    has_ref_image_input = (bool(args.ref_image_url) or bool(args.ref_image_cos_key)
                           or bool(getattr(args, 'ref_image_local', None)))
    has_multishot_prompts = bool(args.multi_shot and args.multi_prompts_json)
    if not args.prompt and not has_image_input and not has_ref_image_input and not has_multishot_prompts:
        parser.error("Please specify at least --prompt, --image-url/--image-cos-key/--image-local, or --multi-shot --multi-prompts-json")

    # Model version validation
    model_info = SUPPORTED_MODELS.get(args.model)
    if model_info and args.model_version:
        valid_versions = model_info["versions"]
        if valid_versions and args.model_version not in valid_versions:
            parser.error(
                f"Supported versions for model {args.model}: {', '.join(valid_versions)}, "
                f"current: {args.model_version}"
            )

    # PixVerse-specific validation (aspect ratio + duration + quality)
    if args.model == "PixVerse":
        pixverse_info = SUPPORTED_MODELS["PixVerse"]
        valid_ratios = pixverse_info.get("aspect_ratios", [])
        if args.aspect_ratio and valid_ratios and args.aspect_ratio not in valid_ratios:
            parser.error(
                f"PixVerse supports the following aspect ratios: {', '.join(valid_ratios)}, "
                f"current: {args.aspect_ratio}"
            )
        if args.duration is not None:
            valid_durations = pixverse_info.get("duration_options", [])
            if valid_durations and args.duration not in valid_durations:
                parser.error(
                    f"PixVerse supports durations of integers from 1 to 15 seconds, "
                    f"current: {args.duration}"
                )
        if args.quality:
            valid_qualities = pixverse_info.get("quality_options", [])
            if valid_qualities and args.quality not in valid_qualities:
                parser.error(
                    f"PixVerse supports the following qualities: {', '.join(valid_qualities)}, "
                    f"current: {args.quality}"
                )

    # --quality is only supported by PixVerse
    if args.quality and args.model != "PixVerse":
        parser.error(f"--quality is only supported by the PixVerse model, current: {args.model}")

    # --generate-audio is only supported by PixVerse
    if args.generate_audio is not None and args.model != "PixVerse":
        parser.error(f"--generate-audio is only supported by the PixVerse model, current: {args.model}")

    # Multi-shot feature validation
    if args.multi_shot:
        if not model_info or not model_info.get("supports_multishot", False):
            parser.error(f"The multi-shot feature currently only supports the Kling model")

        # If using multi-shot configuration, validation is required
        if args.multi_prompts_json:
            try:
                multi_prompts = json.loads(args.multi_prompts_json)
            except json.JSONDecodeError as e:
                parser.error(f"--multi-prompts-json must be a valid JSON format: {e}")

            total_shots_duration = validate_multi_prompts(multi_prompts, args.duration, parser)
            if total_shots_duration is None:
                parser.error("Multi-shot configuration validation failed")

    # COS path parameter validation - first frame image
    if args.image_cos_key:
        if not args.image_cos_bucket and not get_cos_bucket():
            parser.error("When using --image-cos-key, you must specify --image-cos-bucket or set the TENCENTCLOUD_COS_BUCKET environment variable")  # NOCA:line-too-long(line cannot be shortened)

    # COS path parameter validation - last frame image
    if args.last_image_cos_key:
        if not args.last_image_cos_bucket and not get_cos_bucket():
            parser.error("When using --last-image-cos-key, you must specify --last-image-cos-bucket or set the TENCENTCLOUD_COS_BUCKET environment variable")  # NOCA:line-too-long(line cannot be shortened)

    # COS path parameter validation - multi-image reference
    if args.ref_image_cos_key:
        if not args.ref_image_cos_bucket and not get_cos_bucket():
            parser.error("When using --ref-image-cos-key, you must specify --ref-image-cos-bucket or set the TENCENTCLOUD_COS_BUCKET environment variable")  # NOCA:line-too-long(line cannot be shortened)
        if args.ref_image_cos_region and len(args.ref_image_cos_region) > 1:
            if len(args.ref_image_cos_region) != len(args.ref_image_cos_key):
                parser.error("The number of --ref-image-cos-region entries must match --ref-image-cos-key, or specify only one")  # NOCA:line-too-long(line cannot be shortened)

    # COS path parameter validation - reference video
    if args.ref_video_cos_key:
        if not args.ref_video_cos_bucket and not get_cos_bucket():
            parser.error("When using --ref-video-cos-key, you must specify --ref-video-cos-bucket or set the TENCENTCLOUD_COS_BUCKET environment variable")  # NOCA:line-too-long(line cannot be shortened)
        if args.ref_video_cos_region and len(args.ref_video_cos_region) > 1:
            if len(args.ref_video_cos_region) != len(args.ref_video_cos_key):
                parser.error("The number of --ref-video-cos-region entries must match --ref-video-cos-key, or specify only one")  # NOCA:line-too-long(line cannot be shortened)

    # Last frame image validation: when using GV, first frame must also be provided
    has_first_frame = (bool(args.image_url) or bool(args.image_cos_key)
                       or bool(getattr(args, 'image_local', None)))
    has_last_frame = (bool(args.last_image_url) or bool(args.last_image_cos_key)
                      or bool(getattr(args, 'last_image_local', None)))
    if has_last_frame and not has_first_frame:
        parser.error("When using a last frame image, you must also specify a first frame image (--image-url / --image-cos-key / --image-local)")  # NOCA:line-too-long(line cannot be shortened)

    # Multi-image reference and ImageUrl/LastImageUrl are mutually exclusive (GV model restriction)
    if has_ref_image_input and has_first_frame:
        if args.model == "GV":
            parser.error("GV model: multi-image reference (--ref-image-url / --ref-image-cos-key / --ref-image-local) cannot be used together with a first-frame image")  # NOCA:line-too-long(line cannot be shortened)

    # Local file existence validation (fail fast)
    for attr, flag in [('image_local', '--image-local'),
                       ('last_image_local', '--last-image-local')]:
        val = getattr(args, attr, None)
        if val and not os.path.isfile(val):
            parser.error(f"{flag} file does not exist: {val}")
    if getattr(args, 'ref_image_local', None):
        for p in args.ref_image_local:
            if not os.path.isfile(p):
                parser.error(f"--ref-image-local file does not exist: {p}")

    # The number of ref_image_type entries cannot exceed the total number of reference images
    total_ref_images = 0
    if args.ref_image_url:
        total_ref_images += len(args.ref_image_url)
    if args.ref_image_cos_key:
        total_ref_images += len(args.ref_image_cos_key)
    if getattr(args, 'ref_image_local', None):
        total_ref_images += len(args.ref_image_local)
    if args.ref_image_type:
        if len(args.ref_image_type) > total_ref_images:
            parser.error("The number of --ref-image-type entries cannot exceed the total number of reference images")
        elif total_ref_images == 0:
            parser.error("--ref-image-type must be used together with --ref-image-url / --ref-image-cos-key / --ref-image-local")

    # Reference video validation (VideoInfos supported by Kling and Mingmou)
    has_ref_video = bool(args.ref_video_url) or bool(args.ref_video_cos_key)
    if has_ref_video:
        if args.model not in ("Kling", "Mingmou"):
            parser.error("Reference video (--ref-video-url or --ref-video-cos-key) is currently only supported by Kling and Mingmou models")

    total_ref_videos = 0
    if args.ref_video_url:
        total_ref_videos += len(args.ref_video_url)
    if args.ref_video_cos_key:
        total_ref_videos += len(args.ref_video_cos_key)
    if args.ref_video_type:
        if len(args.ref_video_type) > total_ref_videos:
            parser.error("The number of --ref-video-type entries cannot exceed the total number of reference videos")
        elif total_ref_videos == 0:
            parser.error("--ref-video-type must be used together with --ref-video-url or --ref-video-cos-key")

    if args.keep_original_sound and not has_ref_video:
        parser.error("--keep-original-sound must be used together with --ref-video-url or --ref-video-cos-key")

    # Off-peak mode is only supported by Vidu
    if args.off_peak and args.model != "Vidu":
        parser.error("Off-peak mode (--off-peak) is currently only supported by the Vidu model")

    # Scene type validation (strict model mapping)
    if args.scene_type:
        valid_scenes = {
            "Kling": ["motion_control"],
            "Mingmou": ["land2port"],
            "Vidu": ["template_effect"],
            "Hunyuan": ["3d_scene"],
        }
        # Find models that support this scene
        supported_models = [m for m, scenes in valid_scenes.items() if args.scene_type in scenes]
        if args.scene_type not in valid_scenes.get(args.model, []):
            if supported_models:
                parser.error(
                    f"Model {args.model} does not support scene type {args.scene_type}. "
                    f"This scene is supported by: {' / '.join(supported_models)}"
                )
            else:
                parser.error(
                    f"Model {args.model} does not support scene type {args.scene_type}."
                )


def run(args):
    """Execute the main workflow."""
    region = args.region or os.environ.get("TENCENTCLOUD_API_REGION", "ap-guangzhou")
    cred = get_credentials()
    client = create_mps_client(cred, region)

    # Mode 1: Query an existing task
    if args.task_id:
        print("=" * 60)
        print("Tencent Cloud MPS AIGC Video Generation — Query Task")
        print("=" * 60)
        print(f"TaskId: {args.task_id}")
        print("-" * 60)

        if args.dry_run:
            print("[Dry Run Mode] Printing query info only, API will not be called")
            print(f"Query params: {{\"TaskId\": \"{args.task_id}\"}}")
            return

        try:
            result = describe_aigc_video_task(client, args.task_id)
            status = result.get("Status", "")
            status_text = {
                "WAIT": "Waiting", "RUN": "Running",
                "DONE": "Completed", "FAIL": "Failed"
            }.get(status, status)

            print(f"Task status: {status_text}")

            if status == "DONE":
                video_urls = result.get("VideoUrls", [])
                resolution = result.get("Resolution", "")
                print(f"Video resolution: {resolution}")
                print(f"Videos generated: {len(video_urls)}")
                statuses = []
                for i, url in enumerate(video_urls, 1):
                    final_url, st = ensure_signed_url(url)
                    print(f"  Video {i}: {final_url}")
                    statuses.append(st)
                print_storage_hint(statuses)
            elif status == "FAIL":
                print(f"Failure reason: {result.get('Message', 'Unknown')}")

            if args.verbose:
                print("\nFull response:")
                print(json.dumps(result, ensure_ascii=False, indent=2))

        except TencentCloudSDKException as e:
            print(f"❌ Query failed: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # Mode 2: Create a task
    params = build_create_params(args)

    if args.dry_run:
        print("=" * 60)
        print("[Dry Run Mode] Printing request params only, API will not be called")
        print("=" * 60)
        print(json.dumps(params, ensure_ascii=False, indent=2))
        return

    # Print execution info
    print("=" * 60)
    print("Tencent Cloud MPS AIGC Intelligent Video Generation")
    print("=" * 60)
    model_info = SUPPORTED_MODELS.get(args.model, {})
    model_desc = model_info.get("description", args.model)
    print(f"Model: {args.model} ({model_desc})")
    if args.model_version:
        print(f"Version: {args.model_version}")
    if args.scene_type:
        scene_desc = SCENE_TYPES.get(args.scene_type, args.scene_type)
        print(f"Scene: {scene_desc}")
    if args.multi_shot:
        print("Storyboard: Enabled")
        if args.multi_prompts_json:
            try:
                multi_prompts = json.loads(args.multi_prompts_json)
                print(f"Shot count: {len(multi_prompts)}")
                for shot in multi_prompts:
                    print(f"  Shot {shot['index']}: duration {shot['duration']}s - {shot['prompt'][:50]}...")
            except json.JSONDecodeError:
                pass
        else:
            print("Storyboard mode: Single shot (auto-split by system)")
    if args.prompt:
        prompt_display = args.prompt[:80] + "..." if len(args.prompt) > 80 else args.prompt
        print(f"Prompt: {prompt_display}")
    if args.negative_prompt:
        print(f"Negative prompt: {args.negative_prompt}")
    if args.enhance_prompt:
        print("Prompt enhancement: Enabled")
    # First-frame image (URL, COS path, or local file)
    if args.image_url:
        print(f"First-frame image: {args.image_url}")
    elif getattr(args, 'image_cos_key', None):
        bucket = args.image_cos_bucket or get_cos_bucket()
        region = args.image_cos_region or get_cos_region()
        print(f"First-frame image: [COS] {bucket}/{region}{args.image_cos_key}")
    elif getattr(args, 'image_local', None):
        print(f"First-frame image: [Local] {args.image_local} (will be uploaded to COS)")

    # Last-frame image (URL, COS path, or local file)
    if args.last_image_url:
        print(f"Last-frame image: {args.last_image_url}")
    elif getattr(args, 'last_image_cos_key', None):
        bucket = args.last_image_cos_bucket or get_cos_bucket()
        region = args.last_image_cos_region or get_cos_region()
        print(f"Last-frame image: [COS] {bucket}/{region}{args.last_image_cos_key}")
    elif getattr(args, 'last_image_local', None):
        print(f"Last-frame image: [Local] {args.last_image_local} (will be uploaded to COS)")

    # Multi-image reference (URL, COS path, or local file)
    total_ref_images = 0
    if args.ref_image_url:
        total_ref_images += len(args.ref_image_url)
    if getattr(args, 'ref_image_cos_key', None):
        total_ref_images += len(args.ref_image_cos_key)
    if getattr(args, 'ref_image_local', None):
        total_ref_images += len(args.ref_image_local)

    if total_ref_images > 0:
        print(f"Reference images: {total_ref_images}")
        # Display direct URLs
        if args.ref_image_url:
            for i, url in enumerate(args.ref_image_url, 1):
                ref_type = ""
                if args.ref_image_type and i - 1 < len(args.ref_image_type):
                    ref_type = f" ({args.ref_image_type[i - 1]})"
                print(f"  Image {i}{ref_type}: {url}")
        # Display COS paths
        if getattr(args, 'ref_image_cos_key', None):
            start_idx = len(args.ref_image_url) if args.ref_image_url else 0
            for i, key in enumerate(args.ref_image_cos_key, 1):
                idx = start_idx + i
                ref_type = ""
                if args.ref_image_type and idx - 1 < len(args.ref_image_type):
                    ref_type = f" ({args.ref_image_type[idx - 1]})"
                bucket = args.ref_image_cos_bucket[i-1] if i-1 < len(args.ref_image_cos_bucket) else (args.ref_image_cos_bucket[0] if args.ref_image_cos_bucket else get_cos_bucket())  # NOCA:line-too-long(line cannot be shortened)
                region = args.ref_image_cos_region[i-1] if args.ref_image_cos_region and i-1 < len(args.ref_image_cos_region) else (args.ref_image_cos_region[0] if args.ref_image_cos_region else get_cos_region())  # NOCA:line-too-long(line cannot be shortened)
                print(f"  Image {idx}{ref_type}: [COS] {bucket}/{region}{key}")
        # Display local files
        if getattr(args, 'ref_image_local', None):
            cos_start = (len(args.ref_image_url) if args.ref_image_url else 0) + \
                        (len(args.ref_image_cos_key) if getattr(args, 'ref_image_cos_key', None) else 0)
            for i, path in enumerate(args.ref_image_local, 1):
                idx = cos_start + i
                ref_type = ""
                if args.ref_image_type and idx - 1 < len(args.ref_image_type):
                    ref_type = f" ({args.ref_image_type[idx - 1]})"
                print(f"  Image {idx}{ref_type}: [Local] {path} (will be uploaded to COS)")

    # Reference videos (URL or COS path)
    total_ref_videos = 0
    if args.ref_video_url:
        total_ref_videos += len(args.ref_video_url)
    if getattr(args, 'ref_video_cos_key', None):
        total_ref_videos += len(args.ref_video_cos_key)

    if total_ref_videos > 0:
        print(f"Reference videos: {total_ref_videos}")
        # Display direct URLs
        if args.ref_video_url:
            for i, url in enumerate(args.ref_video_url, 1):
                ref_type = ""
                if args.ref_video_type and i - 1 < len(args.ref_video_type):
                    ref_type = f" ({args.ref_video_type[i - 1]})"
                keep_sound = ""
                if args.keep_original_sound and i - 1 < len(args.keep_original_sound):
                    keep_sound = f" [Original audio: {args.keep_original_sound[i - 1]}]"
                print(f"  Video {i}{ref_type}{keep_sound}: {url}")
        # Display COS paths
        if getattr(args, 'ref_video_cos_key', None):
            start_idx = len(args.ref_video_url) if args.ref_video_url else 0
            for i, key in enumerate(args.ref_video_cos_key, 1):
                idx = start_idx + i
                ref_type = ""
                if args.ref_video_type and idx - 1 < len(args.ref_video_type):
                    ref_type = f" ({args.ref_video_type[idx - 1]})"
                keep_sound = ""
                if args.keep_original_sound and idx - 1 < len(args.keep_original_sound):
                    keep_sound = f" [Original audio: {args.keep_original_sound[idx - 1]}]"
                bucket = args.ref_video_cos_bucket[i-1] if args.ref_video_cos_bucket and i-1 < len(args.ref_video_cos_bucket) else (args.ref_video_cos_bucket[0] if args.ref_video_cos_bucket else get_cos_bucket())
                region = args.ref_video_cos_region[i-1] if args.ref_video_cos_region and i-1 < len(args.ref_video_cos_region) else (args.ref_video_cos_region[0] if args.ref_video_cos_region else get_cos_region())
                print(f"  Video {idx}{ref_type}{keep_sound}: [COS→PresignedURL] {bucket}/{region}{key}")
    if args.duration is not None:
        print(f"Duration: {args.duration}s")
    if args.resolution:
        print(f"Resolution: {args.resolution}")
    if args.aspect_ratio:
        print(f"Aspect ratio: {args.aspect_ratio}")

    extras = []
    if args.no_logo:
        extras.append("Watermark removal")
    if args.enable_audio is not None:
        extras.append(f"Audio: {'Enabled' if args.enable_audio else 'Disabled'}")
    if args.enable_bgm:
        extras.append("Background music")
    if args.off_peak:
        extras.append("Off-peak mode")
    if extras:
        print(f"Other: {' | '.join(extras)}")
    print("-" * 60)

    if args.verbose:
        print("Request params:")
        print(json.dumps(params, ensure_ascii=False, indent=2))
        print()

    try:
        result = create_aigc_video_task(client, params)
        task_id = result.get("TaskId", "N/A")
        request_id = result.get("RequestId", "N/A")

        print(f"✅ AIGC video generation task submitted successfully!")
        print(f"   TaskId: {task_id}")
        print(f"   RequestId: {request_id}")
        print(f"\n## TaskId: {task_id}")

        if args.no_wait:
            print(f"\nTip: Use the following command to query the task result:")
            print(f"  python mps_aigc_video.py --task-id {task_id}")
            return result

        # Automatically poll and wait for result
        print(f"\nWaiting for task to complete (polling interval {args.poll_interval}s, max wait {args.max_wait}s)...")
        poll_result = poll_task_result(client, task_id, args.poll_interval, args.max_wait)

        video_urls = poll_result.get("VideoUrls", [])
        resolution = poll_result.get("Resolution", "")
        print(f"\n✅ Task completed!")
        if resolution:
            print(f"   Resolution: {resolution}")
        print(f"   Videos generated: {len(video_urls)}")
        statuses = []
        for i, url in enumerate(video_urls, 1):
            final_url, st = ensure_signed_url(url)
            print(f"   Video {i}: {final_url}")
            statuses.append(st)
        print_storage_hint(statuses)

        # Automatically download generated videos
        download_dir = getattr(args, 'download_dir', None)
        if download_dir and video_urls:
            import urllib.request
            import os as _os
            _os.makedirs(download_dir, exist_ok=True)
            print(f"\n📥 Auto-downloading generated videos to: {_os.path.abspath(download_dir)}")
            for i, url in enumerate(video_urls, 1):
                ext = ".mp4"
                local_path = _os.path.join(download_dir, f"aigc_video_{i}{ext}")
                try:
                    urllib.request.urlretrieve(url, local_path)
                    size = _os.path.getsize(local_path)
                    print(f"   [{i}] ✅ {local_path} ({size / 1024 / 1024:.2f} MB)")
                except Exception as e:  # NOCA:broad-except(CLI script needs to handle all exceptions)
                    print(f"   [{i}] ❌ Download failed: {e}")

        if args.verbose:
            print("\nFull response:")
            print(json.dumps(poll_result, ensure_ascii=False, indent=2))

        return poll_result

    except TencentCloudSDKException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud MPS AIGC Intelligent Video Generation — Integrating Hunyuan/Hailuo/Kling/Vidu/OS/GV/PixVerse and other large models for one-stop text-to-video and image-to-video",  # NOCA:line-too-long(line cannot be shortened)


        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-video (default Hunyuan model)
  python mps_aigc_video.py --prompt "A cute orange cat stretching in the sunlight"

  # Specify Kling model version 2.5 + 10-second duration
  python mps_aigc_video.py --prompt "Cyberpunk" --model Kling --model-version 2.5 --duration 10

  # Kling multi-shot: single shot (automatic intelligent splitting)
  python mps_aigc_video.py --prompt "Travel diary, capturing beautiful moments" --model Kling --multi-shot

  # Kling multi-shot: multiple shots (custom per shot)
  python mps_aigc_video.py --model Kling --multi-shot --duration 12 \\
      --multi-prompts-json '[
        {"index": 1, "prompt": "At sunrise, city skyline viewed from hotel window", "duration": "3"},
        {"index": 2, "prompt": "Having breakfast at a cafe, pedestrians on the street outside", "duration": "4"},
        {"index": 3, "prompt": "Walking in the park, sunlight filtering through leaves", "duration": "5"}
      ]'

  # Image-to-video (first frame image URL)
  python mps_aigc_video.py --prompt "Bring the image to life" --image-url https://example.com/photo.jpg

  # Image-to-video (first frame image COS path)
  python mps_aigc_video.py --prompt "Bring the image to life" \\
      --image-cos-bucket mybucket-125xxx --image-cos-region ap-guangzhou --image-cos-key /input/photo.jpg

  # First-and-last frame video generation (GV model)
  python mps_aigc_video.py --prompt "Transition" --model GV \\
      --image-url https://example.com/start.jpg \\
      --last-image-url https://example.com/end.jpg

  # GV multi-image reference (URL)
  python mps_aigc_video.py --prompt "Fusion" --model GV \\
      --ref-image-url https://example.com/img1.jpg --ref-image-type asset \\
      --ref-image-url https://example.com/img2.jpg --ref-image-type style

  # GV multi-image reference (COS path)
  python mps_aigc_video.py --prompt "Fusion" --model GV \\
      --ref-image-cos-bucket mybucket-125xxx --ref-image-cos-region ap-guangzhou --ref-image-cos-key /input/img1.jpg
      --ref-image-type asset \\
      --ref-image-cos-bucket mybucket-125xxx --ref-image-cos-region ap-guangzhou --ref-image-cos-key /input/img2.jpg
      --ref-image-type style

  # Kling reference video + keep original audio
  python mps_aigc_video.py --prompt "Stylization" --model Kling --model-version O1 \\
      --ref-video-url https://example.com/video.mp4 \\
      --ref-video-type base --keep-original-sound yes

  # Kling reference video (COS path, auto-generates pre-signed URL)
  python mps_aigc_video.py --prompt "Stylization" --model Kling --model-version O1 \\
      --ref-video-cos-bucket mybucket-125xxx --ref-video-cos-region ap-guangzhou --ref-video-cos-key /input/video.mp4 \\
      --ref-video-type base --keep-original-sound yes

  # Mingmou landscape to portrait
  python mps_aigc_video.py --prompt "Landscape to portrait conversion" --model Mingmou --scene-type land2port

  # PixVerse v6 text-to-video (10s + 21:9 + 1080p quality)
  python mps_aigc_video.py --prompt "Cinematic city skyline shot" --model PixVerse --model-version v6 \\
      --duration 10 --aspect-ratio 21:9 --quality 1080p

  # PixVerse c1 image-to-video (short-form 9:16 + 540p quality)
  python mps_aigc_video.py --prompt "Character walking forward" --model PixVerse --model-version c1 \\
      --image-url https://example.com/first-frame.jpg --duration 5 --aspect-ratio 9:16 --quality 540p

  # 1080P + 16:9 + remove watermark + audio + BGM
  python mps_aigc_video.py --prompt "Product showcase" --model Kling \\
      --resolution 1080P --aspect-ratio 16:9 --no-logo --enable-audio true --enable-bgm

  # Vidu off-peak mode
  python mps_aigc_video.py --prompt "Scenery" --model Vidu --off-peak

  # Query task result
  python mps_aigc_video.py --task-id 4-AigcVideo-c3b145ec76xxxx

  # Dry Run (print request parameters only)
  python mps_aigc_video.py --prompt "Test" --dry-run

Supported models:
  Hunyuan     Tencent Hunyuan large model (default)
  Hailuo      Hailuo video model, versions 02 / 2.3, duration 6 / 10 seconds
  Kling       Kling video model, versions 2.0-3.0/O1/3.0-Omni, duration 5 / 10 seconds, **supports multi-shot**, **supports reference video**
  Vidu        Vidu video model, versions q2/q2-pro/q2-turbo/q3-pro/q3-turbo, duration 1-10 seconds
  OS          OS video model, version 2.0, duration 4 / 8 / 12 seconds
  GV          GV video model, version 3.1, duration 8 seconds
  Mingmou     Mingmou landscape-to-portrait model, supports land2port scene
  PixVerse    PixVerse video model, versions v6 / c1, duration 1~15 seconds, supports 8 aspect ratios (16:9/4:3/1:1/3:4/9:16/2:3/3:2/21:9), quality 360p/540p/720p/1080p

Scene types (strict model mapping):
  motion_control   Kling — motion control
  land2port        Mingmou — landscape to portrait
  template_effect  Vidu — effect template

Multi-shot feature (Kling exclusive):
  --multi-shot              Enable multi-shot feature (single shot mode: system auto-splits intelligently; multi-shot
  mode: use with --multi-prompts-json to customize each shot)
  --multi-prompts-json      Multi-shot configuration (JSON array format, customize each shot)

Resolution options:
  720P  1080P  2K  4K

Aspect ratio options (supported by some models):
  16:9  9:16  1:1  4:3  3:4

Environment variables:
  TENCENTCLOUD_SECRET_ID   Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET       COS Bucket name (optional, for result storage)
  TENCENTCLOUD_COS_REGION       COS Bucket region (default ap-guangzhou)
        """
    )

    # ---- Task query ----
    query_group = parser.add_argument_group("Task Query (query existing tasks, mutually exclusive with task creation)")
    query_group.add_argument("--task-id", type=str,
                             help="TaskId of an existing task to query")

    # ---- Model configuration ----
    model_group = parser.add_argument_group("Model Configuration")
    model_group.add_argument("--model", type=str, default="Hunyuan",
                             choices=["Hunyuan", "Hailuo", "Kling", "Vidu", "OS", "GV", "Mingmou", "PixVerse"],
                             help="Model name (default: Hunyuan)")
    model_group.add_argument("--model-version", type=str,
                             help="Model version (e.g. Kling: 2.5, Hailuo: 2.3, Vidu: q2-pro, PixVerse: v6/c1)")
    model_group.add_argument("--scene-type", type=str,
                             choices=["motion_control", "land2port", "template_effect", "3d_scene"],
                             help="Scene type (strict model mapping)")

    # ---- Multi-shot configuration (Kling exclusive) ----
    multishot_group = parser.add_argument_group("Multi-shot Configuration (Kling Exclusive)")
    multishot_group.add_argument("--multi-shot", action="store_true",
                                 help="Enable multi-shot feature (Kling exclusive). Single shot mode: system auto-splits intelligently; multi-shot mode: use with --multi-prompts-json to customize each shot")  # NOCA:line-too-long(line cannot be shortened)
    multishot_group.add_argument("--multi-prompts-json", type=str,
                                 help='Multi-shot configuration (JSON array format). Each shot contains index (sequence number), prompt (description), duration (length). Example: \'[{"index":1,"prompt":"Shot 1 description","duration":"5"},...]\'. Number of shots: 1-6, max prompt length per shot: 512 characters, each duration >= 1 second, sum of all durations must equal total duration')  # NOCA:line-too-long(line cannot be shortened)

    # ---- Video generation content ----
    content_group = parser.add_argument_group("Video Generation Content")
    content_group.add_argument("--prompt", type=str,
                               help="Video description text (max 2000 characters). Required when no image is provided")
    content_group.add_argument("--negative-prompt", type=str,
                               help="Negative prompt: describe content you do not want generated (supported by some models)")  # NOCA:line-too-long(line cannot be shortened)
    content_group.add_argument("--enhance-prompt", action="store_true",
                               help="Enable prompt enhancement: automatically optimize prompt to improve generation quality")  # NOCA:line-too-long(line cannot be shortened)

    # ---- Image input (simple mode) ----
    image_group = parser.add_argument_group("Image Input (Image-to-Video)")
    image_group.add_argument("--image-url", type=str,
                             help="First frame image URL (recommended < 10MB, supports jpeg/png)")
    image_group.add_argument("--last-image-url", type=str,
                             help="Last frame image URL (supported by some models, requires --image-url)")
    # COS path input (first frame image)
    image_group.add_argument("--image-cos-bucket", type=str,
                             help="COS Bucket for first frame image (used with --image-cos-region/--image-cos-key)")
    image_group.add_argument("--image-cos-region", type=str,
                             help="COS Region for first frame image (e.g. ap-guangzhou)")
    image_group.add_argument("--image-cos-key", type=str,
                             help="COS Key for first frame image (e.g. /input/image.jpg)")
    image_group.add_argument("--image-local", type=str,
                             metavar="FILE",
                             help="Local first-frame image path; auto-uploaded to COS then passed as ImageUrl. Requires TENCENTCLOUD_COS_BUCKET or --cos-bucket-name")
    # COS path input (last frame image)
    image_group.add_argument("--last-image-cos-bucket", type=str,
                             help="COS Bucket for last frame image (used with --last-image-cos-region/--last-image-cos-key)")  # NOCA:line-too-long(line cannot be shortened)
    image_group.add_argument("--last-image-cos-region", type=str,
                             help="COS Region for last frame image (e.g. ap-guangzhou)")
    image_group.add_argument("--last-image-cos-key", type=str,
                             help="COS Key for last frame image (e.g. /input/last.jpg)")
    image_group.add_argument("--last-image-local", type=str,
                             metavar="FILE",
                             help="Local last-frame image path; auto-uploaded to COS then passed as LastImageUrl. Requires TENCENTCLOUD_COS_BUCKET or --cos-bucket-name")

    # ---- Multi-image reference (Image Infos) ----
    multi_image_group = parser.add_argument_group("Multi-image Reference (supported by GV / Vidu, mutually exclusive with --image-url for GV model)")  # NOCA:line-too-long(line cannot be shortened)
    multi_image_group.add_argument("--ref-image-url", type=str, action="append",
                                   help="Reference image URL (can be specified multiple times, max 3 images)")
    multi_image_group.add_argument("--ref-image-type", type=str, action="append",
                                   choices=["asset", "style"],
                                   help="Reference type (in order across all sources — ref-image-url / ref-image-cos-key / ref-image-local): asset=material | style=style")  # NOCA:line-too-long(line cannot be shortened)
    # COS path input (multi-image reference)
    multi_image_group.add_argument("--ref-image-cos-bucket", type=str, action="append",
                                   help="COS Bucket for reference image (used with --ref-image-cos-region/--ref-image-cos-key, can be specified multiple times)")  # NOCA:line-too-long(line cannot be shortened)
    multi_image_group.add_argument("--ref-image-cos-region", type=str, action="append",
                                   help="COS Region for reference image (e.g. ap-guangzhou, corresponds one-to-one with --ref-image-cos-key)")  # NOCA:line-too-long(line cannot be shortened)
    multi_image_group.add_argument("--ref-image-cos-key", type=str, action="append",
                                   help="COS Key for reference image (e.g. /input/ref.jpg, used with --ref-image-cos-bucket/--ref-image-cos-region)")  # NOCA:line-too-long(line cannot be shortened)
    multi_image_group.add_argument("--ref-image-local", type=str, action="append",
                                   metavar="FILE",
                                   help="Local reference image path (can be specified multiple times); auto-uploaded to COS then passed as ImageUrl. Requires TENCENTCLOUD_COS_BUCKET or --cos-bucket-name")

    # ---- Reference video (Video Infos) ----
    video_ref_group = parser.add_argument_group("Reference Video (Kling model only)")
    video_ref_group.add_argument("--ref-video-url", type=str, action="append",
                                 help="Reference video URL")
    video_ref_group.add_argument("--ref-video-type", type=str, action="append",
                                 choices=["feature", "base"],
                                 help="Reference video type: feature=feature reference | base=video to edit (default)")
    video_ref_group.add_argument("--keep-original-sound", type=str, action="append",
                                 choices=["yes", "no"],
                                 help="Whether to keep the original audio of the video (corresponds to --ref-video-url)")  # NOCA:line-too-long(line cannot be shortened)
    # COS path input (reference video)
    video_ref_group.add_argument("--ref-video-cos-bucket", type=str, action="append",
                                 help="COS Bucket for reference video (used with --ref-video-cos-region/--ref-video-cos-key, can be specified multiple times)")  # NOCA:line-too-long(line cannot be shortened)
    video_ref_group.add_argument("--ref-video-cos-region", type=str, action="append",
                                 help="COS Region for reference video (e.g. ap-guangzhou, corresponds one-to-one with --ref-video-cos-key)")  # NOCA:line-too-long(line cannot be shortened)
    video_ref_group.add_argument("--ref-video-cos-key", type=str, action="append",
                                 help="COS Key for reference video (e.g. /input/video.mp4, used with --ref-video-cos-bucket/--ref-video-cos-region. A pre-signed URL will be auto-generated and filled into VideoUrl)")

    # ---- Video output configuration ----
    output_group = parser.add_argument_group("Video Output Configuration")
    output_group.add_argument("--duration", type=int,
                              help="Video duration (seconds). In multi-shot mode, automatically calculated as the sum of all shot durations; in single shot or non-multi-shot mode, different models support different options, see documentation")  # NOCA:line-too-long(line cannot be shortened)
    output_group.add_argument("--resolution", type=str,
                              choices=["720P", "1080P", "2K", "4K"],
                              help="Output resolution (default varies by model)")
    output_group.add_argument("--aspect-ratio", type=str,
                              help="Aspect ratio (e.g. 16:9, 9:16, 1:1). Different models support different options")
    output_group.add_argument("--quality", type=str,
                              choices=["360p", "540p", "720p", "1080p"],
                              help="Video quality (PixVerse only): 360p / 540p / 720p / 1080p")
    output_group.add_argument("--no-logo", action="store_true",
                              help="Remove logo watermark (supported by Hailuo/Kling/Vidu)")
    output_group.add_argument("--enable-audio", type=str,
                              help="Whether to generate audio for the video (supported by GV/OS, values: true/false)")
    output_group.add_argument("--enable-bgm", action="store_true",
                              help="Whether to add background music (supported by some model versions)")
    output_group.add_argument("--generate-audio", type=str,
                              choices=["true", "false"],
                              help="Whether to generate sound effects (PixVerse only; true=on / false=off; passed via ExtraParameters.EnableAudio, mapped by MPS backend to PixVerse's generate_audio_switch)")  # NOCA:line-too-long(line cannot be shortened)
    output_group.add_argument("--off-peak", action="store_true",
                              help="Off-peak mode (Vidu only), task generated within 48 hours, auto-cancelled on timeout")  # NOCA:line-too-long(line cannot be shortened)

    # ---- COS storage ----
    cos_group = parser.add_argument_group("COS Storage Configuration (optional; if not configured, MPS temporary storage is used for 12 hours; if configured, videos are written to your bucket permanently with an auto-generated 24-hour signed link)")  # NOCA:line-too-long(line cannot be shortened)
    cos_group.add_argument("--cos-bucket-name", type=str,
                           help="COS Bucket name (default: TENCENTCLOUD_COS_BUCKET environment variable)")
    cos_group.add_argument("--cos-bucket-region", type=str,
                           help="COS Bucket region (default: TENCENTCLOUD_COS_REGION environment variable, default ap-guangzhou)")  # NOCA:line-too-long(line cannot be shortened)
    cos_group.add_argument("--cos-bucket-path", type=str, default="/output/aigc-video/",
                          help="Output directory path in COS bucket (default: /output/aigc-video/)")

    # ---- Additional parameters ----
    extra_group = parser.add_argument_group("Additional Parameters")
    extra_group.add_argument("--additional-params", type=str,
                             help="Additional parameters in JSON format (e.g. camera control: '{\"camera_control\":{\"type\":\"simple\"}}')")  # NOCA:line-too-long(line cannot be shortened)

    # ---- Execution control ----
    control_group = parser.add_argument_group("Execution Control")
    control_group.add_argument("--no-wait", action="store_true",
                               help="Create task only, do not wait for result. Query later with --task-id")
    control_group.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
                               help=f"Polling interval (seconds), default {DEFAULT_POLL_INTERVAL}")
    control_group.add_argument("--max-wait", type=int, default=DEFAULT_MAX_WAIT,
                               help=f"Maximum wait time (seconds), default {DEFAULT_MAX_WAIT}")
    control_group.add_argument("--operator", type=str,
                               help="Operator name")

    # ---- Other ----
    other_group = parser.add_argument_group("Other Configuration")
    other_group.add_argument("--region", type=str,
                             help="MPS service region (default ap-guangzhou)")
    other_group.add_argument("--verbose", "-v", action="store_true",
                             help="Output verbose information")
    other_group.add_argument("--dry-run", action="store_true",
                             help="Print request parameters only, do not actually call the API")
    other_group.add_argument("--download-dir", type=str, default=None,
                             help="Automatically download generated video to specified directory after task completion (default: no download; specify a path to enable auto-download)")  # NOCA:line-too-long(line cannot be shortened)

    args = parser.parse_args()

    # Parameter validation
    validate_args(args, parser)

    # Execute
    run(args)

if __name__ == "__main__":
    main()
