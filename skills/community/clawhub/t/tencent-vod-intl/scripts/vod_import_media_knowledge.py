#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD Import Media Knowledge Script
Use the ImportMediaKnowledge API to perform large model content understanding on videos and store the results in a
knowledge base.

Core workflow:
1. Initiate a large model content understanding task for the specified video (including summary generation, ASR speech
recognition, etc.)
2. Persist the structured content after understanding (summaries, subtitles, key information, etc.) into the VOD
knowledge base
3. The stored content can be semantically searched and retrieved via interfaces such as SearchMediaBySemantics

Typical use cases:
- Intelligently analyze uploaded videos to extract core content
- Build a video knowledge base to support subsequent semantic content retrieval and Q&A
- Batch-process video libraries to establish searchable knowledge indexes for large-scale video assets

Default template 100: includes audio-level summary and ASR (Automatic Speech Recognition).

API documentation: https://cloud.tencent.com/document/api/266/126286
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


# Preset template descriptions
DEFINITION_TEMPLATES = {
    100: "Audio-level summary and ASR (Automatic Speech Recognition)",
}


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


def import_media_knowledge(args):
    """Import media into the knowledge base"""

    req = models.ImportMediaKnowledgeRequest()

    # Required parameters
    if not args.sub_app_id:
        print("Error: --sub-app-id must be specified or the environment variable TENCENTCLOUD_VOD_SUB_APP_ID must be set")  # NOCA:line-too-long(long output string or URL, cannot be shortened)
        sys.exit(1)
    req.SubAppId = args.sub_app_id
    req.FileId = args.file_id

    # Optional parameter: large model understanding template ID, default 100
    if args.definition is not None:
        req.Definition = args.definition

    # dry-run mode (no authentication required)
    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return None

    client = get_client(args.region)

    try:
        resp = client.ImportMediaKnowledge(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get("TaskId", "N/A")
        request_id = result.get("RequestId", "N/A")

        print(f"✅ Import media knowledge task submitted successfully!")
        print(f"  TaskId:    {task_id}")
        print(f"  RequestId: {request_id}")
        print(f"  FileId:    {args.file_id}")
        print(f"  SubAppId:  {args.sub_app_id}")
        if args.definition is not None:
            desc = DEFINITION_TEMPLATES.get(args.definition, "Custom template")
            print(f"  Definition: {args.definition} ({desc})")

        # Wait for task completion
        if not args.no_wait and task_id != "N/A":
            wait_result = wait_for_task(client, task_id, args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {task_id}")

        if args.json:
            print("\nFull response:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
        error_msg = str(e)
        print(f"❌ Failed to import media knowledge: {error_msg}")
        sys.exit(1)


def wait_for_task(client, task_id, sub_app_id=None, max_wait=600):
    """Wait for task completion

    Poll task status via DescribeTaskDetail.

    Args:
        client: VOD client
        task_id: Task ID
        sub_app_id: Sub-application ID
        max_wait: Maximum wait time (seconds), default 600
    """
    print(f"\n⏳ Waiting for task to complete (TaskId: {task_id})...")
    start_time = time.time()
    poll_interval = 5  # Initial polling interval: 5 seconds

    while time.time() - start_time < max_wait:
        try:
            req = models.DescribeTaskDetailRequest()
            req.TaskId = task_id
            if sub_app_id:
                req.SubAppId = sub_app_id

            resp = client.DescribeTaskDetail(req)
            result = json.loads(resp.to_json_string())

            status = result.get("Status", "PROCESSING")
            elapsed = int(time.time() - start_time)
            print(f"  [{elapsed}s] Status: {status}")

            if status == "FINISH":
                print("✅ Task completed!")

                # Attempt to output task result
                task_result = result.get("ImportMediaKnowledgeTask") or result.get("Output")
                if task_result:
                    print("\nTask result:")
                    print(json.dumps(task_result, indent=2, ensure_ascii=False))

                return result

            elif status == "FAIL":
                err_code = result.get("ErrCode", "N/A")
                err_msg = result.get("Message", "Unknown error")
                print(f"❌ Task failed!")
                print(f"  Error code: {err_code}")
                print(f"  Error message: {err_msg}")
                return result

            # Dynamically adjust polling interval
            if elapsed > 60:
                poll_interval = 15
            elif elapsed > 30:
                poll_interval = 10

            time.sleep(poll_interval)

        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
            print(f"  Failed to query task status: {e}")
            time.sleep(poll_interval)

    elapsed = int(time.time() - start_time)
    print(f"⏱️ Wait timed out ({elapsed}s), task is still running")
    print(f"  You can use the following command to manually query the task status:")
    print(f"  python scripts/vod_describe_task.py --task-id {task_id}")
    return None


def batch_import(args):
    """Batch import multiple media files into the knowledge base"""
    if not args.sub_app_id:
        print("Error: --sub-app-id must be specified or the environment variable TENCENTCLOUD_VOD_SUB_APP_ID must be set")  # NOCA:line-too-long(long output string or URL, cannot be shortened)
        sys.exit(1)
    client = get_client(args.region)

    file_ids = args.file_ids
    success_count = 0
    fail_count = 0
    results = []

    print(f"📦 Batch importing {len(file_ids)} media files into the knowledge base...")
    print(f"  SubAppId:  {args.sub_app_id}")
    if args.definition is not None:
        desc = DEFINITION_TEMPLATES.get(args.definition, "Custom template")
        print(f"  Definition: {args.definition} ({desc})")
    print()

    for i, file_id in enumerate(file_ids, 1):
        print(f"[{i}/{len(file_ids)}] FileId: {file_id}")

        req = models.ImportMediaKnowledgeRequest()
        req.SubAppId = args.sub_app_id
        req.FileId = file_id
        if args.definition is not None:
            req.Definition = args.definition

        if args.dry_run:
            print(f"  [DRY RUN] Skipped")
            continue

        try:
            resp = client.ImportMediaKnowledge(req)
            result = json.loads(resp.to_json_string())
            task_id = result.get("TaskId", "N/A")
            print(f"  ✅ Submitted successfully (TaskId: {task_id})")
            success_count += 1
            results.append({"file_id": file_id, "task_id": task_id, "status": "success"})
        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
            print(f"  ❌ Submission failed: {e}")
            fail_count += 1
            results.append({"file_id": file_id, "error": str(e), "status": "failed"})

    print(f"\n📊 Batch import results: {success_count}/{len(file_ids)} succeeded, {fail_count}/{len(file_ids)} failed")

    if args.json:
        print("\nFull results:")
        print(json.dumps(results, indent=2, ensure_ascii=False))

    return results


def list_templates(args):
    """List available large model understanding templates"""
    print("Available large model understanding templates (Definition):")
    print()
    for def_id, desc in DEFINITION_TEMPLATES.items():
        print(f"  {def_id}: {desc}")
    print()
    print("Notes:")
    print("  - Template 100 is the default template, including audio-level summary and ASR (Automatic Speech Recognition)")  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    print("  - To use a custom template, specify the template ID via the --definition parameter")
    print("  - For more template information, refer to the API documentation: https://cloud.tencent.com/document/api/266/126286")  # NOCA:line-too-long(long output string or URL, cannot be shortened)


def main():
    parser = argparse.ArgumentParser(
        description='VOD Import Media Knowledge Tool — Perform large model content understanding on videos and store the results in a knowledge base for subsequent semantic search queries',  # NOCA:line-too-long(long output string or URL, cannot be shortened)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Import a single media file into the knowledge base (using default template 100)
  python vod_import_media_knowledge.py import \\
      --sub-app-id 1500046806 \\
      --file-id 5285485487985271487

  # Specify a large model understanding template
  python vod_import_media_knowledge.py import \\
      --sub-app-id 1500046806 \\
      --file-id 5285485487985271487 \\
      --definition 100

  # Wait for task completion by default
  python vod_import_media_knowledge.py import \\
      --sub-app-id 1500046806 \\
      --file-id 5285485487985271487
  
  # Do not wait, only submit the task
  python vod_import_media_knowledge.py import \\
      --sub-app-id 1500046806 \\
      --file-id 5285485487985271487 \\
      --no-wait

  # Batch import multiple media files
  python vod_import_media_knowledge.py batch \\
      --sub-app-id 1500046806 \\
      --file-ids 528548548798527148 528548548798527149 528548548798527150

  # Preview request parameters (without actually executing)
  python vod_import_media_knowledge.py import \\
      --sub-app-id 1500046806 \\
      --file-id 5285485487985271487 \\
      --dry-run

  # List available templates
  python vod_import_media_knowledge.py templates
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # ---- import subcommand (single import) ----
    import_parser = subparsers.add_parser('import', help='Import a single media file into the knowledge base')
    import_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                               help='VOD application ID (required; can also be set via the environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    import_parser.add_argument('--file-id', required=True,
                               help='Media file ID (required)')
    import_parser.add_argument('--definition', type=int, default=100,
                               help='Large model understanding template ID (default 100, includes audio-level summary and ASR)')  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    import_parser.add_argument('--region', default='ap-guangzhou',
                               help='Region, default ap-guangzhou')
    import_parser.add_argument('--no-wait', action='store_true',
                               help='Only submit the task without waiting for results')
    import_parser.add_argument('--max-wait', type=int, default=600,
                               help='Maximum wait time (seconds), default 600')
    import_parser.add_argument('--json', action='store_true',
                               help='Output full response in JSON format')
    import_parser.add_argument('--dry-run', action='store_true',
                               help='Preview request parameters without actually executing')

    # ---- batch subcommand (batch import) ----
    batch_parser = subparsers.add_parser('batch', help='Batch import multiple media files into the knowledge base')
    batch_parser.add_argument('--sub-app-id', type=int,
                              default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                              help='VOD application ID (required; can also be set via the environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    batch_parser.add_argument('--file-ids', nargs='+', required=True,
                              help='List of media file IDs (required, space-separated)')
    batch_parser.add_argument('--definition', type=int, default=100,
                              help='Large model understanding template ID (default 100, includes audio-level summary and ASR)')  # NOCA:line-too-long(long output string or URL, cannot be shortened)
    batch_parser.add_argument('--region', default='ap-guangzhou',
                              help='Region, default ap-guangzhou')
    batch_parser.add_argument('--json', action='store_true',
                              help='Output full results in JSON format')
    batch_parser.add_argument('--dry-run', action='store_true',
                              help='Preview request parameters without actually executing')

    # ---- templates subcommand ----
    _ = subparsers.add_parser('templates', help='List available large model understanding templates')

    args = parser.parse_args()

    if args.command == 'import':
        import_media_knowledge(args)
    elif args.command == 'batch':
        batch_import(args)
    elif args.command == 'templates':
        list_templates(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
