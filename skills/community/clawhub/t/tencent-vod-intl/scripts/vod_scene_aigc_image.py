#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD Scene-based AIGC Image Generation Script
Based on CreateSceneAigcImageTask API
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
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
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


def build_scene_info(args):
    """Build scene-based image generation parameters SceneInfo"""
    scene_info = {
        "Type": args.scene_type
    }

    # AI outfit change scene configuration
    if args.scene_type == "change_clothes":
        change_clothes_config = {}

        # Clothing image list
        if args.clothes_files:
            clothes_file_infos = []
            for file_info in args.clothes_files:
                # Format: type:file_id or type:url
                parts = file_info.split(":", 1)
                if len(parts) == 2:
                    file_type, file_value = parts
                    info = {"Type": file_type}
                    if file_type == "File":
                        info["FileId"] = file_value
                    elif file_type == "Url":
                        info["Url"] = file_value
                    clothes_file_infos.append(info)
            if clothes_file_infos:
                change_clothes_config["ClothesFileInfos"] = clothes_file_infos

        # Outfit change prompt
        if args.change_prompt:
            change_clothes_config["Prompt"] = args.change_prompt

        if change_clothes_config:
            scene_info["ChangeClothesConfig"] = change_clothes_config

    # AI product image generation scene configuration
    elif args.scene_type == "product_image":
        product_image_config = {}

        if args.product_prompt:
            product_image_config["Prompt"] = args.product_prompt
        if args.negative_prompt:
            product_image_config["NegativePrompt"] = args.negative_prompt
        if args.product_desc:
            product_image_config["ProductDesc"] = args.product_desc
        if args.more_requirement:
            product_image_config["MoreRequirement"] = args.more_requirement
        if args.output_image_count:
            product_image_config["OutputImageCount"] = args.output_image_count

        if product_image_config:
            scene_info["ProductImageConfig"] = product_image_config

    return scene_info


def build_file_infos(args):
    """Build input image list FileInfos"""
    file_infos = []

    if args.input_files:
        for file_info in args.input_files:
            # Format: type:file_id or type:url
            parts = file_info.split(":", 1)
            if len(parts) == 2:
                file_type, file_value = parts
                info = {"Type": file_type}
                if file_type == "File":
                    info["FileId"] = file_value
                elif file_type == "Url":
                    info["Url"] = file_value
                file_infos.append(info)

    return file_infos if file_infos else None


def build_output_config(args):
    """Build output configuration OutputConfig"""
    output_config = {}

    if args.output_storage_mode:
        output_config["StorageMode"] = args.output_storage_mode
    if args.media_name:
        output_config["MediaName"] = args.media_name
    if args.class_id is not None:
        output_config["ClassId"] = args.class_id
    if args.expire_time:
        output_config["ExpireTime"] = args.expire_time
    if args.aspect_ratio:
        output_config["AspectRatio"] = args.aspect_ratio
    if args.image_width:
        output_config["ImageWidth"] = args.image_width
    if args.image_height:
        output_config["ImageHeight"] = args.image_height
    if args.resolution:
        output_config["Resolution"] = args.resolution

    # Encoding configuration (only valid for AI outfit change scene)
    if args.encode_format or args.encode_quality:
        encode_config = {}
        if args.encode_format:
            encode_config["Format"] = args.encode_format
        if args.encode_quality:
            encode_config["Quality"] = args.encode_quality
        output_config["EncodeConfig"] = encode_config

    return output_config if output_config else None


def create_scene_aigc_image_task(args):
    """Create a scene-based AIGC image generation task"""
    client = get_client(args.region)

    req = models.CreateSceneAigcImageTaskRequest()

    # Required parameters
    if not args.sub_app_id:
        print("Error: Must specify --sub-app-id or set environment variable TENCENTCLOUD_VOD_SUB_APP_ID")
        sys.exit(1)
    req.SubAppId = args.sub_app_id
    req.SceneInfo = build_scene_info(args)

    # Input image list
    file_infos = build_file_infos(args)
    if file_infos:
        req.FileInfos = file_infos

    # Output configuration
    output_config = build_output_config(args)
    if output_config:
        req.OutputConfig = output_config

    # Optional parameters
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
        resp = client.CreateSceneAigcImageTask(req)
        result = json.loads(resp.to_json_string())

        print(f"Scene-based AIGC image generation task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")
        print(f"RequestId: {result.get('RequestId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(long SDK parameter or URL string)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except TencentCloudSDKException as e:
        print(f"Failed to create task: {e}")
        sys.exit(1)
    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        print(f"An error occurred: {e}")
        sys.exit(1)


def query_task(args):
    """Query task details"""
    if hasattr(args, 'dry_run') and args.dry_run:
        print(f"[DRY RUN] DescribeTaskDetail request preview:")
        print(f"  TaskId: {args.task_id}")
        if getattr(args, 'sub_app_id', None):
            print(f"  SubAppId: {args.sub_app_id}")
        return

    client = get_client(args.region)

    req = models.DescribeTaskDetailRequest()
    req.TaskId = args.task_id

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id

    try:
        resp = client.DescribeTaskDetail(req)
        result = json.loads(resp.to_json_string())

        task_type = result.get('TaskType', 'N/A')
        status = result.get('Status', 'N/A')

        print(f"Task type: {task_type}")
        print(f"Task status: {status}")

        if result.get('TaskId'):
            print(f"TaskId: {result['TaskId']}")
        if result.get('CreateTime'):
            print(f"Create time: {result['CreateTime']}")

        # Output task details
        if result.get('ProcedureTask'):
            print(f"\nMedia processing task details:")
            print(json.dumps(result['ProcedureTask'], indent=2, ensure_ascii=False))
        if result.get('EditMediaTask'):
            print(f"\nVideo editing task details:")
            print(json.dumps(result['EditMediaTask'], indent=2, ensure_ascii=False))
        if result.get('WechatPublishTask'):
            print(f"\nWeChat publish task details:")
            print(json.dumps(result['WechatPublishTask'], indent=2, ensure_ascii=False))
        if result.get('ComposeMediaTask'):
            print(f"\nCompose media task details:")
            print(json.dumps(result['ComposeMediaTask'], indent=2, ensure_ascii=False))
        if result.get('SplitMediaTask'):
            print(f"\nVideo split task details:")
            print(json.dumps(result['SplitMediaTask'], indent=2, ensure_ascii=False))
        if result.get('WechatMiniProgramPublishTask'):
            print(f"\nWeChat Mini Program publish task details:")
            print(json.dumps(result['WechatMiniProgramPublishTask'], indent=2, ensure_ascii=False))

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except TencentCloudSDKException as e:
        print(f"Query failed: {e}")
        sys.exit(1)
    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        print(f"An error occurred: {e}")
        sys.exit(1)


def wait_for_task(client, task_id, sub_app_id=None, max_wait=600):
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

            if status == 'SUCCESS':
                print("Task completed!")
                return result
            elif status == 'FAIL':
                print("Task failed!")
                return result

            time.sleep(5)
        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
            print(f"Failed to query task status: {e}")
            time.sleep(5)

    print(f"⏱️ Wait timed out ({max_wait}s), task is still running")
    return None


def main():
    check_sdk_version()
    parser = argparse.ArgumentParser(
        description='VOD Scene-based AIGC Image Generation Tool\nBased on CreateSceneAigcImageTask API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # AI outfit change scene
  python vod_scene_aigc_image.py generate \\
    --sub-app-id 251007502 \\
    --scene-type change_clothes \\
    --input-files "File:3704211xxx" \\
    --clothes-files "File:3704211yyy" \\
    --change-prompt "open the shirt a little"

  # AI product image generation scene
  python vod_scene_aigc_image.py generate \\
    --sub-app-id 251007502 \\
    --scene-type product_image \\
    --input-files "File:3704211xxx" "File:3704211yyy" \\
    --product-prompt "red Chinese New Year background" \\
    --product-desc "This is a bottle of cola" \\
    --output-image-count 6

  # Query task
  python vod_scene_aigc_image.py query --task-id "251007502-SceneAigcImageTask-xxx"

Scene types:
  - change_clothes: AI outfit change
  - product_image: AI product image generation
  - outpainting: AI image outpainting

Input file format:
  - File:FileId  (use VOD media file)
  - Url:URL      (use an accessible URL)
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='subcommands')

    # Generate image task
    gen_parser = subparsers.add_parser('generate', help='Create a scene-based AIGC image generation task')

    # Required parameters
    gen_parser.add_argument('--sub-app-id', type=int,
                           default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                           help='VOD application ID (required, can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long SDK parameter or URL string)
    gen_parser.add_argument('--scene-type', required=True,
                           choices=['change_clothes', 'product_image', 'outpainting'],
                           help='AI image generation scene type (required)')

    # Input image list
    gen_parser.add_argument('--input-files', nargs='+',
                           help='Input image list, format: File:FileId or Url:URL')

    # AI outfit change scene parameters
    gen_parser.add_argument('--clothes-files', nargs='+',
                           help='[Outfit change scene] Clothing image list, format: File:FileId or Url:URL')
    gen_parser.add_argument('--change-prompt',
                           help='[Outfit change scene] Prompt for AI outfit change')

    # AI product image generation scene parameters
    gen_parser.add_argument('--product-prompt',
                           help='[Product image scene] Prompt for generating image background')
    gen_parser.add_argument('--negative-prompt',
                           help='[Product image scene] Prompt to prevent the model from generating certain content')
    gen_parser.add_argument('--product-desc',
                           help='[Product image scene] Detailed description of the product')
    gen_parser.add_argument('--more-requirement',
                           help='[Product image scene] Special requirements')
    gen_parser.add_argument('--output-image-count', type=int,
                           help='[Product image scene] Expected number of images to generate (1-10, default 1)')

    # Output configuration
    gen_parser.add_argument('--output-storage-mode',
                           choices=['Permanent', 'Temporary'],
                           help='Storage mode: Permanent (permanent storage) / Temporary (temporary storage, default)')
    gen_parser.add_argument('--media-name',
                           help='Output filename (max 64 characters)')
    gen_parser.add_argument('--class-id', type=int,
                           help='Category ID (default 0)')
    gen_parser.add_argument('--expire-time',
                           help='Expiration time (ISO 8601 format)')
    gen_parser.add_argument('--aspect-ratio',
                           choices=['1:1', '3:2', '2:3', '3:4', '4:3', '4:5', '5:4', '16:9', '9:16', '21:9'],
                           help='Aspect ratio of the generated image')
    gen_parser.add_argument('--image-width', type=int,
                           help='[Outpainting scene] Output image width')
    gen_parser.add_argument('--image-height', type=int,
                           help='[Outpainting scene] Output image height')
    gen_parser.add_argument('--resolution',
                           choices=['1K', '2K', '4K'],
                           help='[Outfit change scene] Output resolution')

    # Encoding configuration (only valid for AI outfit change scene)
    gen_parser.add_argument('--encode-format',
                           choices=['JPEG', 'PNG'],
                           help='[Outfit change scene] Image format')
    gen_parser.add_argument('--encode-quality', type=int,
                           help='[Outfit change scene] Relative image quality (1-100)')

    # Other optional parameters
    gen_parser.add_argument('--session-id',
                           help='Identifier for deduplication (max 50 characters)')
    gen_parser.add_argument('--session-context',
                           help='Source context (max 1000 characters)')
    gen_parser.add_argument('--tasks-priority', type=int,
                           help='Task priority (-10 to 10, default 0)')
    gen_parser.add_argument('--ext-info',
                           help='Reserved field, used for special purposes')

    # Common parameters
    gen_parser.add_argument('--region', default='ap-guangzhou',
                           help='Region (default: ap-guangzhou)')
    gen_parser.add_argument('--no-wait', action='store_true',
                           help='Submit task only, do not wait for result')
    gen_parser.add_argument('--max-wait', type=int, default=600,
                           help='Maximum wait time in seconds (default: 600)')
    gen_parser.add_argument('--json', action='store_true',
                           help='Output in JSON format')
    gen_parser.add_argument('--dry-run', action='store_true',
                           help='Preview request parameters without actually executing')

    # Query task
    query_parser = subparsers.add_parser('query', help='Query task details')
    query_parser.add_argument('--task-id', required=True,
                             help='Task ID')
    query_parser.add_argument('--sub-app-id', type=int,
                             default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                             help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long SDK parameter or URL string)
    query_parser.add_argument('--region', default='ap-guangzhou',
                             help='Region')
    query_parser.add_argument('--json', action='store_true',
                             help='Output in JSON format')
    query_parser.add_argument('--dry-run', action='store_true',
                             help='Preview request parameters without actually executing')

    args = parser.parse_args()

    if args.command == 'generate':
        create_scene_aigc_image_task(args)
    elif args.command == 'query':
        query_task(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
