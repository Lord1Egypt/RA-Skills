#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD AIGC Advanced Custom Element Creation Script
Based on the CreateAigcAdvancedCustomElement API

Features:
  - Create AIGC advanced custom elements (video character elements / multi-image elements)
  - Support interactive guided input (--interactive)
  - Automatically record to mem/elements.json upon successful creation
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime

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
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.common.common_client import CommonClient
except ImportError:
    print("Error: Please install the Tencent Cloud SDK first: pip install tencentcloud-sdk-python")
    sys.exit(1)


# ─────────────────────────────────────────────
# Utility Functions
# ─────────────────────────────────────────────

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
    """Get VOD CommonClient (supports new APIs not yet included in the SDK)"""
    cred = get_credential()
    http_profile = HttpProfile()
    http_profile.endpoint = "vod.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return CommonClient("vod", "2018-07-17", cred, region, client_profile)


def get_mem_path():
    """Get the path to mem/elements.json"""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mem_dir = os.path.join(skill_dir, "mem")
    os.makedirs(mem_dir, exist_ok=True)
    return os.path.join(mem_dir, "elements.json")


def save_element_record(record: dict):
    """Write a creation record to mem/elements.json (upsert by task_id as unique key)"""
    mem_path = get_mem_path()
    elements = []
    if os.path.exists(mem_path):
        try:
            with open(mem_path, "r", encoding="utf-8") as f:
                elements = json.load(f)
            if not isinstance(elements, list):
                elements = []
        except (json.JSONDecodeError, IOError):
            elements = []

    task_id = record.get("task_id")
    matched = False
    for rec in elements:
        if rec.get("task_id") == task_id:
            rec.update(record)
            matched = True
            break
    if not matched:
        elements.append(record)

    with open(mem_path, "w", encoding="utf-8") as f:
        json.dump(elements, f, ensure_ascii=False, indent=2)

    return mem_path


def prompt_input(prompt_text, max_len=None, required=True, default=None, choices=None):
    """Interactive input helper function"""
    while True:
        suffix = ""
        if default:
            suffix += f" [Default: {default}]"
        if choices:
            suffix += f"\n   Available values: {' / '.join(choices)}"
        if max_len:
            suffix += f" (max {max_len} characters)"

        val = input(f"{prompt_text}{suffix}: ").strip()

        if not val:
            if default:
                return default
            if not required:
                return None
            print("  ⚠️  This field is required. Please enter a value.")
            continue

        if max_len and len(val) > max_len:
            print(f"  ⚠️  Input exceeds the {max_len}-character limit (current: {len(val)} characters). Please re-enter.")
            continue

        if choices and val not in choices:
            print(f"  ⚠️  Please enter a valid value: {' / '.join(choices)}")
            continue

        return val


def prompt_list_input(prompt_text, required=False):
    """Interactive list input (comma-separated), returns a list"""
    val = input(f"{prompt_text} (separate multiple entries with commas; press Enter to skip): ").strip()
    if not val:
        if required:
            print("  ⚠️  This field is required. Please enter a value.")
            return prompt_list_input(prompt_text, required=True)
        return []
    return [v.strip() for v in val.split(",") if v.strip()]


# ─────────────────────────────────────────────
# Interactive Guide
# ─────────────────────────────────────────────

def interactive_guide():
    """Interactively guide the user to enter the parameters required to create an element"""
    print("\n" + "=" * 60)
    print("  VOD AIGC Advanced Custom Element Creation Wizard")
    print("=" * 60)
    print("This wizard will guide you step by step through the information needed to create an element.\n")

    params = {}

    # ── 1. Element Name ──
    print("[1/7]Element Name (ElementName)")
    print("  Description: A unique identifier name for the element. Choose a descriptive name that reflects its function for easy future lookup.")
    params["element_name"] = prompt_input("  Enter element name", max_len=20, required=True)

    # ── 2. Element Description ──
    print("\n[2/7]Element Description (ElementDescription)")
    print("  Description: A detailed description of the element's functionality to help quickly understand its purpose later.")
    params["element_description"] = prompt_input("  Enter element description", max_len=100, required=True)

    # ── 3. Reference Type ──
    print("\n[3/7]Element Reference Type (ReferenceType)")
    print("  Description: Determines the element customization method; different methods have different availability:")
    print("    video_refer  —— Video character element: defines appearance via a reference video; supports voice binding")
    print("    image_refer  —— Multi-image element: defines appearance via multiple images; does not support voice binding")
    params["reference_type"] = prompt_input(
        "  Select reference type", required=True,
        choices=["video_refer", "image_refer"]
    )

    # ── 4. Element VoiceId (video_refer only) ──
    if params["reference_type"] == "video_refer":
        print("\n[4/7]Element Voice (ElementVoiceId)")
        print("  Description: You can bind an existing voice ID from the voice library. Leave blank to skip voice binding.")
        print("  Note: Only video-customized elements (video_refer) support voice binding.")
        val = input("  Enter voice ID (leave blank to skip): ").strip()
        params["element_voice_id"] = val if val else None
    else:
        print("\n[4/7]Element Voice (ElementVoiceId)")
        print("  Description: Multi-image elements (image_refer) do not support voice binding. This step has been skipped automatically.")
        params["element_voice_id"] = None

    # ── 5. Element Video List / Element Image List ──
    if params["reference_type"] == "video_refer":
        print("\n[5/7]Element Reference Video List (ElementVideoList)")
        print("  Description: Define the element's appearance via video. Videos with audio (containing human voice) will automatically trigger voice customization.")
        print("  Format requirements:")
        print("    - Only MP4/MOV formats are supported")
        print("    - Duration: 3s–8s, aspect ratio 16:9 or 9:16, 1080P")
        print("    - Maximum 1 video, file size no more than 200MB")
        print("  Enter video URL (video_url):")
        video_urls = prompt_list_input("  Video URL", required=True)
        # Build JSON format
        refer_videos = [{"video_url": url} for url in video_urls]
        params["element_video_list"] = json.dumps({"refer_videos": refer_videos}, ensure_ascii=False)
        params["element_image_list"] = None
    else:
        print("\n[5/7]Element Reference Image List (ElementImageList)")
        print("  Description: Define the element's appearance via multiple images.")
        print("  Requirements:")
        print("    - At least 1 frontal reference image (frontal_image)")
        print("    - 1–3 additional reference images from other angles or close-ups (refer_images), must differ from the frontal image")

        frontal = input("  Enter frontal reference image URL (frontal_image): ").strip()
        while not frontal:
            print("  ⚠️  Frontal reference image is required.")
            frontal = input("  Enter frontal reference image URL (frontal_image): ").strip()

        print("  Enter other reference image URLs (1–3 images, separate multiple with commas):")
        other_urls = prompt_list_input("  Other reference image URLs", required=False)

        refer_images = [{"image_url": url} for url in other_urls[:3]]
        img_payload = {"frontal_image": frontal}
        if refer_images:
            img_payload["refer_images"] = refer_images

        params["element_image_list"] = json.dumps(img_payload, ensure_ascii=False)
        params["element_video_list"] = None

    # ── 6. Tag List ──
    print("\n[6/7]Tag List (TagList)")
    print("  Description: Configure tags for the element to facilitate categorized management. Tag ID format examples: o_101, o_102.")
    tag_ids = prompt_list_input("  Tag IDs", required=False)
    if tag_ids:
        params["tag_list"] = json.dumps([{"tag_id": t} for t in tag_ids], ensure_ascii=False)
    else:
        params["tag_list"] = None

    # ── 7. Sub AppId ──
    print("\n[7/7]Sub-Application ID (SubAppId)")
    print("  Description: VOD sub-application ID. Required for users who activated VOD after 2023-12-25.")
    env_sub = os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", "")
    default_sub = env_sub if env_sub else None
    val = input(f"  Enter sub-application ID{' [Environment variable configured: ' + env_sub + ']' if env_sub else ' (required)'}: ").strip()
    if val:
        params["sub_app_id"] = int(val)
    elif default_sub:
        params["sub_app_id"] = int(default_sub)
    else:
        print("  ⚠️  Sub-application ID is required. Please re-enter.")
        val = input("  Enter sub-application ID: ").strip()
        params["sub_app_id"] = int(val)

    print("\n" + "=" * 60)
    print("  Parameter Confirmation")
    print("=" * 60)
    print(f"  Element Name       : {params['element_name']}")
    print(f"  Element Description: {params['element_description']}")
    print(f"  Reference Type     : {params['reference_type']}")
    print(f"  Voice ID           : {params['element_voice_id'] or '(none)'}")
    if params.get("element_video_list"):
        print(f"  Reference Video    : {params['element_video_list']}")
    if params.get("element_image_list"):
        print(f"  Reference Images   : {params['element_image_list']}")
    print(f"  Tags               : {params['tag_list'] or '(none)'}")
    print(f"  Sub-Application ID : {params['sub_app_id']}")
    print("=" * 60)

    confirm = input("\nConfirm the above information and submit for creation? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Creation cancelled.")
        sys.exit(0)

    return params



# ─────────────────────────────────────────────
# Core Functions
# ─────────────────────────────────────────────

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def create_element(args):
    """Call the CreateAigcAdvancedCustomElement API to create an element"""
    # Required parameter validation
    if not args.sub_app_id:
        print("Error: --sub-app-id must be specified or the environment variable TENCENTCLOUD_VOD_SUB_APP_ID must be set")
        sys.exit(1)

    if not args.element_name:
        print("Error: --element-name must be specified")
        sys.exit(1)

    if not args.element_description:
        print("Error: --element-description must be specified")
        sys.exit(1)

    if not args.reference_type:
        print("Error: --reference-type must be specified (video_refer or image_refer)")
        sys.exit(1)

    # Build request body
    req_body = {
        "SubAppId": args.sub_app_id,
        "ElementName": args.element_name,
        "ElementDescription": args.element_description,
        "ReferenceType": args.reference_type,
    }

    if args.element_voice_id:
        req_body["ElementVoiceId"] = args.element_voice_id

    if args.element_video_list:
        req_body["ElementVideoList"] = args.element_video_list

    if args.element_image_list:
        req_body["ElementImageList"] = args.element_image_list

    if args.tag_list:
        req_body["TagList"] = args.tag_list

    if args.session_id:
        req_body["SessionId"] = args.session_id

    if args.session_context:
        req_body["SessionContext"] = args.session_context

    if args.tasks_priority is not None:
        req_body["TasksPriority"] = args.tasks_priority

    if args.dry_run:
        print("[DRY RUN] Request parameter preview:")
        print(json.dumps(req_body, indent=2, ensure_ascii=False))
        return

    client = get_client(args.region)

    try:
        resp = client.call_json("CreateAigcAdvancedCustomElement", req_body)
        result = resp.get("Response", resp)

        task_id = result.get("TaskId", "N/A")
        request_id = result.get("RequestId", "N/A")

        print("\n" + "=" * 60)
        print("✅ AIGC advanced custom element creation task submitted!")
        print("=" * 60)
        print(f"  TaskId     : {task_id}")
        print(f"  RequestId  : {request_id}")
        print("=" * 60)

        # Save record to mem/elements.json
        record = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task_id": task_id,
            "request_id": request_id,
            "sub_app_id": args.sub_app_id,
            "element_name": args.element_name,
            "element_description": args.element_description,
            "reference_type": args.reference_type,
            "element_voice_id": args.element_voice_id or None,
            "element_video_list": args.element_video_list or None,
            "element_image_list": args.element_image_list or None,
            "tag_list": args.tag_list or None,
            "session_id": args.session_id or None,
            "session_context": args.session_context or None,
            "tasks_priority": args.tasks_priority,
        }
        save_element_record(record)

        # Wait for task completion (wait by default)
        if not args.no_wait and task_id != "N/A":
            wait_result = wait_for_task(client, task_id, args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {task_id}")

        if args.json:
            print("\nJSON Response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result

    except TencentCloudSDKException as e:
        print(f"Failed to create element: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def list_elements(args):
    """List locally recorded element information"""
    mem_path = get_mem_path()
    if not os.path.exists(mem_path):
        print("No element creation records found.")
        return

    with open(mem_path, "r", encoding="utf-8") as f:
        elements = json.load(f)

    if not elements:
        print("No element creation records found.")
        return

    if args.json:
        print(json.dumps(elements, indent=2, ensure_ascii=False))
        return

    print(f"\nTotal {len(elements)} element creation record(s):\n")
    for i, elem in enumerate(elements, 1):
        print(f"[{i}] Element Name : {elem.get('element_name', 'N/A')}")
        print(f"    Created At  : {elem.get('created_at', 'N/A')}")
        print(f"    TaskId      : {elem.get('task_id', 'N/A')}")
        print(f"    Description : {elem.get('element_description', 'N/A')}")
        print(f"    Ref Type    : {elem.get('reference_type', 'N/A')}")
        print(f"    Tags        : {elem.get('tag_list', '(none)')}")
        print()


def wait_for_task(client, task_id, sub_app_id=None, max_wait=600):
    """Wait for task completion"""
    print(f"\nWaiting for task to complete (TaskId: {task_id})...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            req = {
                "TaskId": task_id
            }
            if sub_app_id:
                req["SubAppId"] = sub_app_id
                
            resp = client.call_json("DescribeTaskDetail", req)
            result = resp.get("Response", resp)
            
            status = result.get("Status", "PROCESSING")
            elapsed = int(time.time() - start_time)
            print(f"  [{elapsed}s] Status: {status}")
            
            if status == "FINISH":
                print("✅ Task completed!")
                return result
            elif status == "FAIL":
                err_msg = result.get("Message", "Unknown error")
                print(f"❌ Task failed: {err_msg}")
                return result
            
            time.sleep(5)
        except Exception as e:
            print(f"Failed to query task status: {e}")
            time.sleep(5)
    
    print(f"⏱️ Wait timed out ({max_wait}s), task is still running")
    return None


# ─────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="VOD AIGC Advanced Custom Element Creation Tool\nBased on the CreateAigcAdvancedCustomElement API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive guided creation (recommended)
  python vod_create_aigc_advanced_custom_element.py create --interactive

  # Direct command-line creation (multi-image element)
  python vod_create_aigc_advanced_custom_element.py create \\
    --sub-app-id 1500046725 \\
    --element-name "My Element" \\
    --element-description "An element for product display" \\
    --reference-type image_refer \\
    --element-image-list '{"frontal_image":"https://example.com/front.jpg","refer_images":[{"image_url":"https://example.com/side.jpg"}]}' \\
    --tag-list '[{"tag_id":"o_101"}]'

  # Direct command-line creation (video character element)
  python vod_create_aigc_advanced_custom_element.py create \\
    --sub-app-id 1500046725 \\
    --element-name "Video Element A" \\
    --element-description "A character element customized from video" \\
    --reference-type video_refer \\
    --element-video-list '{"refer_videos":[{"video_url":"https://example.com/ref.mp4"}]}' \\
    --element-voice-id "123333"

  # Preview request parameters (without actual execution)
  python vod_create_aigc_advanced_custom_element.py create \\
    --element-name "Test" --element-description "Test description" \\
    --reference-type image_refer --sub-app-id 1500046725 --dry-run

  # View locally created element records
  python vod_create_aigc_advanced_custom_element.py list

Reference type description:
  video_refer  —— Video character element, defines appearance via reference video, supports binding a voice
  image_refer  —— Multi-image element, defines appearance via multiple images, does not support binding a voice
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # ── create subcommand ──
    create_parser = subparsers.add_parser("create", help="Create an AIGC advanced custom element")

    create_parser.add_argument(
        "--interactive", "-i", action="store_true",
        help="Enable interactive guided mode, prompting for each parameter step by step (recommended for new users)"
    )

    # Required parameters (non-interactive mode)
    create_parser.add_argument(
        "--sub-app-id", type=int,
        default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
        help="VOD application ID (required; can also be set via the environment variable TENCENTCLOUD_VOD_SUB_APP_ID)"
    )
    create_parser.add_argument(
        "--element-name",
        help="Element name, must not exceed 20 characters (required)"
    )
    create_parser.add_argument(
        "--element-description",
        help="Element description, must not exceed 100 characters (required)"
    )
    create_parser.add_argument(
        "--reference-type",
        choices=["video_refer", "image_refer"],
        help="Element reference type: video_refer (video character element) / image_refer (multi-image element) (required)"
    )

    # Optional parameters
    create_parser.add_argument(
        "--element-voice-id",
        help="Element voice ID, binds an existing voice from the voice library. Only supported for video_refer type. Leave empty to not bind a voice."
    )
    create_parser.add_argument(
        "--element-video-list",
        help=(
            "Element reference videos (JSON string). Required when reference type is video_refer.\n"
            'Format: \'{"refer_videos":[{"video_url":"https://..."}]}\''
        )
    )
    create_parser.add_argument(
        "--element-image-list",
        help=(
            "Element reference images (JSON string). Required when reference type is image_refer.\n"
            'Format: \'{"frontal_image":"https://...","refer_images":[{"image_url":"https://..."}]}\''
        )
    )
    create_parser.add_argument(
        "--tag-list",
        help=(
            "Element tag list (JSON string).\n"
            'Format: \'[{"tag_id":"o_101"},{"tag_id":"o_102"}]\''
        )
    )
    create_parser.add_argument(
        "--session-id",
        help="Deduplication identifier (max 50 characters; returns an error if duplicated within 3 days)"
    )
    create_parser.add_argument(
        "--session-context",
        help="Source context for passing through user request information (max 1000 characters)"
    )
    create_parser.add_argument(
        "--tasks-priority", type=int,
        help="Task priority (-10 to 10, higher value means higher priority, default 0)"
    )

    # Common parameters
    create_parser.add_argument("--region", default="ap-guangzhou", help="Region (default: ap-guangzhou)")
    create_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    create_parser.add_argument("--dry-run", action="store_true", help="Preview request parameters without actual execution")
    create_parser.add_argument("--no-wait", action="store_true", help="Submit task only, do not wait for result")
    create_parser.add_argument("--max-wait", type=int, default=600, help="Maximum wait time in seconds, default 600")

    # ── list subcommand ──
    list_parser = subparsers.add_parser("list", help="View locally created element records (mem/elements.json)")
    list_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    if args.command == "create":
        if args.interactive:
            # Interactive guided mode
            params = interactive_guide()
            # Merge guided results into args
            args.sub_app_id = params["sub_app_id"]
            args.element_name = params["element_name"]
            args.element_description = params["element_description"]
            args.reference_type = params["reference_type"]
            args.element_voice_id = params.get("element_voice_id")
            args.element_video_list = params.get("element_video_list")
            args.element_image_list = params.get("element_image_list")
            args.tag_list = params.get("tag_list")
            if not hasattr(args, "session_id"):
                args.session_id = None
            if not hasattr(args, "session_context"):
                args.session_context = None
            if not hasattr(args, "tasks_priority"):
                args.tasks_priority = None
            if not hasattr(args, "dry_run"):
                args.dry_run = False
            if not hasattr(args, "json"):
                args.json = False

        create_element(args)

    elif args.command == "list":
        list_elements(args)

    else:
        parser.print_help()



if __name__ == "__main__":
    main()
