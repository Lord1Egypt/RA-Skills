#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD Semantic Media Search Script
Uses the SearchMediaBySemantics API to perform natural language semantic search on media imported into the knowledge
base.

Core workflow:
1. User inputs a natural language description (e.g., "beach video with sunset")
2. Calls the SearchMediaBySemantics API for semantic matching
3. Returns a list of matching media segments (including FileId, match score, and segment time range)

Prerequisites:
- Media files must first be imported into the knowledge base via ImportMediaKnowledge (vod_import_media_knowledge.py)
- After import, the large model performs content understanding on the video (summary, ASR, etc.), and the results are
stored in the knowledge base
- This script performs semantic retrieval based on the understanding results stored in the knowledge base

Difference from SearchMedia:
- SearchMedia (vod_search_media.py): Condition-based filtering using metadata (name, tags, categories, etc.)
- SearchMediaBySemantics (this script): Natural language semantic search that matches based on video content
understanding

API documentation: https://cloud.tencent.com/document/api/266/126287
"""

import os
import sys
import json
import argparse

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


# Supported file categories
VALID_CATEGORIES = ["Video", "Audio", "Image"]

# Supported search task types
VALID_TASK_TYPES = [
    "AiAnalysis.DescriptionTask",
    "SmartSubtitle.AsrFullTextTask",
]


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
def resolve_sub_app_id(client, app_name):
    """Fuzzy-match a sub-application ID by application name, description, or tag.

    Queries the full list of sub-applications and performs fuzzy matching against name, description, and tag values.
    - Exact name match takes priority
    - Falls back to fuzzy matching on name, description, and tags
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


def format_time_offset(seconds):
    """Format a time offset in seconds into a human-readable string"""
    if seconds is None:
        return "N/A"
    seconds = float(seconds)
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        m = int(seconds // 60)
        s = seconds % 60
        return f"{m}m{s:.1f}s"
    else:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        return f"{h}h{m}m{s:.0f}s"


def print_search_results(results, verbose=False):
    """Format and print search results"""
    if not results:
        print("\nNo matching media segments found.")
        print("Tip: Make sure the target media has been imported into the knowledge base via ImportMediaKnowledge.")
        return

    # Group and count by FileId
    file_ids = set()
    for r in results:
        file_ids.add(r.get("FileId", "N/A"))

    print(f"\n📋 Search results: {len(results)} matching segment(s) across {len(file_ids)} media file(s)")
    print("=" * 70)

    for i, result in enumerate(results, 1):
        file_id = result.get("FileId", "N/A")
        score = result.get("Score", 0)
        start = result.get("StartTimeOffset")
        end = result.get("EndTimeOffset")

        # Score bar chart
        bar_len = 20
        filled = int(score * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)

        print(f"\n  [{i}] FileId: {file_id}")
        print(f"      Score:  {score:.5f} [{bar}]")

        if start is not None and end is not None:
            duration = float(end) - float(start)
            print(f"      Segment: {format_time_offset(start)} → {format_time_offset(end)} (Duration: {format_time_offset(duration)})")  # NOCA:line-too-long(long SDK parameter or URL string)
        elif start is not None:
            print(f"      Start:  {format_time_offset(start)}")

    print()


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def search_by_semantics(args):
    """Execute semantic search"""

    # Build request parameters
    payload = {}

    # Handle Sub AppId
    sub_app_id = args.sub_app_id
    client = None

    # Resolve Sub AppId from application name
    if args.app_name and not args.dry_run:
        if args.sub_app_id:
            print("Error: --app-name and --sub-app-id cannot be specified at the same time")
            sys.exit(1)
        client = get_client(args.region)
        sub_app_id = resolve_sub_app_id(client, args.app_name)

    if sub_app_id:
        payload["SubAppId"] = sub_app_id

    # Required: search text
    payload["Text"] = args.text

    # Optional parameters
    if args.limit is not None:
        payload["Limit"] = args.limit

    if args.categories:
        payload["Categories"] = args.categories

    if args.tags:
        payload["Tags"] = args.tags

    if args.persons:
        payload["Persons"] = args.persons

    if args.task_types:
        payload["TaskTypes"] = args.task_types

    # dry-run mode
    if args.dry_run:
        if args.app_name:
            payload["_app_name"] = args.app_name
            payload["_note"] = "app_name will be resolved to SubAppId during actual execution"
        print("[DRY RUN] Request parameters:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return None

    # Build request
    if client is None:
        client = get_client(args.region)

    req = models.SearchMediaBySemanticsRequest()
    req.from_json_string(json.dumps(payload, ensure_ascii=False))

    try:
        resp = client.SearchMediaBySemantics(req)
        result = json.loads(resp.to_json_string())

        search_results = result.get("SearchResults", [])
        request_id = result.get("RequestId", "N/A")

        # JSON format output
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result

        # Human-readable output
        print(f"🔍 Semantic search complete!")
        print(f"  Search text: \"{args.text}\"")
        print(f"  Matches: {len(search_results)} segment(s)")
        print(f"  RequestId: {request_id}")

        if sub_app_id:
            print(f"  SubAppId: {sub_app_id}")

        if args.categories:
            print(f"  File categories: {', '.join(args.categories)}")
        if args.tags:
            print(f"  Tag filter: {', '.join(args.tags)}")
        if args.persons:
            print(f"  Person filter: {', '.join(args.persons)}")
        if args.task_types:
            print(f"  Task types: {', '.join(args.task_types)}")

        print_search_results(search_results, verbose=args.verbose)

        # Usage tips
        if search_results:
            sample_file_id = search_results[0].get("FileId", "xxx")
            print("💡 Next steps:")
            print(f"  View media details: python scripts/vod_describe_media.py --file-id {sample_file_id}" +
                  (f" --sub-app-id {sub_app_id}" if sub_app_id else ""))

        return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        error_msg = str(e)
        print(f"❌ Semantic search failed: {error_msg}")

        # Common error hints
        if "InvalidParameterValue" in error_msg:
            print("\nPossible causes:")
            print("  - Search text is empty or in an incorrect format")
            print("  - SubAppId is incorrect")
        elif "ResourceNotFound" in error_msg or "KnowledgeBase" in error_msg.lower():
            print("\nPossible causes:")
            print("  - The target media has not been imported into the knowledge base")
            print("  - Please use vod_import_media_knowledge.py to import media into the knowledge base first")

        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='VOD Semantic Media Search Tool — Search video content imported into the knowledge base using natural language',  # NOCA:line-too-long(long SDK parameter or URL string)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Prerequisites:
  Media files must first be imported into the knowledge base via ImportMediaKnowledge:
    python scripts/vod_import_media_knowledge.py import \\
        --sub-app-id 1500046806 --file-id 5285485487985271487

  After import, the large model performs content understanding on the video (summary, ASR, etc.).
  Once the results are stored in the knowledge base, this script can be used for semantic search.

Difference from SearchMedia:
  SearchMedia (vod_search_media.py)          → Condition-based metadata filtering (name, tags, etc.)
  SearchMediaBySemantics (this script)       → Natural language semantic search (matches based on video content understanding)

Examples:
  # Basic semantic search
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "beach video with sunset"

  # Search by application name + semantic query
  python vod_search_media_by_semantics.py \\
      --app-name "Test Application" \\
      --text "scene with someone running"

  # Limit number of results
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "meeting discussion content" \\
      --limit 5

  # Search only video files
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "cats playing" \\
      --categories Video

  # Filter by tags
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "amazing goal" \\
      --tags "sports" "soccer"

  # Filter by person (search segments containing specified person)
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "speech content" \\
      --persons "John Doe"

  # Specify search task type
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "product introduction" \\
      --task-types AiAnalysis.DescriptionTask

  # JSON format output
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "beach video with sunset" \\
      --json

  # Preview request parameters (without actual execution)
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "beach video with sunset" \\
      --dry-run
        '''
    )

    # Application selection (mutually exclusive)
    app_group = parser.add_argument_group('Application Selection')
    app_group.add_argument('--sub-app-id', type=int,
                           default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                           help='VOD sub-application ID (can also be set via the environment variable TENCENTCLOUD_VOD_SUB_APP_ID; mutually exclusive with --app-name)')  # NOCA:line-too-long(long SDK parameter or URL string)
    app_group.add_argument('--app-name',
                           help='Fuzzy-match a sub-application by name or description (mutually exclusive with --sub-app-id)')  # NOCA:line-too-long(long SDK parameter or URL string)

    # Search parameters
    search_group = parser.add_argument_group('Search Parameters')
    search_group.add_argument('--text', '-t', required=True,
                              help='Search content as a natural language description (required), e.g., "beach video with sunset"')  # NOCA:line-too-long(long SDK parameter or URL string)
    search_group.add_argument('--limit', '-n', type=int, default=20,
                              help='Number of records to return, default 20, range [1, 100]')

    # Filter conditions
    filter_group = parser.add_argument_group('Filter Conditions')
    filter_group.add_argument('--categories', nargs='+',
                              choices=VALID_CATEGORIES,
                              help='File category filter: Video / Audio / Image')
    filter_group.add_argument('--tags', nargs='+',
                              help='Tag filter (matches any tag, up to 16 tags)')
    filter_group.add_argument('--persons', nargs='+',
                              help='Person filter (matches all specified persons, up to 16)')
    filter_group.add_argument('--task-types', nargs='+',
                              choices=VALID_TASK_TYPES,
                              help='Search task type: AiAnalysis.DescriptionTask / SmartSubtitle.AsrFullTextTask')

    # Output control
    output_group = parser.add_argument_group('Output Control')
    output_group.add_argument('--verbose', '-v', action='store_true',
                              help='Show detailed information')
    output_group.add_argument('--json', action='store_true',
                              help='Output the full response in JSON format')
    output_group.add_argument('--region', default='ap-guangzhou',
                              help='Region, default ap-guangzhou')
    output_group.add_argument('--dry-run', action='store_true',
                              help='Preview request parameters without actual execution')

    args = parser.parse_args()

    # Validate that --app-name and --sub-app-id are mutually exclusive
    if args.app_name and args.sub_app_id:
        print("Error: --app-name and --sub-app-id cannot be specified at the same time")
        sys.exit(1)

    # Validate that an application must be specified
    if not args.sub_app_id and not args.app_name:
        print("Error: Either --sub-app-id or --app-name must be specified")
        sys.exit(1)

    # Validate limit range
    if args.limit is not None and (args.limit < 1 or args.limit > 100):
        print("Error: --limit must be in the range [1, 100]")
        sys.exit(1)

    search_by_semantics(args)


if __name__ == '__main__':
    main()
