#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD AIGC Image Generation Task Script
Uses the CreateAigcImageTask API to create AIGC image generation tasks
Supported models: Hunyuan, Qwen, Vidu, Kling, MJ (Midjourney), GEM
"""

import os
import sys
import json
import argparse
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vod_auto_upgrade import check_sdk_version


try:
    from vod_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False

try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.vod.v20180717 import vod_client, models
except ImportError:
    print("Error: Please install the Tencent Cloud SDK first: pip install tencentcloud-sdk-python")
    sys.exit(1)


def get_credential():
    """Get Tencent Cloud credentials"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        # Fallback: try to load credentials from ~/.env etc.
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] Environment variables not set, attempting to load from dotenv files...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from vod_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print("Error: Please set environment variables TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
            sys.exit(1)

    return credential.Credential(secret_id, secret_key)


def get_client(region="ap-guangzhou"):
    """Get VOD client"""
    cred = get_credential()
    http_profile = HttpProfile()
    http_profile.endpoint = "vod.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return vod_client.VodClient(cred, region, client_profile)


# Model version mapping
MODEL_VERSIONS = {
    "Qwen": ["0925"],
    "Hunyuan": ["3.0"],
    "Vidu": ["q2"],
    "Kling": ["2.1", "3.0", "3.0-Omni"],
    "MJ": ["v7"],
    "GEM": ["2.5", "3.0"],
}

# Model default versions
MODEL_DEFAULT_VERSION = {
    "Qwen": "0925",
    "Hunyuan": "3.0",
    "Vidu": "q2",
    "Kling": "2.1",
    "MJ": "v7",
    "GEM": "2.5",
}


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def create_image_task(args):
    """Create an AIGC image generation task"""
    client = get_client(args.region)

    req = models.CreateAigcImageTaskRequest()

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id

    # Model name and version (required)
    req.ModelName = args.model
    if args.model_version:        req.ModelVersion = args.model_version
    else:
        # Use default version
        req.ModelVersion = MODEL_DEFAULT_VERSION.get(args.model, "")
        if not req.ModelVersion:
            print(f"Error: Unknown model {args.model}, available models: {list(MODEL_DEFAULT_VERSION.keys())}")
            sys.exit(1)

    # Prompt
    if args.prompt:
        req.Prompt = args.prompt

    if args.negative_prompt:
        req.NegativePrompt = args.negative_prompt

    if args.enhance_prompt:
        req.EnhancePrompt = args.enhance_prompt

    # Input file info (reference image)
    if args.file_id or args.file_url:
        file_info = models.AigcImageTaskInputFileInfo()
        if args.file_id:
            file_info.Type = "File"
            file_info.FileId = args.file_id
        elif args.file_url:
            file_info.Type = "Url"
            file_info.Url = args.file_url
        if args.file_text:
            file_info.Text = args.file_text
        req.FileInfos = [file_info]
    elif args.file_infos:
        # Support multiple file infos in JSON format
        try:
            file_infos_data = json.loads(args.file_infos)
            file_infos = []
            for fi in file_infos_data:
                file_info = models.AigcImageTaskInputFileInfo()
                file_info.Type = fi.get("Type", "Url")
                if fi.get("FileId"):
                    file_info.FileId = fi["FileId"]
                if fi.get("Url"):
                    file_info.Url = fi["Url"]
                if fi.get("Text"):
                    file_info.Text = fi["Text"]
                file_infos.append(file_info)
            req.FileInfos = file_infos
        except json.JSONDecodeError as e:
            print(f"Error: --file-infos parameter has invalid JSON format: {e}")
            sys.exit(1)

    # Output configuration
    if any([args.output_storage_mode, args.output_media_name, args.output_class_id,
            args.output_expire_time, args.output_resolution, args.output_aspect_ratio,
            args.output_person_generation, args.input_compliance_check, args.output_compliance_check]):
        output_config = models.AigcImageOutputConfig()
        if args.output_storage_mode:
            output_config.StorageMode = args.output_storage_mode
        if args.output_media_name:
            output_config.MediaName = args.output_media_name
        if args.output_class_id is not None:
            output_config.ClassId = args.output_class_id
        if args.output_expire_time:
            output_config.ExpireTime = args.output_expire_time
        if args.output_resolution:
            output_config.Resolution = args.output_resolution
        if args.output_aspect_ratio:
            output_config.AspectRatio = args.output_aspect_ratio
        if args.output_person_generation:
            output_config.PersonGeneration = args.output_person_generation
        if args.input_compliance_check:
            output_config.InputComplianceCheck = args.input_compliance_check
        if args.output_compliance_check:
            output_config.OutputComplianceCheck = args.output_compliance_check
        req.OutputConfig = output_config

    if args.scene_type:
        req.SceneType = args.scene_type
    if args.seed is not None:
        req.Seed = args.seed
    if args.input_region:
        req.InputRegion = args.input_region
    if args.session_id:
        req.SessionId = args.session_id
    if args.session_context:
        req.SessionContext = args.session_context
    if args.tasks_priority is not None:
        req.TasksPriority = args.tasks_priority
    if args.ext_info:
        req.ExtInfo = args.ext_info

    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return

    try:
        resp = client.CreateAigcImageTask(req)
        result = json.loads(resp.to_json_string())

        print(f"AIGC image generation task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query later: python scripts/vod_aigc_image.py query --task-id {result['TaskId']}")

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"Failed to create image generation task: {e}")
        sys.exit(1)


def wait_for_task(client, task_id, sub_app_id=None, max_wait=600, poll_interval=10):
    """Wait for task completion"""
    print(f"\nWaiting for task to complete (TaskId: {task_id})...")
    start_time = time.time()

    while time.time() - start_time < max_wait:
        req = models.DescribeTaskDetailRequest()
        req.TaskId = task_id
        if sub_app_id:
            req.SubAppId = sub_app_id

        try:
            resp = client.DescribeTaskDetail(req)
            result = json.loads(resp.to_json_string())

            status = result.get('Status', 'PROCESSING')
            print(f"  Current status: {status}")

            if status == 'FINISH':
                print("Task completed!")
                return result
            elif status == 'FAIL':
                print("Task failed!")
                return result

            time.sleep(poll_interval)
        except Exception as e:
            print(f"Failed to query task status: {e}")
            time.sleep(poll_interval)

    print(f"⏱️ Wait timed out ({max_wait}s), task is still running")
    return None


def list_models(args):
    """List supported models"""
    print("Supported models and versions:")
    for model, versions in MODEL_VERSIONS.items():
        default = MODEL_DEFAULT_VERSION[model]
        print(f"  {model}: versions {versions} (default: {default})")


def query_task(args):
    """Query AIGC image generation task status"""
    if hasattr(args, 'dry_run') and args.dry_run:
        print(f"[DRY RUN] DescribeTaskDetail request preview:")
        print(f"  TaskId: {args.task_id}")
        if getattr(args, 'sub_app_id', None):
            print(f"  SubAppId: {args.sub_app_id}")
        return

    client = get_client(args.region)

    if not args.no_wait:
        result = wait_for_task(client, args.task_id, args.sub_app_id, args.max_wait, args.poll_interval)
        if result is None:
            print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
    else:
        req = models.DescribeTaskDetailRequest()
        req.TaskId = args.task_id
        if args.sub_app_id:
            req.SubAppId = args.sub_app_id
        try:
            resp = client.DescribeTaskDetail(req)
            result = json.loads(resp.to_json_string())
            status = result.get('Status', 'N/A')
            print(f"Task status: {status}")
        except Exception as e:
            print(f"Query failed: {e}")
            sys.exit(1)

    if result and args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    check_sdk_version()
    parser = argparse.ArgumentParser(
        description='VOD AIGC Image Generation Task Tool (CreateAigcImageTask)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate image using Hunyuan model (text-to-image)
  python vod_aigc_image.py create --model Hunyuan --prompt "A cute kitten playing in the grass"

  # Use Qwen model with a specified version
  python vod_aigc_image.py create --model Qwen --model-version 0925 --prompt "a beautiful sunset"

  # Image-to-image (specify reference image FileId)
  python vod_aigc_image.py create --model GEM --model-version 2.5 \\
      --file-id 528548548798527148 --prompt "Change the image style to watercolor painting"

  # Image-to-image (specify reference image URL)
  python vod_aigc_image.py create --model Kling --model-version 2.1 \\
      --file-url "https://example.com/ref.jpg" --prompt "Keep the subject, change the background to a starry sky"

  # Set output configuration (permanent storage, specify resolution and aspect ratio)
  python vod_aigc_image.py create --model Hunyuan --prompt "landscape painting" \\
      --output-storage-mode Permanent --output-resolution 2K --output-aspect-ratio 16:9

  # Enable prompt enhancement
  python vod_aigc_image.py create --model GEM --prompt "cat" --enhance-prompt Enabled

  # Wait for task completion by default (add --no-wait to skip waiting)
  python vod_aigc_image.py create --model Hunyuan --prompt "a dog"

  # List supported models
  python vod_aigc_image.py models

  # Preview request parameters
  python vod_aigc_image.py create --model Hunyuan --prompt "test" --dry-run
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='subcommands')

    # ---- create subcommand ----
    create_parser = subparsers.add_parser('create', help='Create an AIGC image generation task')

    # Model parameters (required)
    create_parser.add_argument('--model', required=True,
                               choices=list(MODEL_VERSIONS.keys()),
                               help='Model name (required): Hunyuan/Qwen/Vidu/Kling/MJ/GEM')
    create_parser.add_argument('--model-version', help='Model version; uses default version if not specified')

    # Content parameters
    create_parser.add_argument('--prompt', help='Prompt for image generation (required when no input file is provided)')
    create_parser.add_argument('--negative-prompt', help='Negative prompt to prevent the model from generating certain content')
    create_parser.add_argument('--enhance-prompt', choices=['Enabled', 'Disabled'],
                               help='Whether to automatically enhance the prompt: Enabled/Disabled')

    # Input files (reference image, choose one of three)
    create_parser.add_argument('--file-id', help='VOD FileId of the reference image (mutually exclusive with --file-url)')
    create_parser.add_argument('--file-url', help='URL of the reference image (mutually exclusive with --file-id)')
    create_parser.add_argument('--file-text', help='Description of the reference image (only valid for GEM 2.5/3.0)')
    create_parser.add_argument('--file-infos', help='JSON array of multiple reference images, format: [{"Type":"Url","Url":"..."}]')

    # Output configuration
    create_parser.add_argument('--output-storage-mode', choices=['Permanent', 'Temporary'],
                               help='Storage mode: Permanent / Temporary (default)')
    create_parser.add_argument('--output-media-name', help='Output filename, max 64 characters')
    create_parser.add_argument('--output-class-id', type=int, help='Output file category ID, default 0')
    create_parser.add_argument('--output-expire-time', help='Output file expiration time in ISO 8601 format')
    create_parser.add_argument('--output-resolution',
                               help='Generated image resolution, e.g. 1K/2K/4K (GEM), 1080p/2K/4K (Vidu), 720P/1080P/2K/4K (Hunyuan)')
    create_parser.add_argument('--output-aspect-ratio',
                               help='Image aspect ratio, e.g. 16:9, 9:16, 1:1, 4:3, 3:4, etc.')
    create_parser.add_argument('--output-person-generation',
                               choices=['AllowAdult', 'Disallowed'],
                               help='Whether to allow person generation: AllowAdult/Disallowed')
    create_parser.add_argument('--input-compliance-check', choices=['Enabled', 'Disabled'],
                               help='Whether to enable input content compliance check')
    create_parser.add_argument('--output-compliance-check', choices=['Enabled', 'Disabled'],
                               help='Whether to enable output content compliance check')

    # Other parameters
    create_parser.add_argument('--scene-type',
                               help='Scene type (when ModelName is Hunyuan: 3d_panorama for panoramic image; not supported for other models)')
    create_parser.add_argument('--seed', type=int, help='Model random seed')
    create_parser.add_argument('--input-region', choices=['Mainland', 'Oversea'],
                               help='Input file region: Mainland (default) / Oversea (use for overseas addresses)')
    create_parser.add_argument('--session-id', help='Deduplication identifier; returns an error for the same ID within three days, max 50 characters')
    create_parser.add_argument('--session-context', help='Source context, passes through user request info, max 1000 characters')
    create_parser.add_argument('--tasks-priority', type=int, help='Task priority, range -10 to 10, default 0')
    create_parser.add_argument('--ext-info', help='Reserved field, used for special purposes')
    create_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                               help='Sub-application ID, required for customers who activated VOD after 2023-12-25')
    create_parser.add_argument('--region', default='ap-guangzhou', help='Region, default ap-guangzhou')
    create_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    create_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds), default 600')
    create_parser.add_argument('--json', action='store_true', help='Output full response in JSON format')
    create_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters without actually executing')

    # ---- models subcommand ----
    models_parser = subparsers.add_parser('models', help='List supported models and versions')

    # ---- query subcommand (query task status) ----
    query_parser = subparsers.add_parser('query', help='Query AIGC image generation task status (via DescribeTaskDetail)')
    query_parser.add_argument('--task-id', required=True, help='Task ID (required)')
    query_parser.add_argument('--sub-app-id', type=int,
                              default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                              help='Sub-application ID')
    query_parser.add_argument('--region', default='ap-guangzhou', help='Region, default ap-guangzhou')
    query_parser.add_argument('--no-wait', action='store_true', help='Query status only, do not wait for completion')
    query_parser.add_argument('--poll-interval', type=int, default=10, help='Polling interval (seconds), default 10')
    query_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds), default 600')
    query_parser.add_argument('--json', action='store_true', help='Output full response in JSON format')
    query_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters without actually executing')

    args = parser.parse_args()

    if args.command == 'create':
        create_image_task(args)
    elif args.command == 'models':
        list_models(args)
    elif args.command == 'query':
        query_task(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
