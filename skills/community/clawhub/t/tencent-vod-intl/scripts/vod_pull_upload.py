#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD URL Pull Upload Script
Supports pulling media files from URLs and uploading them to Cloud VOD
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
    """Get Tencent Cloud authentication credentials"""
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


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def resolve_sub_app_id(client, app_name):
    """Fuzzy match sub-application ID by application name/description/tag.

    Queries the full list of sub-applications and performs fuzzy matching
    against name, description, and tag values.
    - Exact name match takes priority
    - Falls back to fuzzy match on name, description, and tags
    - Returns directly if a unique match is found
    - Lists all matches and exits if multiple are found
    - Exits with an error if no match is found
    """
    print(f"Querying sub-application list, matching keyword: '{app_name}' ...")

    # Paginate through all sub-applications
    all_apps = []
    offset = 0
    limit = 200
    while True:
        req = models.DescribeSubAppIdsRequest()
        req.Offset = offset
        req.Limit = limit
        try:
            resp = client.DescribeSubAppIds(req)
            result = json.loads(resp.to_json_string())
        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
            print(f"Failed to query sub-application list: {e}")
            sys.exit(1)

        items = result.get("SubAppIdInfoSet", [])
        all_apps.extend(items)
        total = result.get("TotalCount", 0)
        if len(all_apps) >= total or not items:
            break
        offset += limit

    if not all_apps:
        print("Error: No sub-applications found under the current account")
        sys.exit(1)

    keyword = app_name.lower()

    # 1) Exact name match
    exact = [a for a in all_apps
             if (a.get("SubAppIdName") or a.get("Name") or "").lower() == keyword]
    if len(exact) == 1:
        matched = exact[0]
        sub_id = matched.get("SubAppId")
        name = matched.get("SubAppIdName") or matched.get("Name") or "N/A"
        print(f"✅ Exact match found: {name} (SubAppId: {sub_id})")
        return sub_id

    # 2) Fuzzy match (name, description, tag values)
    fuzzy = []
    for a in all_apps:
        name = (a.get("SubAppIdName") or a.get("Name") or "").lower()
        desc = (a.get("Description") or "").lower()
        tag_values = " ".join(
            (t.get("TagValue", "") + " " + t.get("TagKey", ""))
            for t in (a.get("Tags") or [])
        ).lower()

        if keyword in name or keyword in desc or keyword in tag_values:
            fuzzy.append(a)

    if not fuzzy:
        print(f"Error: No sub-application matching '{app_name}' was found.")
        print("Available sub-applications:")
        for a in all_apps:
            n = a.get("SubAppIdName") or a.get("Name") or "N/A"
            sid = a.get("SubAppId", "N/A")
            d = a.get("Description") or ""
            print(f"  - {n} (SubAppId: {sid}){' — ' + d if d else ''}")
        sys.exit(1)

    if len(fuzzy) == 1:
        matched = fuzzy[0]
        sub_id = matched.get("SubAppId")
        name = matched.get("SubAppIdName") or matched.get("Name") or "N/A"
        desc = matched.get("Description") or ""
        print(f"✅ Match found: {name} (SubAppId: {sub_id}){' — ' + desc if desc else ''}")
        return sub_id

    # Multiple matches
    print(f"Found {len(fuzzy)} matching sub-applications. Please specify the exact application ID via --sub-app-id:")
    for a in fuzzy:
        n = a.get("SubAppIdName") or a.get("Name") or "N/A"
        sid = a.get("SubAppId", "N/A")
        d = a.get("Description") or ""
        print(f"  - {n} (SubAppId: {sid}){' — ' + d if d else ''}")
    sys.exit(1)

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)

def pull_upload(args):
    """URL pull upload"""
    client = get_client(args.region)

    # Resolve Sub AppId from application name
    if args.app_name:
        if args.sub_app_id:
            print("Error: --app-name and --sub-app-id cannot be specified at the same time")
            sys.exit(1)
        args.sub_app_id = resolve_sub_app_id(client, args.app_name)

    req = models.PullUploadRequest()
    req.MediaUrl = args.url

    if args.media_name:
        req.MediaName = args.media_name
    if args.media_type:
        req.MediaType = args.media_type
    if args.cover_url:
        req.CoverUrl = args.cover_url
    if args.procedure:
        req.Procedure = args.procedure
    if args.expire_time:
        req.ExpireTime = args.expire_time
    if args.storage_region:
        req.StorageRegion = args.storage_region
    if args.class_id is not None:
        req.ClassId = args.class_id
    if args.tasks_priority is not None:
        req.TasksPriority = args.tasks_priority
    if args.session_context:
        req.SessionContext = args.session_context
    if args.session_id:
        req.SessionId = args.session_id
    if args.ext_info:
        req.ExtInfo = args.ext_info
    if args.source_context:
        req.SourceContext = args.source_context
    if args.media_storage_path:
        req.MediaStoragePath = args.media_storage_path
    if args.sub_app_id:
        req.SubAppId = args.sub_app_id

    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return

    try:
        resp = client.PullUpload(req)
        result = json.loads(resp.to_json_string())

        print(f"Pull upload task submitted successfully!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")
        print(f"FileId: {result.get('FileId', 'N/A')}")

        # Wait for task completion if needed
        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(long SDK parameter or URL string)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        print(f"Pull upload failed: {e}")
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

            if status == 'FINISH':
                print("Task completed!")
                pull_task = result.get('PullUploadTask') or {}
                if pull_task:
                    file_id = pull_task.get('FileId', 'N/A')
                    print(f"  FileId: {file_id}")
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
        description='VOD URL Pull Upload Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic pull upload
  python vod_pull_upload.py --url "https://example.com/video.mp4"

  # Specify media name and cover
  python vod_pull_upload.py --url "https://example.com/video.mp4" --media-name "My Video" --cover-url "https://example.com/cover.jpg"

  # Automatically run a task flow after pull upload
  python vod_pull_upload.py --url "https://example.com/video.mp4" --procedure "SimpleAes"

  # Specify storage region and category
  python vod_pull_upload.py --url "https://example.com/video.mp4" --storage-region "ap-chongqing" --class-id 100

  # Set expiration time
  python vod_pull_upload.py --url "https://example.com/video.mp4" --expire-time "2025-12-31T23:59:59Z"

  # Wait for task completion
  python vod_pull_upload.py --url "https://example.com/video.mp4"  # waits by default

  # Submit task only, do not wait
  python vod_pull_upload.py --url "https://example.com/video.mp4" --no-wait

  # Preview request parameters (dry run, no actual execution)
  python vod_pull_upload.py --url "https://example.com/video.mp4" --dry-run
        '''
    )

    parser.add_argument('--url', required=True, help='Media URL (required)')
    parser.add_argument('--media-name', help='Media name')
    parser.add_argument('--media-type', help='Media type (mp4, mp3, jpg, etc.)')
    parser.add_argument('--cover-url', help='Cover image URL')
    parser.add_argument('--procedure', help='Task flow name, executed automatically after upload')
    parser.add_argument('--expire-time', help='Media file expiration time in ISO 8601 format, e.g. 2025-12-31T23:59:59Z')  # NOCA:line-too-long(long SDK parameter or URL string)
    parser.add_argument('--storage-region', help='Specify storage region, e.g. ap-chongqing')
    parser.add_argument('--class-id', type=int, help='Category ID, default 0 (other categories)')
    parser.add_argument('--tasks-priority', type=int, help='Task priority, range -10 to 10, default 0')
    parser.add_argument('--session-context', help='Session context, passes through user request info, max 1000 characters')  # NOCA:line-too-long(long SDK parameter or URL string)
    parser.add_argument('--session-id', help='Deduplication identifier, requests with the same ID within 3 days will return an error, max 50 characters')  # NOCA:line-too-long(long SDK parameter or URL string)
    parser.add_argument('--ext-info', help='Reserved field, used for special purposes')
    parser.add_argument('--source-context', help='Source context, passes through user request info, max 250 characters')
    parser.add_argument('--media-storage-path', help='Media storage path, must start with /, only available for sub-applications in FileID+Path mode')  # NOCA:line-too-long(long SDK parameter or URL string)
    parser.add_argument('--sub-app-id', type=int,
                        default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                        help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long SDK parameter or URL string)
    parser.add_argument('--app-name', help='Fuzzy match sub-application by name/description (mutually exclusive with --sub-app-id)')  # NOCA:line-too-long(long SDK parameter or URL string)
    parser.add_argument('--region', default='ap-guangzhou', help='Region, default ap-guangzhou')
    parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time in seconds, default 600')
    parser.add_argument('--json', action='store_true', help='Output full response in JSON format')
    parser.add_argument('--dry-run', action='store_true', help='Preview request parameters, do not actually execute')

    args = parser.parse_args()
    pull_upload(args)


if __name__ == '__main__':
    main()
