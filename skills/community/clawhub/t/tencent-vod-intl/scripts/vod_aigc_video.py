#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD AIGC Video Generation Task Script
Uses the CreateAigcVideoTask API to create AIGC video generation tasks
Supported models: GV, Hailuo, Kling, Jimeng, Vidu, Hunyuan, Mingmou, OS
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
    "GV": ["3.1", "3.1-fast"],
    "Hailuo": ["02", "2.3", "2.3-fast"],
    "Kling": ["1.6", "2.0", "2.1", "2.5", "O1", "3.0-Omni"],
    "Jimeng": ["3.0pro"],
    "Vidu": ["q2", "q2-pro", "q2-turbo", "q3-pro", "q3-turbo"],
    "Hunyuan": ["1.5"],
    "Mingmou": ["1.0"],
    "OS": ["2.0"],
}

MODEL_DEFAULT_VERSION = {
    "GV": "3.1",
    "Hailuo": "2.3",
    "Kling": "2.1",
    "Jimeng": "3.0pro",
    "Vidu": "q2",
    "Hunyuan": "1.5",
    "Mingmou": "1.0",
    "OS": "2.0",
}


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def create_video_task(args):
    """Create an AIGC video generation task"""
    client = get_client(args.region)

    req = models.CreateAigcVideoTaskRequest()

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id

    # Model name and version (required)
    req.ModelName = args.model
    if args.model_version:
        req.ModelVersion = args.model_version
    else:
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

    # Input file info (reference image / first frame)
    if args.file_id or args.file_url:
        file_info = models.AigcVideoTaskInputFileInfo()
        if args.file_id:
            file_info.Type = "File"
            file_info.FileId = args.file_id
        elif args.file_url:
            file_info.Type = "Url"
            file_info.Url = args.file_url
        req.FileInfos = [file_info]
    elif args.file_infos:
        try:
            file_infos_data = json.loads(args.file_infos)
            file_infos = []
            for fi in file_infos_data:
                file_info = models.AigcVideoTaskInputFileInfo()
                file_info.Type = fi.get("Type", "Url")
                if fi.get("FileId"):
                    file_info.FileId = fi["FileId"]
                if fi.get("Url"):
                    file_info.Url = fi["Url"]
                if fi.get("ObjectId"):
                    file_info.ObjectId = fi["ObjectId"]
                file_infos.append(file_info)
            req.FileInfos = file_infos
        except json.JSONDecodeError as e:
            print(f"Error: --file-infos parameter has invalid JSON format: {e}")
            sys.exit(1)

    # Fixed subject input info (Subject Infos - may not be supported in SDK, skipping)
    # if args.subject_infos: ... (SDK does not support this field yet)

    # Last frame (first-and-last-frame video generation)
    if args.last_frame_file_id:
        req.LastFrameFileId = args.last_frame_file_id
    if args.last_frame_url:
        req.LastFrameUrl = args.last_frame_url

    # Scene type
    if args.scene_type:
        req.SceneType = args.scene_type

    # Output configuration
    if any([args.output_storage_mode, args.output_media_name, args.output_class_id,
            args.output_expire_time, args.output_resolution, args.output_duration,
            args.output_aspect_ratio, args.output_audio_generation, args.output_person_generation,
            args.output_enhance_switch, args.output_off_peak, args.output_frame_interpolate,
            args.output_logo_add, args.input_compliance_check, args.output_compliance_check]):
        output_config = models.AigcVideoOutputConfig()
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
        if args.output_duration:
            output_config.Duration = args.output_duration
        if args.output_aspect_ratio:
            output_config.AspectRatio = args.output_aspect_ratio
        if args.output_audio_generation:
            output_config.AudioGeneration = args.output_audio_generation
        if args.output_person_generation:
            output_config.PersonGeneration = args.output_person_generation
        if args.output_enhance_switch:
            output_config.EnhanceSwitch = args.output_enhance_switch
        if args.output_off_peak:
            output_config.OffPeak = args.output_off_peak
        if args.output_frame_interpolate:
            output_config.FrameInterpolate = args.output_frame_interpolate
        if args.output_logo_add:
            output_config.LogoAdd = args.output_logo_add
        if args.input_compliance_check:
            output_config.InputComplianceCheck = args.input_compliance_check
        if args.output_compliance_check:
            output_config.OutputComplianceCheck = args.output_compliance_check
        req.OutputConfig = output_config

    if args.procedure:
        req.Procedure = args.procedure
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

    # ── Ext Info construction ──────────────────────────────────────────────────────────
    # Priority: --element-ids / --elements-file > --ext-info
    # Format: Ext Info = json.dumps({"Additional Parameters": json.dumps({"element_list": [{"element_id": ...}]})})
    ext_info_val = None

    element_ids = []

    if args.element_ids:
        # --element-ids supports a comma-separated list of integers
        try:
            element_ids = [int(eid.strip()) for eid in args.element_ids.split(",") if eid.strip()]
        except ValueError as e:
            print(f"Error: --element-ids format is invalid, expected comma-separated integers, e.g. 865750283577090106: {e}")
            sys.exit(1)

    if not element_ids and args.elements_file:
        # Read all Element Ids from elements.json file
        ef_path = args.elements_file
        if not os.path.isabs(ef_path):
            # Relative path: relative to the parent directory of the script directory (skill root)
            ef_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                ef_path,
            )
        try:
            with open(ef_path, "r", encoding="utf-8") as f:
                elements_data = json.load(f)
            if isinstance(elements_data, list):
                element_ids = [int(item["ElementId"]) for item in elements_data if item.get("ElementId")]
            elif isinstance(elements_data, dict):
                element_ids = [int(v["ElementId"]) for v in elements_data.values() if v.get("ElementId")]
            print(f"Read {len(element_ids)} subject ElementIds from {ef_path}: {element_ids}")
        except FileNotFoundError:
            print(f"Error: Subject file not found: {ef_path}")
            sys.exit(1)
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            print(f"Error: Failed to read subject file: {e}")
            sys.exit(1)

    if element_ids:
        # Build nested JSON string
        # Ext Info = '{"Additional Parameters": "{\"element_list\": [{\"element_id\": 123}]}"}'
        element_list = [{"element_id": eid} for eid in element_ids]
        additional_params = json.dumps({"element_list": element_list}, ensure_ascii=False)
        ext_info_val = json.dumps({"AdditionalParameters": additional_params}, ensure_ascii=False)
        print(f"  Using subject element_list: {element_ids}")
        print(f"  ExtInfo: {ext_info_val}")
    elif args.ext_info:
        ext_info_val = args.ext_info

    if ext_info_val:
        req.ExtInfo = ext_info_val

    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return

    try:
        resp = client.CreateAigcVideoTask(req)
        result = json.loads(resp.to_json_string())

        print(f"AIGC video generation task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"Failed to create video generation task: {e}")
        sys.exit(1)


def wait_for_task(client, task_id, sub_app_id=None, max_wait=1800):
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

            time.sleep(15)
        except Exception as e:
            print(f"Failed to query task status: {e}")
            time.sleep(15)

    print(f"⏱️ Wait timed out ({max_wait}s), task is still running")
    return None


def list_models(args):
    """List supported models"""
    print("Supported models and versions:")
    for model, versions in MODEL_VERSIONS.items():
        default = MODEL_DEFAULT_VERSION[model]
        print(f"  {model}: versions {versions} (default: {default})")
    print("\nScene types (SceneType):")
    print("  Kling model: motion_control, avatar_i2v (digital avatar), lip_sync")
    print("  Vidu model: template_effect (template effect), subject_reference (subject reference)")


def main():
    check_sdk_version()
    parser = argparse.ArgumentParser(
        description='VOD AIGC Video Generation Task Tool (CreateAigcVideoTask)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Text-to-video (using GV model)
  python vod_aigc_video.py create --model GV --prompt "A puppy running on the grass"

  # Image-to-video (specify reference image FileId)
  python vod_aigc_video.py create --model Kling --model-version 2.1 \\
      --file-id 528548548798527148 --prompt "Make the person in the image start walking"

  # Image-to-video (specify reference image URL)
  python vod_aigc_video.py create --model Vidu --model-version q2 \\
      --file-url "https://example.com/ref.jpg" --prompt "camera panning left"

  # First-and-last-frame video generation
  python vod_aigc_video.py create --model GV \\
      --file-url "https://example.com/first.jpg" \\
      --last-frame-url "https://example.com/last.jpg" \\
      --prompt "smooth transition"

  # Set output configuration (permanent storage, specify resolution and duration)
  python vod_aigc_video.py create --model Hailuo --prompt "Scenic landscape video" \\
      --output-storage-mode Permanent --output-resolution 1080P --output-duration 5

  # Use scene type (Kling digital avatar)
  python vod_aigc_video.py create --model Kling --model-version 2.1 \\
      --file-id 528548548798527148 --scene-type avatar_i2v

  # Use custom subject (Kling 3.0-Omni/O1, specify ElementId directly)
  python vod_aigc_video.py create --model Kling --model-version 3.0-Omni \\
      --prompt "<<<element_1>>> dancing" \\
      --element-ids 865750283577090106

  # Use custom subject (auto-read all subjects from elements.json)
  python vod_aigc_video.py create --model Kling --model-version 3.0-Omni \\
      --prompt "<<<element_1>>> dancing" \\
      --elements-file mem/elements.json

  # Default: wait for task completion (video generation takes longer, default --max-wait 1800)
  python vod_aigc_video.py create --model GV --prompt "A cat"
  
  # No wait, submit task only
  python vod_aigc_video.py create --model GV --prompt "A cat" --no-wait

  # List supported models
  python vod_aigc_video.py models

  # Preview request parameters
  python vod_aigc_video.py create --model GV --prompt "test" --dry-run
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # ---- create subcommand ----
    create_parser = subparsers.add_parser('create', help='Create an AIGC video generation task')

    # Model parameters (required)
    create_parser.add_argument('--model', required=True,
                               choices=list(MODEL_VERSIONS.keys()),
                               help='Model name (required): GV/Hailuo/Kling/Jimeng/Vidu/Hunyuan/Mingmou/OS')
    create_parser.add_argument('--model-version', help='Model version; uses default version if not specified')

    # Content parameters
    create_parser.add_argument('--prompt', help='Prompt for video generation (required when no input file is provided)')
    create_parser.add_argument('--negative-prompt', help='Negative prompt to prevent the model from generating certain content')
    create_parser.add_argument('--enhance-prompt', choices=['Enabled', 'Disabled'],
                               help='Whether to automatically optimize the prompt: Enabled/Disabled')

    # Input files (reference image / first frame)
    create_parser.add_argument('--file-id', help='VOD FileId of the reference image / first frame')
    create_parser.add_argument('--file-url', help='URL of the reference image / first frame')
    create_parser.add_argument('--file-infos',
                               help='JSON array of multiple reference images, format: [{"Type":"Url","Url":"..."}]')

    # Fixed subjects
    create_parser.add_argument('--subject-infos',
                               help='Fixed subject JSON array, format: [{"Id":"...","Name":"..."}]')

    # Last frame (first-and-last-frame video generation)
    create_parser.add_argument('--last-frame-file-id', help='VOD FileId of the last frame image (GV/Kling/Vidu only)')
    create_parser.add_argument('--last-frame-url', help='URL of the last frame image (GV/Kling/Vidu only)')

    # Scene type
    create_parser.add_argument('--scene-type',
                               help='Scene type: Kling supports motion_control/avatar_i2v/lip_sync; Vidu supports template_effect/subject_reference')

    # Output configuration
    create_parser.add_argument('--output-storage-mode', choices=['Permanent', 'Temporary'],
                               help='Storage mode: Permanent / Temporary (default)')
    create_parser.add_argument('--output-media-name', help='Output filename, max 64 characters')
    create_parser.add_argument('--output-class-id', type=int, help='Output file category ID, default 0')
    create_parser.add_argument('--output-expire-time', help='Output file expiration time in ISO 8601 format')
    create_parser.add_argument('--output-resolution', help='Generated video resolution, e.g. 720P/1080P/2K/4K')
    create_parser.add_argument('--output-duration', type=int, help='Generated video duration (seconds)')
    create_parser.add_argument('--output-aspect-ratio', help='Video aspect ratio, e.g. 16:9, 9:16, 1:1')
    create_parser.add_argument('--output-audio-generation', choices=['Enabled', 'Disabled'],
                               help='Whether to generate audio (GV/OS/Vidu supported): Enabled/Disabled, default Disabled')
    create_parser.add_argument('--output-person-generation', choices=['AllowAdult', 'Disallowed'],
                               help='Whether to allow person/face generation: AllowAdult/Disallowed')
    create_parser.add_argument('--output-enhance-switch', choices=['Enabled', 'Disabled'],
                               help='Whether to enable video enhancement (auto-enabled when resolution exceeds model output): Enabled/Disabled')
    create_parser.add_argument('--output-off-peak', choices=['Enabled', 'Disabled'],
                               help='Whether to enable off-peak scheduling: Enabled/Disabled')
    create_parser.add_argument('--output-frame-interpolate', choices=['Enabled', 'Disabled'],
                               help='Whether to enable Vidu smart frame interpolation: Enabled/Disabled')
    create_parser.add_argument('--output-logo-add', choices=['Enabled', 'Disabled'],
                               help='Whether to enable logo watermark (Vidu supported): Enabled/Disabled')
    create_parser.add_argument('--input-compliance-check', choices=['Enabled', 'Disabled'],
                               help='Whether to enable input content compliance check')
    create_parser.add_argument('--output-compliance-check', choices=['Enabled', 'Disabled'],
                               help='Whether to enable output content compliance check')

    # Other parameters
    create_parser.add_argument('--procedure', help='Task flow name, auto-execute specified task flow after video generation')
    create_parser.add_argument('--seed', type=int, help='Model random seed')
    create_parser.add_argument('--input-region', choices=['Mainland', 'Oversea'],
                               help='Input file region: Mainland (default) / Oversea (use for overseas URLs)')
    create_parser.add_argument('--session-id', help='Deduplication identifier; same ID within 3 days returns an error, max 50 characters')
    create_parser.add_argument('--session-context', help='Source context, passes through user request info, max 1000 characters')
    create_parser.add_argument('--tasks-priority', type=int, help='Task priority, range -10 to 10, default 0')
    create_parser.add_argument('--element-ids',
                               help='Subject ElementId list (comma-separated integers), Kling 3.0-Omni/O1 only, '
                                    'e.g.: 865750283577090106,865750283577090107')
    create_parser.add_argument('--elements-file',
                               help='Read subject ElementIds from elements.json file; supports relative path (relative to skill root) '
                                    'or absolute path, e.g.: mem/elements.json')
    create_parser.add_argument('--ext-info', help='Reserved field for special use (mutually exclusive with --element-ids, lower priority)')
    create_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                               help='Sub-application ID; required for VOD accounts created after 2023-12-25')
    create_parser.add_argument('--region', default='ap-guangzhou', help='Region, default ap-guangzhou')
    create_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    create_parser.add_argument('--max-wait', type=int, default=1800, help='Maximum wait time (seconds), default 1800')
    create_parser.add_argument('--json', action='store_true', help='Output full response in JSON format')
    create_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters without executing')

    # ---- models subcommand ----
    models_parser = subparsers.add_parser('models', help='List supported models and versions')

    args = parser.parse_args()

    if args.command == 'create':
        create_video_task(args)
    elif args.command == 'models':
        list_models(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
