#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD image processing script
Supports async image processing (ProcessImageAsync), image understanding (large language model), and image
super-resolution enhancement

Image understanding features:
- Intelligent image understanding and analysis powered by large language models (Gemini series)
- Supports custom prompts to guide the model's analysis direction
- Supports three input methods: FileId / URL / Base64
- Supports model selection: gemini-2.5-flash / gemini-2.5-flash-lite / gemini-2.5-pro / gemini-3-flash / gemini-3-pro

Image super-resolution enhancement features:
- Create custom super-resolution templates via CreateProcessImageAsyncTemplate (templates are reusable)
- Supports three super-resolution modes: percent (scale factor), fixed (fixed resolution), aspect (aspect-ratio fit)
- Supports standard (general super-resolution) and super (advanced super-resolution) types
- Supports custom output format (JPEG/PNG/BMP/WebP) and quality parameters
- Target resolution must not exceed 4096x4096
"""

import os
import sys
import json
import argparse
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vod_auto_upgrade import check_sdk_version

# Soft dependency: vod_load_env is used as a fallback to load credentials from ~/.env etc. when env vars are missing
try:
    from vod_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False

check_sdk_version()

try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.vod.v20180717 import vod_client, models
except ImportError:
    print("Error: Please install the Tencent Cloud SDK first: pip install tencentcloud-sdk-python")
    sys.exit(1)


def get_credential():
    """Retrieve Tencent Cloud credentials"""
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
    """Get the VOD client"""
    cred = get_credential()
    http_profile = HttpProfile()
    http_profile.endpoint = "vod.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return vod_client.VodClient(cred, region, client_profile)


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def understand_image(args):
    """Image understanding — intelligent image analysis powered by a large language model
    Uses the ProcessImageAsync API with template Definition=14
    Supports Prompts and multiple Gemini models
    """
    # Validate input
    if not args.file_id and not args.url and not args.base64:
        print("Error: Please specify one of --file-id, --url, or --base64")
        sys.exit(1)

    if not args.sub_app_id:
        print("Error: --sub-app-id is required for the image understanding feature")
        sys.exit(1)

    prompt_text = args.prompt or "Understand this image"

    # Build request parameters
    req_params = {}
    if args.file_id:
        req_params["FileId"] = args.file_id
    elif args.url:
        req_params["Url"] = args.url
    elif args.base64:
        req_params["Base64"] = args.base64

    req_params["SubAppId"] = args.sub_app_id

    # Image understanding uses fixed template 14 + Prompts
    req_params["ImageTaskInput"] = {
        "Definition": 14,
        "ExtendedParameter": {
            "Prompts": [prompt_text]
        }
    }

    # Output configuration
    output_config = {}
    if args.output_name:
        output_config["MediaName"] = args.output_name
    if args.class_id is not None:
        output_config["ClassId"] = args.class_id
    if args.expire_time:
        output_config["ExpireTime"] = args.expire_time
    if output_config:
        req_params["OutputConfig"] = output_config

    # Set model (via Ext Info)
    if args.model:
        model_map = {
            "gemini-2.5-flash": "Google/gemini-2.5-flash",
            "gemini-2.5-flash-lite": "Google/gemini-2.5-flash-lite",
            "gemini-2.5-pro": "Google/gemini-2.5-pro",
            "gemini-3-flash": "Google/gemini-3-flash",
            "gemini-3-pro": "Google/gemini-3-pro",
        }
        model_name = model_map.get(args.model, args.model)
        if "/" not in model_name:
            model_name = f"Google/{model_name}"
        req_params["ExtInfo"] = json.dumps({"ModelName": model_name})
    elif args.ext_info:
        req_params["ExtInfo"] = args.ext_info

    if args.session_id:
        req_params["SessionId"] = args.session_id
    if args.session_context:
        req_params["SessionContext"] = args.session_context
    if args.tasks_priority is not None:
        req_params["TasksPriority"] = args.tasks_priority

    if args.dry_run:
        print("[DRY RUN] Image understanding request parameters:")
        print(json.dumps(req_params, indent=2, ensure_ascii=False))
        return

    client = get_client(args.region)

    try:
        req = models.ProcessImageAsyncRequest()
        req.from_json_string(json.dumps(req_params))

        resp = client.ProcessImageAsync(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get('TaskId', 'N/A')
        print(f"Image understanding task submitted!")
        print(f"TaskId: {task_id}")
        print(f"Prompt: {prompt_text}")
        if args.model:
            print(f"Model: {args.model}")

        # By default, wait for the task to complete and print the understanding result
        if not args.no_wait and task_id != 'N/A':
            understand_result = wait_for_understand(client, task_id, args.sub_app_id, args.max_wait)
            if understand_result:
                output_text = extract_output_text(understand_result)
                if output_text:
                    print(f"\n{'='*60}")
                    print(f"Image understanding result:")
                    print(f"{'='*60}")
                    print(output_text)
                    print(f"{'='*60}")

                if args.json:
                    print(json.dumps(understand_result, indent=2, ensure_ascii=False))

                return understand_result
        else:
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
        print(f"Image understanding failed: {e}")
        sys.exit(1)


def super_resolution_image(args):
    """Image super-resolution enhancement — advanced super-resolution via custom template + ProcessImageAsync
    Workflow: 1. Create super-resolution template (or use an existing one) → 2. Submit super-resolution task → 3. Wait for result  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
    """
    if not args.sub_app_id:
        print("Error: --sub-app-id is required for image super-resolution enhancement")
        sys.exit(1)

    # If the user provides a template ID directly, skip the template creation step
    if args.template_id:
        definition = args.template_id
        print(f"Using existing template Definition: {definition}")
    else:
        # Step 1: Build and create the super-resolution template
        template_params = build_super_resolution_template(args)

        if args.dry_run:
            print("[DRY RUN] Step 1 - Create super-resolution template request parameters:")
            print(json.dumps(template_params, indent=2, ensure_ascii=False))
            # Continue to show Step 2 parameters
            print("\n[DRY RUN] Step 2 - Submit super-resolution task request parameters:")
            task_params = {
                "SubAppId": args.sub_app_id,
                "FileId": args.file_id,
                "ImageTaskInput": {
                    "Definition": "<template ID returned from Step 1>"
                }
            }
            print(json.dumps(task_params, indent=2, ensure_ascii=False))
            return

        client = get_client(args.region)
        print("Step 1/3: Creating super-resolution template...")
        definition = create_super_resolution_template(client, template_params)
        print(f"✅ Template created successfully, Definition: {definition}")
        print("Waiting for template to take effect (10 seconds)...")
        time.sleep(10)

    if args.dry_run:
        return

    # Step 2: Submit the super-resolution task
    if not hasattr(args, '_client'):
        client = get_client(args.region)

    print(f"\nStep 2/3: Submitting image super-resolution task...")
    task_params = {
        "SubAppId": args.sub_app_id,
        "FileId": args.file_id,
        "ImageTaskInput": {
            "Definition": definition
        }
    }
    if args.session_id:
        task_params["SessionId"] = args.session_id
    if args.tasks_priority is not None:
        task_params["TasksPriority"] = args.tasks_priority

    try:
        req = models.ProcessImageAsyncRequest()
        req.from_json_string(json.dumps(task_params))

        resp = client.ProcessImageAsync(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get('TaskId', 'N/A')
        print(f"✅ Super-resolution task submitted, TaskId: {task_id}")

        # Step 3: Wait for the task to complete
        if not args.no_wait and task_id != 'N/A':
            print(f"\nStep 3/3: Waiting for super-resolution task to complete...")
            sr_result = wait_for_super_resolution(client, task_id, args.sub_app_id, args.max_wait)
            if sr_result:
                extract_super_resolution_output(sr_result)
                if args.json:
                    print(json.dumps(sr_result, indent=2, ensure_ascii=False))
                return sr_result
        else:
            print("Tip: Use the DescribeTaskDetail API to query the task result")
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
        print(f"Image super-resolution task failed: {e}")
        sys.exit(1)

def build_super_resolution_template(args):
    """Build super-resolution template parameters"""
    # Super-resolution configuration
    sr_config = {
        "Switch": "ON",
        "Type": args.sr_type,
    }

    if args.mode == 'percent':
        sr_config["Mode"] = "percent"
        sr_config["Percent"] = args.percent
    elif args.mode == 'fixed':
        sr_config["Mode"] = "fixed"
        if not args.width or not args.height:
            print("Error: fixed mode requires both --width and --height")
            sys.exit(1)
        sr_config["Width"] = args.width
        sr_config["Height"] = args.height
    elif args.mode == 'aspect':
        sr_config["Mode"] = "aspect"
        if not args.width or not args.height:
            print("Error: aspect mode requires both --width and --height")
            sys.exit(1)
        sr_config["Width"] = args.width
        sr_config["Height"] = args.height

    # Encoding configuration
    encode_config = {}
    if args.output_format:
        encode_config["Format"] = args.output_format
    if args.quality is not None:
        encode_config["Quality"] = args.quality

    # Assemble template
    process_image_configure = {
        "EnhanceConfig": {
            "AdvancedSuperResolution": sr_config
        }
    }
    if encode_config:
        process_image_configure["EncodeConfig"] = encode_config

    # Template name and description
    mode_desc = {
        'percent': f"{args.percent}x upscale",
        'fixed': f"{args.width}x{args.height} fixed resolution",
        'aspect': f"{args.width}x{args.height} aspect fit",
    }
    template_name = args.template_name or f"SR-Template-{args.sr_type}-{mode_desc[args.mode]}"
    template_comment = args.template_comment or f"Image {args.sr_type} super-resolution - {mode_desc[args.mode]}"

    template_params = {
        "ProcessImageConfigure": process_image_configure,
        "SubAppId": args.sub_app_id,
        "Name": template_name,
        "Comment": template_comment,
    }

    return template_params


def create_super_resolution_template(client, template_params):
    """Call CreateProcessImageAsyncTemplate to create a super-resolution template"""
    try:
        action = "CreateProcessImageAsyncTemplate"
        resp_str = client.call(action, template_params)
        result = json.loads(resp_str)

        if 'Response' in result and 'Definition' in result['Response']:
            return result['Response']['Definition']
        elif 'Response' in result and 'Error' in result['Response']:
            error = result['Response']['Error']
            print(f"Failed to create template: [{error.get('Code')}] {error.get('Message')}")
            sys.exit(1)
        else:
            print(f"Unexpected template creation response: {json.dumps(result, indent=2, ensure_ascii=False)}")
            sys.exit(1)
    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
        print(f"Failed to create super-resolution template: {e}")
        sys.exit(1)


def wait_for_super_resolution(client, task_id, sub_app_id=None, max_wait=300):
    """Wait for the image super-resolution task to complete"""
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
            elapsed = int(time.time() - start_time)
            print(f"  [{elapsed}s] Status: {status}")

            if status == 'FINISH':
                task_detail = result.get('ProcessImageAsyncTask') or {}
                err_code = task_detail.get('ErrCode', -1)
                if err_code == 0:
                    print("✅ Image super-resolution completed!")
                else:
                    print(f"❌ Image super-resolution failed: {task_detail.get('Message', 'Unknown error')}")
                return result
            elif status in ('FAIL', 'ABORTED'):
                print(f"❌ Task failed: {status}")
                return result

            time.sleep(3)
        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
            print(f"  Failed to query status: {e}")
            time.sleep(5)

    print(f"⏱️ Wait timed out ({max_wait}s), task is still running")
    return None


def extract_super_resolution_output(result):
    """Extract output information from the super-resolution task result"""
    task_detail = result.get('ProcessImageAsyncTask') or {}
    output = task_detail.get('Output') or {}
    file_info = output.get('FileInfo') or {}

    if file_info:
        print(f"\n{'='*60}")
        print(f"Image Super-Resolution Result:")
        print(f"{'='*60}")
        if file_info.get('FileId'):
            print(f"  FileId:     {file_info['FileId']}")
        if file_info.get('FileType'):
            print(f"  Format:     {file_info['FileType']}")
        if file_info.get('FileUrl'):
            print(f"  URL:        {file_info['FileUrl']}")

        meta = file_info.get('MetaData') or {}
        if meta:
            if meta.get('Width') and meta.get('Height'):
                print(f"  Resolution: {meta['Width']}x{meta['Height']}")
            if meta.get('Size'):
                size_mb = meta['Size'] / 1024 / 1024
                print(f"  File size:  {meta['Size']} bytes ({size_mb:.2f} MB)")
        print(f"{'='*60}")



def wait_for_understand(client, task_id, sub_app_id=None, max_wait=600):
    """Wait for the image understanding task to complete and return the full result"""
    print(f"\nWaiting for image understanding task to complete...")
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
            elapsed = int(time.time() - start_time)
            print(f"  [{elapsed}s] Status: {status}")

            if status == 'FINISH':
                task_detail = result.get('ProcessImageAsyncTask') or {}
                err_code = task_detail.get('ErrCode', -1)
                if err_code == 0:
                    print("✅ Image understanding completed!")
                else:
                    print(f"❌ Image understanding failed: {task_detail.get('Message', 'Unknown error')}")
                return result
            elif status in ('FAIL', 'ABORTED'):
                print(f"❌ Task failed: {status}")
                return result

            time.sleep(3)
        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
            print(f"  Failed to query status: {e}")
            time.sleep(5)

    print(f"⏱️ Wait timed out ({max_wait}s), task is still running")
    return None


def extract_output_text(result):
    """Extract OutputText from the image understanding task result"""
    task_detail = result.get('ProcessImageAsyncTask') or {}
    output = task_detail.get('Output') or {}
    return output.get('OutputText', '')


def wait_for_task(client, task_id, sub_app_id=None, max_wait=600):
    """Wait for a task to complete"""
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

            time.sleep(5)
        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
            print(f"Failed to query task status: {e}")
            time.sleep(5)

    print(f"⏱️ Wait timed out ({max_wait}s), task is still running")
    return None


def main():
    parser = argparse.ArgumentParser(
        description='VOD image processing tool (image super-resolution enhancement + image understanding)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Image super-resolution enhancement (default 2x advanced super-resolution, auto-wait for result)
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154

  # Super-resolution to fixed resolution 1920x1080
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154 \\
      --mode fixed --width 1920 --height 1080

  # Super-resolution using an existing template ID
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154 \\
      --template-id 7

  # Image understanding (default prompt "Understand this image", auto-wait for result)
  python vod_process_image.py understand --file-id <id> --sub-app-id 1500046154

  # Image understanding with custom prompt and specified model
  python vod_process_image.py understand --file-id <id> --sub-app-id 1500046154 \\
      --model gemini-2.5-pro --prompt "Analyze the composition and color palette of this image"

  # Image understanding using a template ID
  python vod_process_image.py understand --url 'https://example.com/img.jpg' --sub-app-id 1500046154 \\
      --template-id 10

Supported image understanding models: gemini-2.5-flash, gemini-2.5-flash-lite, gemini-2.5-pro, gemini-3-flash, gemini-3-pro
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # ---- understand subcommand (image understanding) ----
    understand_parser = subparsers.add_parser('understand', help='Image understanding (intelligent analysis using a large language model)')  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)

    # Input source (mutually exclusive, one required)
    understand_input = understand_parser.add_mutually_exclusive_group(required=True)
    understand_input.add_argument('--file-id', help='Image file FileId (mutually exclusive with --url and --base64)')
    understand_input.add_argument('--url', help='Image URL (mutually exclusive with --file-id and --base64)')
    understand_input.add_argument('--base64', help='Image Base64 encoding (mutually exclusive with --file-id and --url; file must be <4MB)')  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)

    # Image understanding parameters
    understand_parser.add_argument('--prompt', default='Understand this image',
                                   help='Prompt to guide the model in understanding the image (default: "Understand this image")')  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
    understand_parser.add_argument('--model', choices=[
        'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-2.5-pro',
        'gemini-3-flash', 'gemini-3-pro'
    ], help='Specify the large language model (default determined by the server)')

    # Output configuration
    understand_parser.add_argument('--output-name', help='Output file name')
    understand_parser.add_argument('--class-id', type=int, help='Category ID')
    understand_parser.add_argument('--expire-time', help='Expiration time in ISO 8601 format, e.g. 2025-12-31T23:59:59Z')  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)

    # Common parameters
    understand_parser.add_argument('--sub-app-id', type=int,
                                   default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                                   help='Sub-application ID (required)')
    understand_parser.add_argument('--session-id', help='Deduplication identifier; requests with the same ID within three days will return an error')  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
    understand_parser.add_argument('--session-context', help='Source context, passes through user request information')
    understand_parser.add_argument('--tasks-priority', type=int, help='Task priority, range -10 to 10')
    understand_parser.add_argument('--ext-info', help='Extended information (JSON string, e.g. to specify a model name)')  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
    understand_parser.add_argument('--region', default='ap-guangzhou', help='Region, default ap-guangzhou')
    understand_parser.add_argument('--no-wait', action='store_true',
                                   help='Submit task only, do not wait for result (default: auto-wait)')
    understand_parser.add_argument('--max-wait', type=int, default=120, help='Maximum wait time in seconds, default 120')  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
    understand_parser.add_argument('--json', action='store_true', help='Output in JSON format')
    understand_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters without executing')  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)

    # ---- super-resolution subcommand (image super-resolution enhancement) ----
    sr_parser = subparsers.add_parser('super-resolution',
        help='Image super-resolution enhancement (create a custom super-resolution template + submit a super-resolution task)',  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Super-resolution mode descriptions:
  percent  Upscale by a multiplier (default), e.g. --percent 2.0 means 2x upscale
  fixed    Output at a fixed resolution; requires --width and --height
  aspect   Aspect-fit super-resolution to the larger rectangle of the specified width/height, preserving aspect ratio

Super-resolution type descriptions:
  standard  General super-resolution, faster processing
  super     Advanced super-resolution, better quality but longer processing time

Examples:
  # 2x super-resolution (default advanced super-resolution, percent mode)
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154

  # Fixed-resolution super-resolution to 1920x1080
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154 \\
      --mode fixed --width 1920 --height 1080

  # Aspect-fit super-resolution to 4K
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154 \\
      --mode aspect --width 3840 --height 2160

  # Use an existing template
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154 \\
      --template-id 30023
        ''')

    sr_parser.add_argument('--file-id', required=True, help='Image file FileId (required)')

    # Super-resolution parameters
    sr_parser.add_argument('--mode', choices=['percent', 'fixed', 'aspect'], default='percent',
                           help='Super-resolution mode: percent=multiplier upscale (default), fixed=fixed resolution, aspect=aspect fit')  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
    sr_parser.add_argument('--percent', type=float, default=2.0,
                           help='Upscale multiplier, can be a decimal (used when mode=percent, default 2.0)')
    sr_parser.add_argument('--width', type=int,
                           help='Target image width, must not exceed 4096 (required when mode=fixed/aspect)')
    sr_parser.add_argument('--height', type=int,
                           help='Target image height, must not exceed 4096 (required when mode=fixed/aspect)')
    sr_parser.add_argument('--sr-type', choices=['standard', 'super'], default='super',
                           help='Super-resolution type: standard=general super-resolution, super=advanced super-resolution (default)')  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)

    # Output format
    sr_parser.add_argument('--output-format', choices=['JPEG', 'PNG', 'BMP', 'WebP'],
                           help='Output image format (default: same as source image)')
    sr_parser.add_argument('--quality', type=int,
                           help='Relative image quality (valid for JPEG/WebP, 1-100), default is source image quality')

    # Template options
    sr_parser.add_argument('--template-id', type=int,
                           help='Use an existing super-resolution template ID (skips template creation)')
    sr_parser.add_argument('--template-name', help='Custom template name')
    sr_parser.add_argument('--template-comment', help='Custom template description')

    # Common parameters
    sr_parser.add_argument('--sub-app-id', type=int,
                           default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                           help='Sub-application ID (required)')
    sr_parser.add_argument('--session-id', help='Deduplication identifier; requests with the same ID within three days will return an error')  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
    sr_parser.add_argument('--tasks-priority', type=int, help='Task priority, range -10 to 10')
    sr_parser.add_argument('--region', default='ap-guangzhou', help='Region, default ap-guangzhou')
    sr_parser.add_argument('--no-wait', action='store_true',
                           help='Submit task only, do not wait for result (default: auto-wait)')
    sr_parser.add_argument('--max-wait', type=int, default=300,
                           help='Maximum wait time in seconds, default 300')
    sr_parser.add_argument('--json', action='store_true', help='Output in JSON format')
    sr_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters without executing')

    args = parser.parse_args()

    if args.command == 'understand':
        understand_image(args)
    elif args.command == 'super-resolution':
        super_resolution_image(args)
    else:
        parser.print_help()



if __name__ == '__main__':
    main()
