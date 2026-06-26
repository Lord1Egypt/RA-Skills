#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD Media Upload Script
Supports local file upload (using the official vod-python-sdk, automatically handles ApplyUpload → COS upload →
CommitUpload)
and URL pull upload (PullUpload)

Note: For URL pull upload, it is recommended to use the dedicated script vod_pull_upload.py, which has more complete
functionality.
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path

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
except ImportError as e:
    print(f"Error: Please install dependencies first: pip install tencentcloud-sdk-python")
    sys.exit(1)

try:
    from qcloud_vod.vod_upload_client import VodUploadClient
    from qcloud_vod.model import VodUploadRequest
except ImportError:
    print("Error: Please install dependencies first: pip install vod-python-sdk")
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


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def resolve_sub_app_id(client, app_name):
    """Fuzzy match sub-application ID by application name/description/tag.

    Queries the full list of sub-applications and performs fuzzy matching on Name, Description, and Tag values.
    - Exact name match takes priority
    - Then fuzzy match on name, description, and tags
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
def upload_media(args):
    """Upload local media file (using the official vod-python-sdk)"""
    if not os.path.exists(args.file):
        print(f"Error: File does not exist: {args.file}")
        sys.exit(1)

    # Resolve Sub AppId by application name (requires VOD API client; credentials only needed when not dry-run)
    if args.app_name:
        if args.sub_app_id:
            print("Error: --app-name and --sub-app-id cannot be specified at the same time")
            sys.exit(1)
        if not args.dry_run:
            client = get_client(args.region)
            args.sub_app_id = resolve_sub_app_id(client, args.app_name)

    # Build upload request
    request = VodUploadRequest()
    request.MediaFilePath = os.path.abspath(args.file)
    request.MediaType = args.media_type or Path(args.file).suffix.lstrip('.').lower()
    if not request.MediaType:
        print("Error: Cannot infer media type. Please specify it with --media-type")
        sys.exit(1)

    request.MediaName = args.media_name or Path(args.file).stem

    if args.cover_file:
        if not os.path.exists(args.cover_file):
            print(f"Error: Cover file does not exist: {args.cover_file}")
            sys.exit(1)
        request.CoverFilePath = os.path.abspath(args.cover_file)
        if args.cover_type:
            request.CoverType = args.cover_type

    if args.class_id is not None:
        request.ClassId = args.class_id
    if args.procedure:
        request.Procedure = args.procedure
    if args.expire_time:
        request.ExpireTime = args.expire_time
    if args.storage_region:
        request.StorageRegion = args.storage_region
    if args.source_context:
        request.SourceContext = args.source_context
    if args.sub_app_id:
        request.SubAppId = args.sub_app_id
    if args.concurrent_upload_number:
        request.ConcurrentUploadNumber = args.concurrent_upload_number
    if args.media_storage_path:
        request.MediaStoragePath = args.media_storage_path

    if args.dry_run:
        print("[DRY RUN] VodUploadRequest parameters:")
        params = {
            "MediaFilePath": request.MediaFilePath,
            "MediaType": request.MediaType,
            "MediaName": request.MediaName,
        }
        if request.CoverFilePath:
            params["CoverFilePath"] = request.CoverFilePath
        if request.CoverType:
            params["CoverType"] = request.CoverType
        if request.ClassId is not None:
            params["ClassId"] = request.ClassId
        if request.Procedure:
            params["Procedure"] = request.Procedure
        if request.ExpireTime:
            params["ExpireTime"] = request.ExpireTime
        if request.StorageRegion:
            params["StorageRegion"] = request.StorageRegion
        if request.SourceContext:
            params["SourceContext"] = request.SourceContext
        if request.SubAppId:
            params["SubAppId"] = request.SubAppId
        if request.ConcurrentUploadNumber:
            params["ConcurrentUploadNumber"] = request.ConcurrentUploadNumber
        if request.MediaStoragePath:
            params["MediaStoragePath"] = request.MediaStoragePath
        print(json.dumps(params, indent=2, ensure_ascii=False))
        print(f"\nUpload region: {args.region}")
        return

    # Get credentials
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print("Error: Please set environment variables TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY")
        sys.exit(1)

    file_size = os.path.getsize(args.file)
    print(f"Uploading file: {args.file}")
    print(f"File size: {file_size / 1024 / 1024:.2f} MB")
    print(f"Upload region: {args.region}")

    # Use the official SDK to upload (internally handles Apply Upload → COS signed upload → Commit Upload automatically)
    upload_client = VodUploadClient(secret_id, secret_key)

    try:
        print("Starting upload (SDK automatically handles multipart upload and signature authentication)...")
        response = upload_client.upload(args.region, request)

        file_id = response.FileId or "N/A"
        media_url = response.MediaUrl or "N/A"
        cover_url = response.CoverUrl or ""

        print(f"\n✅ Upload successful!")
        if args.sub_app_id:
            print(f"SubAppId: {args.sub_app_id}")
        print(f"FileId:   {file_id}")
        print(f"MediaUrl: {media_url}")
        if cover_url:
            print(f"CoverUrl: {cover_url}")

        result = {
            "FileId": file_id,
            "MediaUrl": media_url,
        }
        if args.sub_app_id:
            result["SubAppId"] = args.sub_app_id
        if cover_url:
            result["CoverUrl"] = cover_url

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        print(f"Upload failed: {e}")
        sys.exit(1)

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)

def pull_upload(args):
    """URL pull upload"""
    # Resolve Sub AppId by application name
    if args.app_name:
        if args.sub_app_id:
            print("Error: --app-name and --sub-app-id cannot be specified at the same time")
            sys.exit(1)
        if not args.dry_run:
            client = get_client(args.region)
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
        print("[DRY RUN] PullUpload request parameters:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return

    client = get_client(args.region)

    try:
        resp = client.PullUpload(req)
        result = json.loads(resp.to_json_string())

        print(f"Pull upload task submitted!")
        if args.sub_app_id:
            print(f"SubAppId: {args.sub_app_id}")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")
        print(f"FileId: {result.get('FileId', 'N/A')}")

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
    """Wait for task to complete"""
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
                    print(f"  FileId: {pull_task.get('FileId', 'N/A')}")
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
        description='VOD media upload tool (local upload + URL pull upload)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Upload a local video file
  python vod_upload.py upload --file /path/to/video.mp4

  # Upload with a specified media name and category
  python vod_upload.py upload --file /path/to/video.mp4 --media-name "My Video" --class-id 100

  # Upload and automatically execute a task flow
  python vod_upload.py upload --file /path/to/video.mp4 --procedure "LongVideoPreset"

  # Upload with an expiration time
  python vod_upload.py upload --file /path/to/video.mp4 --expire-time "2025-12-31T23:59:59Z"

  # URL pull upload
  python vod_upload.py pull --url "https://example.com/video.mp4"

  # URL pull upload with a specified name and cover
  python vod_upload.py pull --url "https://example.com/video.mp4" \\
      --media-name "My Video" --cover-url "https://example.com/cover.jpg"

  # URL pull upload and wait for completion
  python vod_upload.py pull --url "https://example.com/video.mp4"  # waits for completion by default
  
  # Do not wait, only submit the pull task
  python vod_upload.py pull --url "https://example.com/video.mp4" --no-wait

  # Preview request parameters (without actually executing)
  python vod_upload.py upload --file /path/to/video.mp4 --dry-run
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # ---- upload subcommand (local file upload) ----
    upload_parser = subparsers.add_parser('upload', help='Upload local file (using the official vod-python-sdk)')
    upload_parser.add_argument('--file', required=True, help='Local file path (required)')
    upload_parser.add_argument('--media-name', help='Media name, defaults to the filename (without extension)')
    upload_parser.add_argument('--media-type', help='Media type (mp4, mp3, jpg, etc.), inferred from file extension by default')  # NOCA:line-too-long(long SDK parameter or URL string)
    upload_parser.add_argument('--cover-file', help='Local cover image file path')
    upload_parser.add_argument('--cover-type', help='Cover type (jpg, png, etc.), inferred from cover file extension by default')  # NOCA:line-too-long(long SDK parameter or URL string)
    upload_parser.add_argument('--class-id', type=int, help='Category ID, default 0 (other categories)')
    upload_parser.add_argument('--procedure', help='Task flow name, automatically executed after upload completes')
    upload_parser.add_argument('--expire-time', help='Media file expiration time, ISO 8601 format, e.g. 2025-12-31T23:59:59Z')  # NOCA:line-too-long(long SDK parameter or URL string)
    upload_parser.add_argument('--storage-region', help='Specify storage region, e.g. ap-chongqing')
    upload_parser.add_argument('--source-context', help='Source context, passes through user request info, max 250 characters')  # NOCA:line-too-long(long SDK parameter or URL string)
    upload_parser.add_argument('--concurrent-upload-number', type=int, help='Number of concurrent multipart uploads, effective for large files')  # NOCA:line-too-long(long SDK parameter or URL string)
    upload_parser.add_argument('--media-storage-path', help='Media storage path, starts with /, only available for sub-applications in FileID+Path mode')  # NOCA:line-too-long(long SDK parameter or URL string)
    upload_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                               help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long SDK parameter or URL string)
    upload_parser.add_argument('--app-name', help='Fuzzy match sub-application by name/description (mutually exclusive with --sub-app-id)')  # NOCA:line-too-long(long SDK parameter or URL string)
    upload_parser.add_argument('--region', default='ap-guangzhou', help='Region, default ap-guangzhou')
    upload_parser.add_argument('--verbose', action='store_true', help='Show detailed upload information')
    upload_parser.add_argument('--json', action='store_true', help='Output full response in JSON format')
    upload_parser.add_argument('--dry-run', action='store_true', help='Preview ApplyUpload request parameters without actually executing')  # NOCA:line-too-long(long SDK parameter or URL string)

    # ---- pull subcommand (URL pull upload) ----
    pull_parser = subparsers.add_parser('pull', help='URL pull upload (PullUpload)')
    pull_parser.add_argument('--url', required=True, help='Media URL (required)')
    pull_parser.add_argument('--media-name', help='Media name')
    pull_parser.add_argument('--media-type', help='Media type (mp4, mp3, jpg, etc.)')
    pull_parser.add_argument('--cover-url', help='Cover image URL')
    pull_parser.add_argument('--procedure', help='Task flow name, automatically executed after upload completes')
    pull_parser.add_argument('--expire-time', help='Media file expiration time, ISO 8601 format')
    pull_parser.add_argument('--storage-region', help='Specify storage region, e.g. ap-chongqing')
    pull_parser.add_argument('--class-id', type=int, help='Category ID, default 0 (other categories)')
    pull_parser.add_argument('--tasks-priority', type=int, help='Task priority, range -10 to 10, default 0')
    pull_parser.add_argument('--session-context', help='Session context, passes through user request info, max 1000 characters')  # NOCA:line-too-long(long SDK parameter or URL string)
    pull_parser.add_argument('--session-id', help='Deduplication identifier, requests with the same ID within three days will return an error, max 50 characters')  # NOCA:line-too-long(long SDK parameter or URL string)
    pull_parser.add_argument('--ext-info', help='Reserved field, used for special purposes')
    pull_parser.add_argument('--source-context', help='Source context, passes through user request info, max 250 characters')  # NOCA:line-too-long(long SDK parameter or URL string)
    pull_parser.add_argument('--media-storage-path', help='Media storage path, starts with /, only available for sub-applications in FileID+Path mode')  # NOCA:line-too-long(long SDK parameter or URL string)
    pull_parser.add_argument('--sub-app-id', type=int,
                             default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                             help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long SDK parameter or URL string)
    pull_parser.add_argument('--app-name', help='Fuzzy match sub-application by name/description (mutually exclusive with --sub-app-id)')  # NOCA:line-too-long(long SDK parameter or URL string)
    pull_parser.add_argument('--region', default='ap-guangzhou', help='Region, default ap-guangzhou')
    pull_parser.add_argument('--no-wait', action='store_true', help='Only submit the task, do not wait for results')
    pull_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds), default 600')
    pull_parser.add_argument('--json', action='store_true', help='Output full response in JSON format')
    pull_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters without actually executing')  # NOCA:line-too-long(long SDK parameter or URL string)

    args = parser.parse_args()

    if args.command == 'upload':
        upload_media(args)
    elif args.command == 'pull':
        pull_upload(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
