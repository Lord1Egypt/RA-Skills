#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD Media Processing Script
Supports standard transcoding, Top Speed Codec (TESHD) transcoding, remuxing, video enhancement, scene transcoding,
screenshots, animated image conversion, and adaptive bitrate streaming tasks

Top Speed Codec (TESHD) transcoding templates:
- Save 50%+ bandwidth costs while maintaining or even improving video quality
- Supports multiple quality levels: same-source / smooth / standard definition / high definition

Remux templates:
- No re-encoding of video or audio required; only the container format is converted
- Supports MP4 and HLS formats

Video enhancement templates (Large Model Enhancement V2):
- Noise reduction + super resolution + comprehensive enhancement, frame rate follows source
- General scene / Anime scene / Live-action short drama scene
- Supports 720P / 1080P / 2K / 4K

Scene transcoding templates:
- Short drama scene: Specifically improves character recognition
- E-commerce scene: Efficiently compresses video size
- Feed stream scene: Improves playback smoothness
"""

import os
import sys
import json
import argparse
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from vod_auto_upgrade import check_sdk_version
check_sdk_version()

# Soft dependency: vod_load_env is used as a fallback to load credentials from ~/.env etc. when env vars are missing
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
    """Get the VOD client"""
    cred = get_credential()
    http_profile = HttpProfile()
    http_profile.endpoint = "vod.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return vod_client.VodClient(cred, region, client_profile)


# Top Speed Codec (TESHD) transcoding template definitions
# Applies adaptive optimization for different video types, delivering higher-quality viewing at lower bandwidth
# Saves 50%+ bandwidth costs while maintaining or even improving video quality
TESHD_TRANSCODE_TEMPLATES = {
    "same": {
        "id": 100800,
        "desc": "TESHD, MP4 container, same-source resolution, preserves original video resolution and audio parameters, high quality at low bitrate",  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
        "resolution": "Same source",
    },
    "flu": {
        "id": 100810,
        "desc": "TESHD, MP4 container, smooth quality (360P), low bitrate saves traffic, suitable for fast loading on mobile networks",  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
        "resolution": "Proportional scaling × 360",
    },
    "sd": {
        "id": 100820,
        "desc": "TESHD, MP4 container, standard definition (540P), low bitrate reduces costs, suitable for multi-terminal distribution of standard videos",  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
        "resolution": "Proportional scaling × 540",
    },
    "hd": {
        "id": 100830,
        "desc": "TESHD, MP4 container, high definition (720P), low bitrate reduces costs, suitable for HD video distribution and online education",  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
        "resolution": "Proportional scaling × 720",
    },
}

# Remux template definitions
# No re-encoding of video or audio required; only the container format is converted, with no loss in video or audio quality  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
REMUX_TEMPLATES = {
    "mp4": {
        "id": 875,
        "desc": "Remux to MP4 format, no re-encoding required, no loss in video or audio quality, suitable for playback across all terminals",  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
    },
    "hls": {
        "id": 876,
        "desc": "Remux to HLS format, no re-encoding required, no loss in video or audio quality, suitable for web playback and live stream distribution",  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
    },
}

# Video enhancement template definitions (Large Model Enhancement V2)
# Noise reduction + super resolution + comprehensive enhancement, frame rate follows source
VIDEO_ENHANCE_TEMPLATES = {
    # General scene
    "general": {
        "720":  {"id": 101410, "desc": "Large Model Enhancement-V2-720P-Noise Reduction+Super Resolution+Comprehensive Enhancement"},  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
        "1080": {"id": 101430, "desc": "Large Model Enhancement-V2-1080P-Noise Reduction+Super Resolution+Comprehensive Enhancement"},  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
        "2k":   {"id": 101450, "desc": "Large Model Enhancement-V2-2K-Noise Reduction+Super Resolution+Comprehensive Enhancement"},  # NOCA:line-too-long(long output string or argparse help text, cannot be shortened)
        "4k":   {"id": 101470, "desc": "Large Model Enhancement-V2-4K-Noise Reduction+Super Resolution+Comprehensive Enhancement"},  # NOCA:line-too-long(content cannot be shortened)
    },
    # Anime scene
    "anime": {
        "720":  {"id": 101510, "desc": "Anime Scene-Large Model Enhancement-720P-Noise Reduction+Super Resolution+Comprehensive Enhancement"},  # NOCA:line-too-long(content cannot be shortened)
        "1080": {"id": 101530, "desc": "Anime Scene-Large Model Enhancement-1080P-Noise Reduction+Super Resolution+Comprehensive Enhancement"},  # NOCA:line-too-long(content cannot be shortened)
        "2k":   {"id": 101550, "desc": "Anime Scene-Large Model Enhancement-2K-Noise Reduction+Super Resolution+Comprehensive Enhancement"},  # NOCA:line-too-long(content cannot be shortened)
        "4k":   {"id": 101570, "desc": "Anime Scene-Large Model Enhancement-4K-Noise Reduction+Super Resolution+Comprehensive Enhancement"},  # NOCA:line-too-long(content cannot be shortened)
    },
    # Live-action / short drama scene
    "live_action": {
        "720":  {"id": 101520, "desc": "Live-action/Short Drama Scene-Large Model Enhancement-720P-Noise Reduction+Super Resolution+Comprehensive Enhancement"},  # NOCA:line-too-long(content cannot be shortened)
        "1080": {"id": 101540, "desc": "Live-action/Short Drama Scene-Large Model Enhancement-1080P-Noise Reduction+Super Resolution+Comprehensive Enhancement"},  # NOCA:line-too-long(content cannot be shortened)
        "2k":   {"id": 101560, "desc": "Live-action/Short Drama Scene-Large Model Enhancement-2K-Noise Reduction+Super Resolution+Comprehensive Enhancement"},  # NOCA:line-too-long(content cannot be shortened)
        "4k":   {"id": 101580, "desc": "Live-action/Short Drama Scene-Large Model Enhancement-4K-Noise Reduction+Super Resolution+Comprehensive Enhancement"},  # NOCA:line-too-long(content cannot be shortened)
    },
}

# Scene transcoding template definitions
SCENE_TRANSCODE_TEMPLATES = {
    # Short drama scene - specifically improves character recognition
    "short_drama": {
        "1080_best": 101300,      # Short drama_Overall best_1080
        "1080_quality": 101301,   # Short drama_Quality priority_1080
        "1080_bitrate": 101302,   # Short drama_Bitrate priority_1080
        "720_best": 101303,       # Short drama_Overall best_720
        "720_quality": 101304,    # Short drama_Quality priority_720
        "720_bitrate": 101305,    # Short drama_Bitrate priority_720
        "480_best": 101306,       # Short drama_Overall best_480
        "480_quality": 101307,    # Short drama_Quality priority_480
        "480_bitrate": 101308,    # Short drama_Bitrate priority_480
    },
    # E-commerce scene - efficiently compresses video size
    "ecommerce": {
        "1080_best": 101309,      # E-commerce_Overall best_1080
        "1080_quality": 101310,   # E-commerce_Quality priority_1080
        "1080_bitrate": 101311,   # E-commerce_Bitrate priority_1080
        "720_best": 101312,       # E-commerce_Overall best_720
        "720_quality": 101313,    # E-commerce_Quality priority_720
        "720_bitrate": 101314,    # E-commerce_Bitrate priority_720
        "480_best": 101315,       # E-commerce_Overall best_480
        "480_quality": 101316,    # E-commerce_Quality priority_480
        "480_bitrate": 101317,    # E-commerce_Bitrate priority_480
    },
    # Feed stream scene - improves playback smoothness
    "feed": {
        "1080_best": 101318,      # Feed_Overall best_1080
        "1080_quality": 101319,   # Feed_Quality priority_1080
        "1080_bitrate": 101320,   # Feed_Bitrate priority_1080
        "720_best": 101321,       # Feed_Overall best_720
        "720_quality": 101322,    # Feed_Quality priority_720
        "720_bitrate": 101323,    # Feed_Bitrate priority_720
        "480_best": 101324,       # Feed_Overall best_480
        "480_quality": 101325,    # Feed_Quality priority_480
        "480_bitrate": 101326,    # Feed_Bitrate priority_480
    },
}


def get_scene_transcode_template_id(scene, resolution="1080", priority="best"):
    """
    Get the scene transcoding template ID

    Args:
        scene: Scene type (short_drama/ecommerce/feed)
        resolution: Resolution (1080/720/480)
        priority: Priority (best/quality/bitrate)

    Returns:
        Template ID or None
    """
    scene_templates = SCENE_TRANSCODE_TEMPLATES.get(scene)
    if not scene_templates:
        return None

    key = f"{resolution}_{priority}"
    return scene_templates.get(key)


def process_by_procedure(args):
    """Process media using a task flow"""
    # dry-run mode does not require authentication, check first
    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  ProcedureName: {args.procedure}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  MediaStoragePath: {args.media_storage_path}")
        print(f"  TasksNotifyMode: {args.tasks_notify_mode}")
        print(f"  SessionId: {args.session_id}")
        print(f"  ExtInfo: {args.ext_info}")
        print(f"  TasksPriority: {args.tasks_priority}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id
    req.ProcedureName = args.procedure

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority
    if args.media_storage_path:
        req.MediaStoragePath = args.media_storage_path
    if args.tasks_notify_mode:
        req.TasksNotifyMode = args.tasks_notify_mode
    if args.session_id:
        req.SessionId = args.session_id
    if args.ext_info:
        req.ExtInfo = args.ext_info

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        print(f"Processing task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"Processing failed: {e}")
        sys.exit(1)


def teshd_transcode(args):
    """Top Speed Codec (TESHD) transcoding - delivers higher-quality viewing at lower bandwidth, saving 50%+ bandwidth costs"""  # NOCA:line-too-long(content cannot be shortened)
    # Get template
    template = TESHD_TRANSCODE_TEMPLATES.get(args.quality)
    if not template:
        print(f"Error: Invalid quality level: {args.quality}")
        print(f"Available levels: same (same-source), flu (smooth 360P), sd (standard definition 540P), hd (high definition 720P)")  # NOCA:line-too-long(content cannot be shortened)
        sys.exit(1)

    template_id = template["id"]

    if args.dry_run:
        print("[DRY RUN] TESHD transcoding request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Quality: {args.quality}")
        print(f"  TemplateId: {template_id}")
        print(f"  Description: {template['desc']}")
        print(f"  Resolution: {template['resolution']}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Build transcoding task
    transcode_task = models.TranscodeTaskInput()
    transcode_task.Definition = template_id

    # Build watermark list
    if args.watermark_set:
        watermark_list = []
        for wm_def in args.watermark_set.split(','):
            wm = models.WatermarkInput()
            wm.Definition = int(wm_def.strip())
            watermark_list.append(wm)
        transcode_task.WatermarkSet = watermark_list

    media_process_task = models.MediaProcessTaskInput()
    media_process_task.TranscodeTaskSet = [transcode_task]
    req.MediaProcessTask = media_process_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.session_context:
        req.SessionContext = args.session_context
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        quality_names = {
            "same": "Same source",
            "flu": "Smooth (360P)",
            "sd": "Standard definition (540P)",
            "hd": "High definition (720P)",
        }

        print(f"TESHD transcoding task submitted!")
        print(f"Quality level: {quality_names.get(args.quality, args.quality)}")
        print(f"Template ID: {template_id}")
        print(f"Description: {template['desc']}")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"TESHD transcoding failed: {e}")
        sys.exit(1)



def remux(args):
    """Remux - Convert video container format without re-encoding, no loss in video or audio quality"""
    # Get template
    template = REMUX_TEMPLATES.get(args.target_format)
    if not template:
        print(f"Error: Invalid target format: {args.target_format}")
        print(f"Available formats: mp4, hls")
        sys.exit(1)

    template_id = template["id"]

    if args.dry_run:
        print("[DRY RUN] Remux request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Format: {args.target_format}")
        print(f"  TemplateId: {template_id}")
        print(f"  Description: {template['desc']}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Remux uses a transcode task, but the template is a remux template (no re-encoding required)
    transcode_task = models.TranscodeTaskInput()
    transcode_task.Definition = template_id

    media_process_task = models.MediaProcessTaskInput()
    media_process_task.TranscodeTaskSet = [transcode_task]
    req.MediaProcessTask = media_process_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.session_context:
        req.SessionContext = args.session_context
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        print(f"Remux task submitted!")
        print(f"Target format: {args.target_format.upper()}")
        print(f"Template ID: {template_id}")
        print(f"Description: {template['desc']}")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"Remux failed: {e}")
        sys.exit(1)


def video_enhance(args):
    """Video enhancement - Large model enhancement V2, denoising + super resolution + comprehensive enhancement"""
    # Get scene template
    scene_templates = VIDEO_ENHANCE_TEMPLATES.get(args.scene)
    if not scene_templates:
        print(f"Error: Invalid enhancement scene: {args.scene}")
        print(f"Available scenes: general, anime, live_action")
        sys.exit(1)

    template = scene_templates.get(args.resolution)
    if not template:
        print(f"Error: Invalid resolution: {args.resolution}")
        print(f"Available resolutions: 720, 1080, 2k, 4k")
        sys.exit(1)

    template_id = template["id"]

    if args.dry_run:
        print("[DRY RUN] Video enhancement request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Scene: {args.scene}")
        print(f"  Resolution: {args.resolution}")
        print(f"  TemplateId: {template_id}")
        print(f"  Description: {template['desc']}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Video enhancement uses a transcode task with a video enhancement preset template
    transcode_task = models.TranscodeTaskInput()
    transcode_task.Definition = template_id

    media_process_task = models.MediaProcessTaskInput()
    media_process_task.TranscodeTaskSet = [transcode_task]
    req.MediaProcessTask = media_process_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.session_context:
        req.SessionContext = args.session_context
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        scene_names = {
            "general": "General",
            "anime": "Anime",
            "live_action": "Live Action / Short Drama",
        }

        print(f"Video enhancement task submitted!")
        print(f"Enhancement scene: {scene_names.get(args.scene, args.scene)}")
        print(f"Target resolution: {args.resolution}")
        print(f"Template ID: {template_id}")
        print(f"Description: {template['desc']}")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"Video enhancement failed: {e}")
        sys.exit(1)


def scene_transcode(args):
    """Scene-based transcoding - Scene-specific transcoding based on Top-Speed Codec"""
    # Get template ID
    template_id = get_scene_transcode_template_id(args.scene, args.resolution, args.priority)
    if not template_id:
        print(f"Error: Invalid scene transcode parameters")
        print(f"Scene: {args.scene}, Resolution: {args.resolution}, Priority: {args.priority}")
        print(f"Available scenes: short_drama, ecommerce, feed")
        sys.exit(1)

    # dry-run mode does not require authentication, check first
    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Scene: {args.scene}")
        print(f"  Resolution: {args.resolution}P")
        print(f"  Priority: {args.priority}")
        print(f"  TemplateId: {template_id}")
        print(f"  SessionContext: {args.session_context}")
        print(f"  TasksPriority: {args.tasks_priority}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Build transcode task
    transcode_task = models.TranscodeTaskInput()
    transcode_task.Definition = template_id

    # Build media processing task
    media_process_task = models.MediaProcessTaskInput()
    media_process_task.TranscodeTaskSet = [transcode_task]
    req.MediaProcessTask = media_process_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.session_context:
        req.SessionContext = args.session_context
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        scene_names = {
            "short_drama": "Short Drama",
            "ecommerce": "E-commerce",
            "feed": "Feed"
        }
        priority_names = {
            "best": "Overall Best",
            "quality": "Quality Priority",
            "bitrate": "Bitrate Priority"
        }

        print(f"Scene transcode task submitted!")
        print(f"Scene: {scene_names.get(args.scene, args.scene)}")
        print(f"Resolution: {args.resolution}P")
        print(f"Strategy: {priority_names.get(args.priority, args.priority)}")
        print(f"Template ID: {template_id}")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"Scene transcode failed: {e}")
        sys.exit(1)


def make_snapshot(args):
    """Take a media snapshot - using the ProcessMedia API"""
    # dry-run mode does not require authentication, check first
    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Definition: {args.definition}")
        print(f"  ExtTimeOffsetSet: {args.ext_time_offset_set}")
        print(f"  WatermarkSet: {args.watermark_set}")
        print(f"  MediaStoragePath: {args.media_storage_path}")
        print(f"  SessionId: {args.session_id}")
        print(f"  ExtInfo: {args.ext_info}")
        print(f"  TasksPriority: {args.tasks_priority}")
        print(f"  TasksNotifyMode: {args.tasks_notify_mode}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Build snapshot task
    snapshot_task = models.SnapshotByTimeOffsetTaskInput()
    snapshot_task.Definition = args.definition
    if args.ext_time_offset_set:
        snapshot_task.ExtTimeOffsetSet = args.ext_time_offset_set.split(',')

    # Build watermark list
    if args.watermark_set:
        watermark_list = []
        for wm_def in args.watermark_set.split(','):
            wm = models.WatermarkInput()
            wm.Definition = int(wm_def.strip())
            watermark_list.append(wm)
        snapshot_task.WatermarkSet = watermark_list

    # Build media processing task
    media_process_task = models.MediaProcessTaskInput()
    media_process_task.SnapshotByTimeOffsetTaskSet = [snapshot_task]
    req.MediaProcessTask = media_process_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.media_storage_path:
        req.MediaStoragePath = args.media_storage_path
    if args.session_id:
        req.SessionId = args.session_id
    if args.ext_info:
        req.ExtInfo = args.ext_info
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority
    if args.tasks_notify_mode:
        req.TasksNotifyMode = args.tasks_notify_mode

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        print(f"Snapshot task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"Snapshot failed: {e}")
        sys.exit(1)



def make_animated_graphics(args):
    """Animated GIF - using ProcessMedia API"""
    # dry-run mode does not require authentication, check first
    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Definition: {args.definition}")
        print(f"  StartTimeOffset: {args.start_time}")
        print(f"  EndTimeOffset: {args.end_time}")
        print(f"  MediaStoragePath: {args.media_storage_path}")
        print(f"  SessionId: {args.session_id}")
        print(f"  ExtInfo: {args.ext_info}")
        print(f"  TasksPriority: {args.tasks_priority}")
        print(f"  TasksNotifyMode: {args.tasks_notify_mode}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Build animated graphics task
    gif_task = models.AnimatedGraphicTaskInput()
    gif_task.Definition = args.definition
    if args.start_time is not None:
        gif_task.StartTimeOffset = args.start_time
    if args.end_time is not None:
        gif_task.EndTimeOffset = args.end_time

    # Build media processing task
    media_process_task = models.MediaProcessTaskInput()
    media_process_task.AnimatedGraphicTaskSet = [gif_task]
    req.MediaProcessTask = media_process_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.media_storage_path:
        req.MediaStoragePath = args.media_storage_path
    if args.session_id:
        req.SessionId = args.session_id
    if args.ext_info:
        req.ExtInfo = args.ext_info
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority
    if args.tasks_notify_mode:
        req.TasksNotifyMode = args.tasks_notify_mode

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        print(f"Animated graphics task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"Animated graphics failed: {e}")
        sys.exit(1)


def sample_snapshot(args):
    """Sample snapshot - using ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Definition: {args.definition}")
        print(f"  WatermarkSet: {args.watermark_set}")
        print(f"  MediaStoragePath: {args.media_storage_path}")
        print(f"  SessionId: {args.session_id}")
        print(f"  ExtInfo: {args.ext_info}")
        print(f"  TasksPriority: {args.tasks_priority}")
        print(f"  TasksNotifyMode: {args.tasks_notify_mode}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Build sample snapshot task
    sample_task = models.SampleSnapshotTaskInput()
    sample_task.Definition = args.definition

    # Build watermark list
    if args.watermark_set:
        watermark_list = []
        for wm_def in args.watermark_set.split(','):
            wm = models.WatermarkInput()
            wm.Definition = int(wm_def.strip())
            watermark_list.append(wm)
        sample_task.WatermarkSet = watermark_list

    # Build media processing task
    media_process_task = models.MediaProcessTaskInput()
    media_process_task.SampleSnapshotTaskSet = [sample_task]
    req.MediaProcessTask = media_process_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.media_storage_path:
        req.MediaStoragePath = args.media_storage_path
    if args.session_id:
        req.SessionId = args.session_id
    if args.ext_info:
        req.ExtInfo = args.ext_info
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority
    if args.tasks_notify_mode:
        req.TasksNotifyMode = args.tasks_notify_mode

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        print(f"Sample snapshot task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"Sample snapshot failed: {e}")
        sys.exit(1)


def image_sprite(args):
    """Image sprite - using ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Definition: {args.definition}")
        print(f"  WatermarkSet: {args.watermark_set}")
        print(f"  MediaStoragePath: {args.media_storage_path}")
        print(f"  SessionId: {args.session_id}")
        print(f"  ExtInfo: {args.ext_info}")
        print(f"  TasksPriority: {args.tasks_priority}")
        print(f"  TasksNotifyMode: {args.tasks_notify_mode}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Build image sprite task
    sprite_task = models.ImageSpriteTaskInput()
    sprite_task.Definition = args.definition

    # Build watermark list
    if args.watermark_set:
        watermark_list = []
        for wm_def in args.watermark_set.split(','):
            wm = models.WatermarkInput()
            wm.Definition = int(wm_def.strip())
            watermark_list.append(wm)
        sprite_task.WatermarkSet = watermark_list

    # Build media processing task
    media_process_task = models.MediaProcessTaskInput()
    media_process_task.ImageSpriteTaskSet = [sprite_task]
    req.MediaProcessTask = media_process_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.media_storage_path:
        req.MediaStoragePath = args.media_storage_path
    if args.session_id:
        req.SessionId = args.session_id
    if args.ext_info:
        req.ExtInfo = args.ext_info
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority
    if args.tasks_notify_mode:
        req.TasksNotifyMode = args.tasks_notify_mode

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        print(f"Image sprite task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"Image sprite failed: {e}")
        sys.exit(1)


def cover_by_snapshot(args):
    """Cover by snapshot - using ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Definition: {args.definition}")
        print(f"  PositionType: {args.position_type}")
        print(f"  PositionValue: {args.position_value}")
        print(f"  WatermarkSet: {args.watermark_set}")
        print(f"  MediaStoragePath: {args.media_storage_path}")
        print(f"  SessionId: {args.session_id}")
        print(f"  ExtInfo: {args.ext_info}")
        print(f"  TasksPriority: {args.tasks_priority}")
        print(f"  TasksNotifyMode: {args.tasks_notify_mode}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Build cover by snapshot task
    cover_task = models.CoverBySnapshotTaskInput()
    cover_task.Definition = args.definition
    cover_task.PositionType = args.position_type
    cover_task.PositionValue = args.position_value

    # Build watermark list
    if args.watermark_set:
        watermark_list = []
        for wm_def in args.watermark_set.split(','):
            wm = models.WatermarkInput()
            wm.Definition = int(wm_def.strip())
            watermark_list.append(wm)
        cover_task.WatermarkSet = watermark_list

    # Build media processing task
    media_process_task = models.MediaProcessTaskInput()
    media_process_task.CoverBySnapshotTaskSet = [cover_task]
    req.MediaProcessTask = media_process_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.media_storage_path:
        req.MediaStoragePath = args.media_storage_path
    if args.session_id:
        req.SessionId = args.session_id
    if args.ext_info:
        req.ExtInfo = args.ext_info
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority
    if args.tasks_notify_mode:
        req.TasksNotifyMode = args.tasks_notify_mode

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        print(f"Cover by snapshot task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"Cover by snapshot failed: {e}")
        sys.exit(1)



def adaptive_streaming(args):
    """Adaptive streaming - using ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Definition: {args.definition}")
        print(f"  SubtitleSet: {args.subtitle_set}")
        print(f"  MediaStoragePath: {args.media_storage_path}")
        print(f"  SessionId: {args.session_id}")
        print(f"  ExtInfo: {args.ext_info}")
        print(f"  TasksPriority: {args.tasks_priority}")
        print(f"  TasksNotifyMode: {args.tasks_notify_mode}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Build adaptive streaming task
    adaptive_task = models.AdaptiveDynamicStreamingTaskInput()
    adaptive_task.Definition = args.definition
    if args.subtitle_set:
        adaptive_task.SubtitleSet = args.subtitle_set.split(',')

    # Build media processing task
    media_process_task = models.MediaProcessTaskInput()
    media_process_task.AdaptiveDynamicStreamingTaskSet = [adaptive_task]
    req.MediaProcessTask = media_process_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.media_storage_path:
        req.MediaStoragePath = args.media_storage_path
    if args.session_id:
        req.SessionId = args.session_id
    if args.ext_info:
        req.ExtInfo = args.ext_info
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority
    if args.tasks_notify_mode:
        req.TasksNotifyMode = args.tasks_notify_mode

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        print(f"Adaptive streaming task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"Adaptive streaming failed: {e}")
        sys.exit(1)


def ai_content_review(args):
    """AI content review - using ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Definition: {args.definition}")
        print(f"  MediaStoragePath: {args.media_storage_path}")
        print(f"  SessionId: {args.session_id}")
        print(f"  ExtInfo: {args.ext_info}")
        print(f"  TasksPriority: {args.tasks_priority}")
        print(f"  TasksNotifyMode: {args.tasks_notify_mode}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Build AI content review task
    review_task = models.AiContentReviewTaskInput()
    review_task.Definition = args.definition
    req.AiContentReviewTask = review_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.media_storage_path:
        req.MediaStoragePath = args.media_storage_path
    if args.session_id:
        req.SessionId = args.session_id
    if args.ext_info:
        req.ExtInfo = args.ext_info
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority
    if args.tasks_notify_mode:
        req.TasksNotifyMode = args.tasks_notify_mode

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        print(f"AI content review task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"AI content review failed: {e}")
        sys.exit(1)


def ai_analysis(args):
    """AI content analysis - using ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Definition: {args.definition}")
        print(f"  MediaStoragePath: {args.media_storage_path}")
        print(f"  SessionId: {args.session_id}")
        print(f"  ExtInfo: {args.ext_info}")
        print(f"  TasksPriority: {args.tasks_priority}")
        print(f"  TasksNotifyMode: {args.tasks_notify_mode}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Build AI content analysis task
    analysis_task = models.AiAnalysisTaskInput()
    analysis_task.Definition = args.definition
    req.AiAnalysisTask = analysis_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.media_storage_path:
        req.MediaStoragePath = args.media_storage_path
    if args.session_id:
        req.SessionId = args.session_id
    if args.ext_info:
        req.ExtInfo = args.ext_info
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority
    if args.tasks_notify_mode:
        req.TasksNotifyMode = args.tasks_notify_mode

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        print(f"AI content analysis task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"AI content analysis failed: {e}")
        sys.exit(1)


def ai_recognition(args):
    """AI content recognition - using ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Definition: {args.definition}")
        print(f"  MediaStoragePath: {args.media_storage_path}")
        print(f"  SessionId: {args.session_id}")
        print(f"  ExtInfo: {args.ext_info}")
        print(f"  TasksPriority: {args.tasks_priority}")
        print(f"  TasksNotifyMode: {args.tasks_notify_mode}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # Build AI content recognition task
    recognition_task = models.AiRecognitionTaskInput()
    recognition_task.Definition = args.definition
    req.AiRecognitionTask = recognition_task

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id
    if args.media_storage_path:
        req.MediaStoragePath = args.media_storage_path
    if args.session_id:
        req.SessionId = args.session_id
    if args.ext_info:
        req.ExtInfo = args.ext_info
    if args.tasks_priority:
        req.TasksPriority = args.tasks_priority
    if args.tasks_notify_mode:
        req.TasksNotifyMode = args.tasks_notify_mode

    try:
        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        print(f"AI content recognition task submitted!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ Wait timed out ({args.max_wait}s), task is still running")
                print(f"📋 You can query manually later: python scripts/vod_describe_task.py --task-id {result['TaskId']}")  # NOCA:line-too-long(content cannot be shortened)
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"AI content recognition failed: {e}")
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

            # The Status field in VOD Describe Task Detail API is at the top level, not nested inside Task Detail
            status = result.get('Status', 'PROCESSING')
            print(f"  Current status: {status}")

            if status == 'FINISH':
                print("Task completed!")
                return result
            elif status == 'FAIL':
                err_msg = result.get('ErrCodeExt', '') or result.get('Message', '')
                print(f"Task failed! {err_msg}")
                return result

            time.sleep(5)
        # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
        except Exception as e:
            print(f"Failed to query task status: {e}")
            time.sleep(5)

    print(f"⏱️ Wait timed out ({max_wait}s), task is still running")
    return None



# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    parser = argparse.ArgumentParser(
        description='VOD media processing tool - supports TESHD transcoding/remuxing/scene transcoding/screenshot/animated graphics, etc.',  # NOCA:line-too-long(content cannot be shortened)
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python vod_process_media.py procedure --file-id <id> --procedure "SimpleAes"
  python vod_process_media.py transcode --file-id <id>                        # TESHD (same source)
  python vod_process_media.py transcode --file-id <id> --quality hd           # TESHD (720P)
  python vod_process_media.py remux --file-id <id> --target-format mp4        # Remux to MP4
  python vod_process_media.py enhance --file-id <id>                          # Video enhancement (general 1080P)
  python vod_process_media.py enhance --file-id <id> --scene anime --resolution 4k  # Anime 4K enhancement
  python vod_process_media.py scene-transcode --file-id <id> --scene short_drama
  python vod_process_media.py snapshot --file-id <id> --definition 10001 --ext-time-offset-set "5s,10s"

TESHD: same(100800)/flu(100810,360P)/sd(100820,540P)/hd(100830,720P)
Remux: mp4(875)/hls(876)
Enhance: general/anime/live_action x 720/1080/2k/4k (default: general 1080, id=101430)
Scene: short_drama/ecommerce/feed x 1080/720/480 x best/quality/bitrate
        '''
    )

    # Common parameters (via parent parser so all subcommands inherit -v/--verbose)
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('-v', '--verbose', action='store_true', help='Output detailed information (including full API response)')  # NOCA:line-too-long(content cannot be shortened)

    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # Procedure-based processing
    proc_parser = subparsers.add_parser('procedure', help='Process using a task flow', parents=[common_parser])
    proc_parser.add_argument('--file-id', required=True, help='Media FileId')
    proc_parser.add_argument('--procedure', required=True, help='Task flow name')
    proc_parser.add_argument('--sub-app-id', type=int,
                              default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                              help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(content cannot be shortened)
    proc_parser.add_argument('--media-storage-path', help='Media storage path (only available for FileID + Path mode sub-applications)')  # NOCA:line-too-long(content cannot be shortened)
    proc_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='Task flow status change notification mode')  # NOCA:line-too-long(content cannot be shortened)
    proc_parser.add_argument('--session-id', help='Deduplication identifier (duplicate within three days will return an error)')  # NOCA:line-too-long(content cannot be shortened)
    proc_parser.add_argument('--ext-info', help='Extended information')
    proc_parser.add_argument('--tasks-priority', type=int, help='Task priority')
    proc_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    proc_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    proc_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    proc_parser.add_argument('--json', action='store_true', help='JSON format output')
    proc_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # TESHD transcoding
    teshd_parser = subparsers.add_parser('transcode', help='Top Speed Codec (TESHD) transcoding - delivers higher quality at lower bandwidth, saving over half the bandwidth cost', parents=[common_parser])  # NOCA:line-too-long(content cannot be shortened)
    teshd_parser.add_argument('--file-id', required=True, help='Media FileId')
    teshd_parser.add_argument('--quality', default='same',
                              choices=['same', 'flu', 'sd', 'hd'],
                              help='Quality level: same(same source, default 100800)/flu(smooth 360P, 100810)/sd(standard 540P, 100820)/hd(high definition 720P, 100830)')  # NOCA:line-too-long(content cannot be shortened)
    teshd_parser.add_argument('--watermark-set', help='Watermark template ID list, comma-separated, e.g. "10001,10002"')
    teshd_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                               help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(content cannot be shortened)
    teshd_parser.add_argument('--session-context', help='Source context, used to pass through user request information')
    teshd_parser.add_argument('--tasks-priority', type=int, help='Task priority (-10 to 10)')
    teshd_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    teshd_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    teshd_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    teshd_parser.add_argument('--json', action='store_true', help='JSON format output')
    teshd_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # Remux
    remux_parser = subparsers.add_parser('remux', help='Remux (no re-encoding required, only converts container format, no quality loss)', parents=[common_parser])  # NOCA:line-too-long(content cannot be shortened)
    remux_parser.add_argument('--file-id', required=True, help='Media FileId')
    remux_parser.add_argument('--target-format', required=True, dest='target_format',
                              choices=['mp4', 'hls'],
                              help='Target container format: mp4(template 875)/hls(template 876)')
    remux_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                               help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(content cannot be shortened)
    remux_parser.add_argument('--session-context', help='Source context, used to pass through user request information')
    remux_parser.add_argument('--tasks-priority', type=int, help='Task priority (-10 to 10)')
    remux_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    remux_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    remux_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    remux_parser.add_argument('--json', action='store_true', help='JSON format output')
    remux_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # Video enhancement
    enhance_parser = subparsers.add_parser('enhance', help='Video enhancement (large model enhancement V2), noise reduction + super resolution + comprehensive enhancement', parents=[common_parser])  # NOCA:line-too-long(content cannot be shortened)
    enhance_parser.add_argument('--file-id', required=True, help='Media FileId')
    enhance_parser.add_argument('--scene', default='general',
                                choices=['general', 'anime', 'live_action'],
                                help='Enhancement scene: general(default)/anime/live_action(real person/short drama)')
    enhance_parser.add_argument('--resolution', default='1080',
                                choices=['720', '1080', '2k', '4k'],
                                help='Target resolution: 720/1080(default)/2k/4k')
    enhance_parser.add_argument('--sub-app-id', type=int,
                                 default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                 help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(content cannot be shortened)
    enhance_parser.add_argument('--session-context', help='Source context, used to pass through user request information')  # NOCA:line-too-long(content cannot be shortened)
    enhance_parser.add_argument('--tasks-priority', type=int, help='Task priority (-10 to 10)')
    enhance_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    enhance_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    enhance_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    enhance_parser.add_argument('--json', action='store_true', help='JSON format output')
    enhance_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # Scene transcoding
    scene_parser = subparsers.add_parser('scene-transcode', help='Scene transcoding (TESHD)', parents=[common_parser])
    scene_parser.add_argument('--file-id', required=True, help='Media FileId')
    scene_parser.add_argument('--scene', required=True,
                              choices=['short_drama', 'ecommerce', 'feed'],
                              help='Scene type: short_drama/ecommerce/feed(information feed)')
    scene_parser.add_argument('--resolution', default='1080',
                              choices=['1080', '720', '480'],
                              help='Output resolution (default: 1080)')
    scene_parser.add_argument('--priority', default='best',
                              choices=['best', 'quality', 'bitrate'],
                              help='Transcoding strategy: best(overall best)/quality(quality first)/bitrate(bitrate first) (default: best)')  # NOCA:line-too-long(content cannot be shortened)
    scene_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                               help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(content cannot be shortened)
    scene_parser.add_argument('--session-context', help='Source context, used to pass through user request information')
    scene_parser.add_argument('--tasks-priority', type=int, help='Task priority (-10 to 10)')
    scene_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    scene_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    scene_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    scene_parser.add_argument('--json', action='store_true', help='JSON format output')
    scene_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # Screenshot
    snap_parser = subparsers.add_parser('snapshot', help='Screenshot', parents=[common_parser])
    snap_parser.add_argument('--file-id', required=True, help='Media FileId')
    snap_parser.add_argument('--definition', type=int, required=True, help='Screenshot template ID')
    snap_parser.add_argument('--ext-time-offset-set', help='Screenshot time point list, comma-separated, e.g. "5s,10s,15s" or "10pct,20pct,30pct"')  # NOCA:line-too-long(content cannot be shortened)
    snap_parser.add_argument('--watermark-set', help='Watermark template ID list, comma-separated, e.g. "10001,10002"')
    snap_parser.add_argument('--sub-app-id', type=int,
                              default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                              help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(content cannot be shortened)
    snap_parser.add_argument('--media-storage-path', help='Media storage path (only available for FileID + Path mode sub-applications)')  # NOCA:line-too-long(content cannot be shortened)
    snap_parser.add_argument('--session-id', help='Deduplication identifier (duplicate within three days will return an error)')  # NOCA:line-too-long(content cannot be shortened)
    snap_parser.add_argument('--ext-info', help='Extended information')
    snap_parser.add_argument('--tasks-priority', type=int, help='Task priority')
    snap_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='Task status change notification mode')  # NOCA:line-too-long(content cannot be shortened)
    snap_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    snap_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    snap_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    snap_parser.add_argument('--json', action='store_true', help='JSON format output')
    snap_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # Animated graphics
    gif_parser = subparsers.add_parser('gif', help='Animated graphics', parents=[common_parser])
    gif_parser.add_argument('--file-id', required=True, help='Media FileId')
    gif_parser.add_argument('--definition', type=int, required=True, help='Animated graphics template ID')
    gif_parser.add_argument('--start-time', type=float, help='Start time offset (seconds)')
    gif_parser.add_argument('--end-time', type=float, help='End time offset (seconds)')
    gif_parser.add_argument('--sub-app-id', type=int,
                             default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                             help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(content cannot be shortened)
    gif_parser.add_argument('--media-storage-path', help='Media storage path (only available for FileID + Path mode sub-applications)')  # NOCA:line-too-long(content cannot be shortened)
    gif_parser.add_argument('--session-id', help='Deduplication identifier (duplicate within three days will return an error)')  # NOCA:line-too-long(content cannot be shortened)
    gif_parser.add_argument('--ext-info', help='Extended information')
    gif_parser.add_argument('--tasks-priority', type=int, help='Task priority')
    gif_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='Task status change notification mode')  # NOCA:line-too-long(content cannot be shortened)
    gif_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    gif_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    gif_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    gif_parser.add_argument('--json', action='store_true', help='JSON format output')
    gif_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # Sampled screenshot
    sample_parser = subparsers.add_parser('sample-snapshot', help='Sampled screenshot', parents=[common_parser])
    sample_parser.add_argument('--file-id', required=True, help='Media FileId')
    sample_parser.add_argument('--definition', type=int, required=True, help='Sampled screenshot template ID')
    sample_parser.add_argument('--watermark-set', help='Watermark template ID list, comma-separated, e.g. "10001,10002"')  # NOCA:line-too-long(content cannot be shortened)
    sample_parser.add_argument('--sub-app-id', type=int,
                                default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(content cannot be shortened)
    sample_parser.add_argument('--media-storage-path', help='Media storage path (only available for FileID + Path mode sub-applications)')  # NOCA:line-too-long(content cannot be shortened)
    sample_parser.add_argument('--session-id', help='Deduplication identifier (duplicate within three days will return an error)')  # NOCA:line-too-long(content cannot be shortened)
    sample_parser.add_argument('--ext-info', help='Extended information')
    sample_parser.add_argument('--tasks-priority', type=int, help='Task priority')
    sample_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='Task status change notification mode')  # NOCA:line-too-long(content cannot be shortened)
    sample_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    sample_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    sample_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    sample_parser.add_argument('--json', action='store_true', help='JSON format output')
    sample_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # Image sprite
    sprite_parser = subparsers.add_parser('image-sprite', help='Image sprite', parents=[common_parser])
    sprite_parser.add_argument('--file-id', required=True, help='Media FileId')
    sprite_parser.add_argument('--definition', type=int, required=True, help='Image sprite template ID')
    sprite_parser.add_argument('--watermark-set', help='Watermark template ID list, comma-separated, e.g. "10001,10002"')  # NOCA:line-too-long(content cannot be shortened)
    sprite_parser.add_argument('--sub-app-id', type=int,
                                default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(content cannot be shortened)
    sprite_parser.add_argument('--media-storage-path', help='Media storage path (only available for FileID + Path mode sub-applications)')  # NOCA:line-too-long(content cannot be shortened)
    sprite_parser.add_argument('--session-id', help='Deduplication identifier (duplicate within three days will return an error)')  # NOCA:line-too-long(content cannot be shortened)
    sprite_parser.add_argument('--ext-info', help='Extended information')
    sprite_parser.add_argument('--tasks-priority', type=int, help='Task priority')
    sprite_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='Task status change notification mode')  # NOCA:line-too-long(content cannot be shortened)
    sprite_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    sprite_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    sprite_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    sprite_parser.add_argument('--json', action='store_true', help='JSON format output')
    sprite_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # Cover by snapshot
    cover_parser = subparsers.add_parser('cover-by-snapshot', help='Set cover by screenshot', parents=[common_parser])
    cover_parser.add_argument('--file-id', required=True, help='Media FileId')
    cover_parser.add_argument('--definition', type=int, required=True, help='Screenshot template ID')
    cover_parser.add_argument('--position-type', required=True, choices=['Time', 'Percent'], help='Screenshot method: Time(time point)/Percent(percentage)')  # NOCA:line-too-long(long SDK parameter or URL string)
    cover_parser.add_argument('--position-value', type=float, required=True, help='Screenshot position: Time method unit is seconds, Percent method is 0-100 percentage')  # NOCA:line-too-long(long SDK parameter or URL string)
    cover_parser.add_argument('--watermark-set', help='Watermark template ID list, comma-separated, e.g. "10001,10002"')
    cover_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                               help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long SDK parameter or URL string)
    cover_parser.add_argument('--media-storage-path', help='Media storage path (only available for FileID + Path mode sub-applications)')  # NOCA:line-too-long(long SDK parameter or URL string)
    cover_parser.add_argument('--session-id', help='Deduplication identifier (duplicate within three days will return an error)')  # NOCA:line-too-long(long SDK parameter or URL string)
    cover_parser.add_argument('--ext-info', help='Extended information')
    cover_parser.add_argument('--tasks-priority', type=int, help='Task priority')
    cover_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='Task status change notification mode')  # NOCA:line-too-long(long SDK parameter or URL string)
    cover_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    cover_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    cover_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    cover_parser.add_argument('--json', action='store_true', help='JSON format output')
    cover_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # Adaptive streaming
    adaptive_parser = subparsers.add_parser('adaptive-streaming', help='Adaptive bitrate streaming', parents=[common_parser])  # NOCA:line-too-long(long SDK parameter or URL string)
    adaptive_parser.add_argument('--file-id', required=True, help='Media FileId')
    adaptive_parser.add_argument('--definition', type=int, required=True, help='Adaptive bitrate streaming template ID')
    adaptive_parser.add_argument('--subtitle-set', help='Subtitle ID list, comma-separated')
    adaptive_parser.add_argument('--sub-app-id', type=int,
                                  default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                  help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long SDK parameter or URL string)
    adaptive_parser.add_argument('--media-storage-path', help='Media storage path (only available for FileID + Path mode sub-applications)')  # NOCA:line-too-long(long SDK parameter or URL string)
    adaptive_parser.add_argument('--session-id', help='Deduplication identifier (duplicate within three days will return an error)')  # NOCA:line-too-long(long SDK parameter or URL string)
    adaptive_parser.add_argument('--ext-info', help='Extended information')
    adaptive_parser.add_argument('--tasks-priority', type=int, help='Task priority')
    adaptive_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='Task status change notification mode')  # NOCA:line-too-long(long SDK parameter or URL string)
    adaptive_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    adaptive_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    adaptive_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    adaptive_parser.add_argument('--json', action='store_true', help='JSON format output')
    adaptive_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # AI content review
    review_parser = subparsers.add_parser('ai-review', help='AI content review (not recommended, use ReviewAudioVideo instead)', parents=[common_parser])  # NOCA:line-too-long(long SDK parameter or URL string)
    review_parser.add_argument('--file-id', required=True, help='Media FileId')
    review_parser.add_argument('--definition', type=int, required=True, help='Audio/video review template ID')
    review_parser.add_argument('--sub-app-id', type=int,
                                default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long SDK parameter or URL string)
    review_parser.add_argument('--media-storage-path', help='Media storage path (only available for FileID + Path mode sub-applications)')  # NOCA:line-too-long(long SDK parameter or URL string)
    review_parser.add_argument('--session-id', help='Deduplication identifier (duplicate within three days will return an error)')  # NOCA:line-too-long(long SDK parameter or URL string)
    review_parser.add_argument('--ext-info', help='Extended information')
    review_parser.add_argument('--tasks-priority', type=int, help='Task priority')
    review_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='Task status change notification mode')  # NOCA:line-too-long(long SDK parameter or URL string)
    review_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    review_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    review_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    review_parser.add_argument('--json', action='store_true', help='JSON format output')
    review_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # AI content analysis
    analysis_parser = subparsers.add_parser('ai-analysis', help='AI content analysis', parents=[common_parser])
    analysis_parser.add_argument('--file-id', required=True, help='Media FileId')
    analysis_parser.add_argument('--definition', type=int, required=True, help='Video content analysis template ID')
    analysis_parser.add_argument('--sub-app-id', type=int,
                                  default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                  help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long SDK parameter or URL string)
    analysis_parser.add_argument('--media-storage-path', help='Media storage path (only available for FileID + Path mode sub-applications)')  # NOCA:line-too-long(long SDK parameter or URL string)
    analysis_parser.add_argument('--session-id', help='Deduplication identifier (duplicate within three days will return an error)')  # NOCA:line-too-long(long SDK parameter or URL string)
    analysis_parser.add_argument('--ext-info', help='Extended information')
    analysis_parser.add_argument('--tasks-priority', type=int, help='Task priority')
    analysis_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='Task status change notification mode')  # NOCA:line-too-long(long SDK parameter or URL string)
    analysis_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    analysis_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    analysis_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    analysis_parser.add_argument('--json', action='store_true', help='JSON format output')
    analysis_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    # AI content recognition
    recognition_parser = subparsers.add_parser('ai-recognition', help='AI content recognition', parents=[common_parser])
    recognition_parser.add_argument('--file-id', required=True, help='Media FileId')
    recognition_parser.add_argument('--definition', type=int, required=True, help='Video intelligent recognition template ID')  # NOCA:line-too-long(long SDK parameter or URL string)
    recognition_parser.add_argument('--sub-app-id', type=int,
                                     default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                     help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')  # NOCA:line-too-long(long SDK parameter or URL string)
    recognition_parser.add_argument('--media-storage-path', help='Media storage path (only available for FileID + Path mode sub-applications)')  # NOCA:line-too-long(long SDK parameter or URL string)
    recognition_parser.add_argument('--session-id', help='Deduplication identifier (duplicate within three days will return an error)')  # NOCA:line-too-long(long SDK parameter or URL string)
    recognition_parser.add_argument('--ext-info', help='Extended information')
    recognition_parser.add_argument('--tasks-priority', type=int, help='Task priority')
    recognition_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='Task status change notification mode')  # NOCA:line-too-long(long SDK parameter or URL string)
    recognition_parser.add_argument('--region', default='ap-guangzhou', help='Region')
    recognition_parser.add_argument('--no-wait', action='store_true', help='Submit task only, do not wait for result')
    recognition_parser.add_argument('--max-wait', type=int, default=600, help='Maximum wait time (seconds)')
    recognition_parser.add_argument('--json', action='store_true', help='JSON format output')
    recognition_parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    args = parser.parse_args()

    if args.command == 'procedure':
        process_by_procedure(args)
    elif args.command == 'transcode':
        teshd_transcode(args)
    elif args.command == 'remux':
        remux(args)
    elif args.command == 'enhance':
        video_enhance(args)
    elif args.command == 'scene-transcode':
        scene_transcode(args)
    elif args.command == 'snapshot':
        make_snapshot(args)
    elif args.command == 'gif':
        make_animated_graphics(args)
    elif args.command == 'sample-snapshot':
        sample_snapshot(args)
    elif args.command == 'image-sprite':
        image_sprite(args)
    elif args.command == 'cover-by-snapshot':
        cover_by_snapshot(args)
    elif args.command == 'adaptive-streaming':
        adaptive_streaming(args)
    elif args.command == 'ai-review':
        ai_content_review(args)
    elif args.command == 'ai-analysis':
        ai_analysis(args)
    elif args.command == 'ai-recognition':
        ai_recognition(args)
    else:
        parser.print_help()



if __name__ == '__main__':
    main()
