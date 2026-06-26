#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD Search Media Script
Uses the SearchMedia API to search for media information, supporting multiple filter conditions.

Scenario Description:
  - SearchMedia: Supports fuzzy search by name, category, tags, file type, and other filter conditions
  - DescribeMediaInfos: Exact query by FileId (handled by a separate script vod_describe_media.py)

This script handles all search scenarios uniformly. It can also be used when only a FileId is
available (via the SearchMedia.FileIds parameter).

API Conflict Resolution:
  - User provides FileId → this script uses SearchMedia.FileIds parameter (or use vod_describe_media.py for exact query)
  - User provides name/description/tags → this script uses SearchMedia fuzzy search
  - User specifies an application by name → first call DescribeSubAppIds to match the app, then search

API Documentation: https://cloud.tencent.com/document/api/266/31813
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
    """Fuzzy-match a sub-application ID by name, description, or tag.

    Queries the full list of sub-applications and matches against name, description, and tag values.
    - Exact name match takes priority
    - Falls back to fuzzy match on name, description, and tags
    - Returns immediately if exactly one match is found
    - Lists all matches and exits if multiple are found
    - Prints an error and exits if no match is found
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
    print(f"Found {len(fuzzy)} matching sub-applications. Please specify the exact application ID with --sub-app-id:")
    for a in fuzzy:
        n = a.get("SubAppIdName") or a.get("Name") or "N/A"
        sid = a.get("SubAppId", "N/A")
        d = a.get("Description") or ""
        print(f"  - {n} (SubAppId: {sid}){' — ' + d if d else ''}")
    sys.exit(1)


def format_duration(seconds):
    """Format a duration in seconds into a human-readable string"""
    if seconds is None:
        return "N/A"
    seconds = float(seconds)
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        m = int(seconds // 60)
        s = seconds % 60
        return f"{m}m{s:.0f}s"
    else:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        return f"{h}h{m}m"


def format_size(size_bytes):
    """Format a file size in bytes into a human-readable string"""
    if size_bytes is None:
        return "N/A"
    size_bytes = int(size_bytes)
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def format_bitrate(bps):
    """Format a bitrate value"""
    if not bps:
        return 'N/A'
    if bps >= 1000000:
        return f"{bps/1000000:.2f} Mbps"
    elif bps >= 1000:
        return f"{bps/1000:.0f} kbps"
    return f"{bps} bps"


def print_video_streams(streams, indent="    "):
    """Print video stream information"""
    if not streams:
        return
    for j, vs in enumerate(streams):
        codec = vs.get('Codec', 'N/A')
        codec_tag = vs.get('CodecTag', '')
        w = vs.get('Width', '?')
        h = vs.get('Height', '?')
        fps = vs.get('Fps', 'N/A')
        br = format_bitrate(vs.get('Bitrate'))
        dri = vs.get('DynamicRangeInfo') or {}
        dr_type = dri.get('Type', '')
        hdr_type = dri.get('HDRType', '')
        dr_str = f"  {dr_type}" if dr_type else ""
        if hdr_type:
            dr_str += f"({hdr_type})"
        tag_str = f"/{codec_tag}" if codec_tag else ""
        print(f"{indent}Video stream[{j}]: {codec}{tag_str}  {w}x{h}  {fps}fps  {br}{dr_str}")


def print_audio_streams(streams, indent="    "):
    """Print audio stream information"""
    if not streams:
        return
    for j, aus in enumerate(streams):
        codec = aus.get('Codec', 'N/A')
        sr = aus.get('SamplingRate', 'N/A')
        br = format_bitrate(aus.get('Bitrate'))
        print(f"{indent}Audio stream[{j}]: {codec}  SampleRate={sr}Hz  {br}")


def print_source_info(source_info, indent="  "):
    """Print source information"""
    if not source_info:
        return
    print(f"{indent}Source type: {source_info.get('SourceType', 'N/A')}")
    ctx = source_info.get('SourceContext', '')
    if ctx:
        print(f"{indent}Source context: {ctx}")
    live_info = source_info.get('LiveRecordInfo') or {}
    if live_info:
        print(f"{indent}Live recording: Domain={live_info.get('Domain','N/A')}  Path={live_info.get('Path','N/A')}  StreamId={live_info.get('StreamId','N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
        print(f"{indent}  Recording time: {live_info.get('RecordStartTime','N/A')} → {live_info.get('RecordEndTime','N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
    trtc_info = source_info.get('TrtcRecordInfo') or {}
    if trtc_info:
        print(f"{indent}TRTC recording: SdkAppId={trtc_info.get('SdkAppId','N/A')}  RoomId={trtc_info.get('RoomId','N/A')}  TaskId={trtc_info.get('TaskId','N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
        user_ids = trtc_info.get('UserIds') or []
        if user_ids:
            print(f"{indent}  Users: {', '.join(user_ids)}")
    web_info = source_info.get('WebPageRecordInfo') or {}
    if web_info:
        print(f"{indent}Web page recording: URL={web_info.get('RecordUrl','N/A')}  TaskId={web_info.get('RecordTaskId','N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def print_media_info(media, index=None, verbose=False):
    """Format and print information for a single media item"""
    file_id = media.get("FileId", "N/A")
    basic = media.get("BasicInfo") or {}
    meta = media.get("MetaData") or {}

    prefix = f"[{index}] " if index is not None else ""

    name = basic.get("Name", "N/A")
    media_type = basic.get("Type", "N/A")
    category = basic.get("Category", "N/A")
    status = basic.get("Status", "N/A")
    create_time = basic.get("CreateTime", "N/A")
    update_time = basic.get("UpdateTime", "")
    expire_time = basic.get("ExpireTime", "")
    media_url = basic.get("MediaUrl", "")
    cover_url = basic.get("CoverUrl", "")
    description = basic.get("Description", "")
    class_name = basic.get("ClassName", "")
    class_path = basic.get("ClassPath", "")
    class_id = basic.get("ClassId")
    tags = basic.get("TagSet") or []
    storage_class = basic.get("StorageClass", "")
    storage_region = basic.get("StorageRegion", "")
    storage_path = basic.get("StoragePath", "")
    vid = basic.get("Vid", "")

    duration = meta.get("Duration")
    size = meta.get("Size")
    width = meta.get("Width")
    height = meta.get("Height")
    bitrate = meta.get("Bitrate")
    rotate = meta.get("Rotate")
    md5 = meta.get("Md5", "")
    vid_dur = meta.get("VideoDuration")
    aud_dur = meta.get("AudioDuration")

    print(f"\n{prefix}📄 {name}")
    print(f"  FileId:   {file_id}")
    print(f"  Type:     {category} ({media_type})")
    print(f"  Status:   {status}")
    print(f"  Created:  {create_time}")
    if update_time:
        print(f"  Updated:  {update_time}")
    if expire_time and expire_time != "9999-12-31T23:59:59Z":
        print(f"  Expires:  {expire_time}")

    if duration is not None:
        print(f"  Duration: {format_duration(duration)}")
    if vid_dur is not None and verbose:
        print(f"  Video Duration: {format_duration(vid_dur)}  Audio Duration: {format_duration(aud_dur)}")
    if size is not None:
        print(f"  Size:     {format_size(size)}")
    if width and height:
        print(f"  Resolution: {width}x{height}")
    if bitrate:
        print(f"  Bitrate:  {format_bitrate(bitrate)}")
    if rotate and verbose:
        print(f"  Rotation: {rotate}°")
    if md5 and verbose:
        print(f"  MD5:      {md5}")

    if description:
        print(f"  Description: {description}")
    if class_name or class_path:
        cls_str = class_path or class_name
        if class_id is not None:
            cls_str += f" (ID: {class_id})"
        print(f"  Category: {cls_str}")
    if tags:
        print(f"  Tags:     {', '.join(tags)}")
    if storage_region:
        print(f"  Storage Region: {storage_region}")
    if storage_path and verbose:
        print(f"  Storage Path: {storage_path}")
    if storage_class:
        print(f"  Storage Class: {storage_class}")
    if vid and verbose:
        print(f"  Vid:      {vid}")

    if verbose:
        if media_url:
            print(f"  Media URL:  {media_url}")
        if cover_url:
            print(f"  Cover URL:  {cover_url}")
        # Source info
        source_info = basic.get("SourceInfo")
        if source_info:
            print_source_info(source_info, indent="  ")
        # Video streams / Audio streams
        print_video_streams(meta.get("VideoStreamSet") or [], indent="  ")
        print_audio_streams(meta.get("AudioStreamSet") or [], indent="  ")
        # Transcode Info
        transcode_set = (media.get('TranscodeInfo') or {}).get('TranscodeSet') or []
        if transcode_set:
            print(f"  Transcode Results: {len(transcode_set)} item(s)")
            for t in transcode_set[:3]:
                print(f"    TemplateID={t.get('Definition','N/A')}  {t.get('Width','?')}x{t.get('Height','?')}  {format_bitrate(t.get('Bitrate'))}  {t.get('Container','N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
                print(f"    URL: {t.get('Url','N/A')}")
            if len(transcode_set) > 3:
                print(f"    ... {len(transcode_set)-3} more transcode result(s)")
        # Animated Graphics Info
        anim_set = (media.get('AnimatedGraphicsInfo') or {}).get('AnimatedGraphicsSet') or []
        if anim_set:
            print(f"  Animated Graphics: {len(anim_set)} item(s)")
            for a in anim_set[:2]:
                print(f"    TemplateID={a.get('Definition','N/A')}  {a.get('Container','N/A')}  URL: {a.get('Url','N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
        # SnapshotBy Time Offset Info
        snap_set = (media.get('SnapshotByTimeOffsetInfo') or {}).get('SnapshotByTimeOffsetSet') or []
        if snap_set:
            print(f"  Time-offset Snapshots: {len(snap_set)} group(s)")
        # Sample Snapshot Info
        sample_set = (media.get('SampleSnapshotInfo') or {}).get('SampleSnapshotSet') or []
        if sample_set:
            print(f"  Sample Snapshots: {len(sample_set)} group(s)")
        # Image Sprite Info
        sprite_set = (media.get('ImageSpriteInfo') or {}).get('ImageSpriteSet') or []
        if sprite_set:
            print(f"  Image Sprites: {len(sprite_set)} group(s)")
        # Adaptive Dynamic Streaming Info
        adaptive_set = (media.get('AdaptiveDynamicStreamingInfo') or {}).get('AdaptiveDynamicStreamingSet') or []
        if adaptive_set:
            print(f"  Adaptive Dynamic Streaming: {len(adaptive_set)} item(s)")
            for a in adaptive_set[:2]:
                print(f"    TemplateID={a.get('Definition','N/A')}  {a.get('Package','N/A')}  URL: {a.get('Url','N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
        # Key Frame Desc Info
        kf_set = (media.get('KeyFrameDescInfo') or {}).get('KeyFrameDescSet') or []
        if kf_set:
            print(f"  Key Frame Marks: {len(kf_set)} item(s)")
        # Subtitle Info
        sub_set = (media.get('SubtitleInfo') or {}).get('SubtitleSet') or []
        if sub_set:
            print(f"  Subtitles: {len(sub_set)} item(s)")
            for s in sub_set:
                print(f"    [{s.get('Id','')}] {s.get('Name','')} ({s.get('Language','')}) {s.get('Format','')} URL: {s.get('Url','N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
        # Review Info
        review_info = media.get('ReviewInfo') or {}
        if review_info:
            mr = review_info.get('MediaReviewInfo') or {}
            cr = review_info.get('CoverReviewInfo') or {}
            if mr:
                print(f"  Media Review: Suggestion={mr.get('Suggestion','N/A')}  Time={mr.get('ReviewTime','N/A')}")
            if cr:
                print(f"  Cover Review: Suggestion={cr.get('Suggestion','N/A')}  Time={cr.get('ReviewTime','N/A')}")
        # Mini Program Review Info
        mp_list = (media.get('MiniProgramReviewInfo') or {}).get('MiniProgramReviewList') or []
        if mp_list:
            print(f"  Mini Program Review: {len(mp_list)} item(s)")
        # MPSAi Media Info
        ai_list = (media.get('MPSAiMediaInfo') or {}).get('AiMediaList') or []
        if ai_list:
            print(f"  MPS AI Media: {len(ai_list)} task type(s)")
        # Image Understanding Info
        img_set = (media.get('ImageUnderstandingInfo') or {}).get('ImageUnderstandingSet') or []
        if img_set:
            print(f"  Image Understanding: {len(img_set)} item(s)")

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)

def search_media(args):
    """Search for media files"""

    # Build request parameters (dry-run does not require authentication)
    payload = {}

    # Handle Sub AppId
    sub_app_id = args.sub_app_id

    # Resolve Sub AppId by app name (requires client, non-dry-run)
    if args.app_name and not args.dry_run:
        if args.sub_app_id:
            print("Error: --app-name and --sub-app-id cannot be specified at the same time")
            sys.exit(1)
        client = get_client(args.region)
        sub_app_id = resolve_sub_app_id(client, args.app_name)

    if sub_app_id:
        payload["SubAppId"] = sub_app_id

    # Search conditions
    if args.file_ids:
        payload["FileIds"] = args.file_ids
    if args.names:
        payload["Names"] = args.names
    if args.name_prefixes:
        payload["NamePrefixes"] = args.name_prefixes
    if args.descriptions:
        payload["Descriptions"] = args.descriptions
    if args.tags:
        payload["Tags"] = args.tags
    if args.class_ids:
        payload["ClassIds"] = args.class_ids
    if args.categories:
        payload["Categories"] = args.categories
    if args.source_types:
        payload["SourceTypes"] = args.source_types
    if args.media_types:
        payload["MediaTypes"] = args.media_types
    if args.status:
        payload["Status"] = args.status
    if args.review_results:
        payload["ReviewResults"] = args.review_results
    if args.storage_regions:
        payload["StorageRegions"] = args.storage_regions
    if args.storage_classes:
        payload["StorageClasses"] = args.storage_classes
    if args.stream_ids:
        payload["StreamIds"] = args.stream_ids
    if args.trtc_sdk_app_ids:
        payload["TrtcSdkAppIds"] = args.trtc_sdk_app_ids
    if args.trtc_room_ids:
        payload["TrtcRoomIds"] = args.trtc_room_ids
    if args.stream_domains:
        payload["StreamDomains"] = args.stream_domains
    if args.stream_paths:
        payload["StreamPaths"] = args.stream_paths

    # Time range
    if args.create_after or args.create_before:
        create_time = {}
        if args.create_after:
            create_time["After"] = args.create_after
        if args.create_before:
            create_time["Before"] = args.create_before
        payload["CreateTime"] = create_time

    if args.expire_after or args.expire_before:
        expire_time = {}
        if args.expire_after:
            expire_time["After"] = args.expire_after
        if args.expire_before:
            expire_time["Before"] = args.expire_before
        payload["ExpireTime"] = expire_time

    # Sorting
    if args.sort_field:
        payload["Sort"] = {
            "Field": args.sort_field,
            "Order": args.sort_order or "Desc"
        }

    # Pagination
    if args.offset is not None:
        payload["Offset"] = args.offset
    if args.limit is not None:
        payload["Limit"] = args.limit

    # Return field filter
    if args.filters:
        payload["Filters"] = args.filters

    # dry-run mode
    if args.dry_run:
        if args.app_name:
            payload["_app_name"] = args.app_name
            payload["_note"] = "app_name will be resolved to SubAppId at actual execution time"
        print("[DRY RUN] Request parameters:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return None

    # Build request
    client = get_client(args.region) if not (args.app_name and not args.dry_run) else client

    req = models.SearchMediaRequest()
    req.from_json_string(json.dumps(payload, ensure_ascii=False))

    try:
        resp = client.SearchMedia(req)
        result = json.loads(resp.to_json_string())

        total = result.get("TotalCount", 0)
        media_list = result.get("MediaInfoSet", [])
        request_id = result.get("RequestId", "N/A")

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result

        # Human-readable output
        print(f"🔍 Search complete!")
        print(f"  Total matches: {total}")
        print(f"  Returned this page: {len(media_list)} item(s)")
        print(f"  RequestId: {request_id}")

        if not media_list:
            print("\nNo matching media files found.")
            return result

        for i, media in enumerate(media_list, 1):
            print_media_info(media, index=i, verbose=args.verbose)

        # Pagination hint
        offset = args.offset or 0
        limit = args.limit or 10
        if total > offset + limit:
            next_offset = offset + limit
            print(f"\n📄 {total - next_offset} more result(s) available, use --offset {next_offset} to view the next page")  # NOCA:line-too-long(long SDK parameter or URL string)

        return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        error_msg = str(e)
        print(f"❌ Search failed: {error_msg}")
        sys.exit(1)



def main():
    parser = argparse.ArgumentParser(
        description='VOD Search Media Tool (SearchMedia)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Scenario Notes:
  SearchMedia is used to search media by conditions (fuzzy name match, category, tags, etc.)
  DescribeMediaInfos (vod_describe_media.py) is used for exact lookup by FileId

  When the user provides a FileId, both scripts can be used:
    - Exact detail query → vod_describe_media.py --file-id xxx
    - Search-style query → vod_search_media.py --file-ids xxx

Examples:
  # ✅ Fuzzy search by name (main app)
  python vod_search_media.py --names "my video"

  # Search by FileId (main app)
  python vod_search_media.py --file-ids 387702292285462759

  # ✅ Fuzzy search by name (specified app)
  python vod_search_media.py --names "my video" --sub-app-id 1500046806

  # ✅ Fuzzy match by app name + name search
  python vod_search_media.py --names "my video" --app-name "test app"

  # Search video files
  python vod_search_media.py --names "test" --categories Video

  # Search image files
  python vod_search_media.py --names "cover" --categories Image

  # Search by tags
  python vod_search_media.py --tags "sports" "basketball"

  # Search by creation time range
  python vod_search_media.py --names "meeting" \\
      --create-after "2026-01-01T00:00:00+08:00" \\
      --create-before "2026-03-31T23:59:59+08:00"

  # Sort by creation time descending
  python vod_search_media.py --names "test" \\
      --sort-field CreateTime --sort-order Desc

  # Paginated query
  python vod_search_media.py --names "video" --offset 0 --limit 20

  # Return basic info only
  python vod_search_media.py --names "video" --filters basicInfo

  # JSON format output
  python vod_search_media.py --names "video" --json

  # Preview request parameters
  python vod_search_media.py --names "video" --dry-run
        '''
    )

    # Application selection (mutually exclusive)
    app_group = parser.add_argument_group('Application Selection')
    app_group.add_argument('--sub-app-id', type=int,
                           default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                           help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long SDK parameter or URL string)
    app_group.add_argument('--app-name',
                           help='Fuzzy match sub-application by name/description (mutually exclusive with --sub-app-id)')  # NOCA:line-too-long(long SDK parameter or URL string)

    # Search conditions
    search_group = parser.add_argument_group('Search Conditions')
    search_group.add_argument('--file-ids', nargs='+',
                              help='File ID list (exact match, up to 10)')
    search_group.add_argument('--names', nargs='+',
                              help='File name list (fuzzy match, up to 10)')
    search_group.add_argument('--name-prefixes', nargs='+',
                              help='File name prefix list (prefix match, up to 10)')
    search_group.add_argument('--descriptions', nargs='+',
                              help='Description list (fuzzy match, up to 10)')
    search_group.add_argument('--tags', nargs='+',
                              help='Tag list (match any tag, up to 16)')
    search_group.add_argument('--class-ids', nargs='+', type=int,
                              help='Category ID list (match category and subcategories, up to 10)')
    search_group.add_argument('--categories', nargs='+',
                              choices=['Video', 'Audio', 'Image'],
                              help='File type: Video/Audio/Image')
    search_group.add_argument('--source-types', nargs='+',
                              help='Source type: Record/Upload/VideoProcessing/TrtcRecord, etc.')
    search_group.add_argument('--media-types', nargs='+',
                              help='Container format: mp4/mp3/flv/jpg, etc.')
    search_group.add_argument('--status', nargs='+',
                              choices=['Normal', 'SystemForbidden', 'Forbidden'],
                              help='File status: Normal/SystemForbidden/Forbidden')
    search_group.add_argument('--review-results', nargs='+',
                              choices=['pass', 'review', 'block', 'notModerated'],
                              help='Review result: pass/review/block/notModerated')
    search_group.add_argument('--storage-regions', nargs='+',
                              help='Storage region: ap-chongqing, etc.')
    search_group.add_argument('--storage-classes', nargs='+',
                              choices=['STANDARD', 'STANDARD_IA', 'ARCHIVE', 'DEEP_ARCHIVE'],
                              help='Storage class: STANDARD/STANDARD_IA/ARCHIVE/DEEP_ARCHIVE')
    search_group.add_argument('--stream-ids', nargs='+',
                              help='Live stream push code list (match any, up to 10)')
    search_group.add_argument('--trtc-sdk-app-ids', nargs='+', type=int,
                              help='TRTC application ID list (match any, up to 10)')
    search_group.add_argument('--trtc-room-ids', nargs='+',
                              help='TRTC room ID list (match any, up to 10)')
    search_group.add_argument('--stream-domains', nargs='+',
                              help='Live stream push domain list (valid for live recording)')
    search_group.add_argument('--stream-paths', nargs='+',
                              help='Live stream push path list (valid for live recording)')

    # Time range
    time_group = parser.add_argument_group('Time Range')
    time_group.add_argument('--create-after',
                            help='Creation time start (ISO 8601, e.g. 2026-01-01T00:00:00+08:00)')
    time_group.add_argument('--create-before',
                            help='Creation time end (ISO 8601, e.g. 2026-12-31T23:59:59+08:00)')
    time_group.add_argument('--expire-after',
                            help='Expiration time start (ISO 8601, expired files cannot be retrieved)')
    time_group.add_argument('--expire-before',
                            help='Expiration time end (ISO 8601)')

    # Sorting and pagination
    page_group = parser.add_argument_group('Sorting and Pagination')
    page_group.add_argument('--sort-field', choices=['CreateTime'],
                            help='Sort field (when Names/Descriptions are provided, sorted by relevance and this parameter is ignored)')  # NOCA:line-too-long(long SDK parameter or URL string)
    page_group.add_argument('--sort-order', choices=['Asc', 'Desc'], default='Desc',
                            help='Sort order: Asc (ascending) / Desc (descending), default Desc')
    page_group.add_argument('--offset', type=int,
                            help='Pagination offset, default 0')
    page_group.add_argument('--limit', type=int,
                            help='Number of results to return, default 10 (Offset + Limit must not exceed 5000)')

    # Output control
    output_group = parser.add_argument_group('Output Control')
    output_group.add_argument('--filters', nargs='+',
                              help='Response filter: basicInfo/metaData/transcodeInfo/animatedGraphicsInfo, etc.')
    output_group.add_argument('--verbose', '-v', action='store_true',
                              help='Show detailed information (including URLs, etc.)')
    output_group.add_argument('--json', action='store_true',
                              help='Output full response in JSON format')
    output_group.add_argument('--region', default='ap-guangzhou',
                              help='Region, default ap-guangzhou')
    output_group.add_argument('--dry-run', action='store_true',
                              help='Preview request parameters without actually executing')

    args = parser.parse_args()

    # Validation: at least one search condition is required
    has_condition = any([
        args.file_ids, args.names, args.name_prefixes, args.descriptions,
        args.tags, args.class_ids, args.categories, args.source_types,
        args.media_types, args.status, args.review_results,
        args.storage_regions, args.storage_classes,
        args.stream_ids, args.trtc_sdk_app_ids, args.trtc_room_ids,
        args.stream_domains, args.stream_paths,
        args.create_after, args.create_before,
        args.expire_after, args.expire_before
    ])

    if not has_condition:
        print("Error: at least one search condition must be specified.")
        print("Use --help to see available search conditions.")
        print("\nCommon search conditions:")
        print("  --names \"video name\"   fuzzy search by name")
        print("  --file-ids FileId      search by file ID")
        print("  --tags \"tag\"           search by tag")
        print("  --categories Video     search by file type")
        sys.exit(1)

    # Validate that --app-name and --sub-app-id are mutually exclusive
    if args.app_name and args.sub_app_id:
        print("Error: --app-name and --sub-app-id cannot be specified at the same time")
        sys.exit(1)

    search_media(args)


if __name__ == '__main__':
    main()
