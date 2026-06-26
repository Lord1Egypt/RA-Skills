#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD Media Information Query Script
"""

import os
import sys
import json
import argparse

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


def _format_size(size_bytes):
    """Format file size"""
    if not size_bytes:
        return 'N/A'
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def _format_bitrate(bps):
    """Format bitrate"""
    if not bps:
        return 'N/A'
    if bps >= 1000000:
        return f"{bps/1000000:.2f} Mbps"
    elif bps >= 1000:
        return f"{bps/1000:.0f} kbps"
    return f"{bps} bps"


def _format_duration(seconds):
    """Format duration"""
    if seconds is None:
        return 'N/A'
    seconds = float(seconds)
    if seconds < 60:
        return f"{seconds:.3f} seconds"
    elif seconds < 3600:
        m = int(seconds // 60)
        s = seconds % 60
        return f"{m}m {s:.1f}s"
    else:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        return f"{h}h {m}m {s:.0f}s"


def _print_video_streams(streams, indent="    "):
    """Print video stream information"""
    if not streams:
        return
    for j, vs in enumerate(streams):
        codec = vs.get('Codec', 'N/A')
        codec_tag = vs.get('CodecTag', '')
        w = vs.get('Width', '?')
        h = vs.get('Height', '?')
        fps = vs.get('Fps', 'N/A')
        br = _format_bitrate(vs.get('Bitrate'))
        dri = vs.get('DynamicRangeInfo') or {}
        dr_type = dri.get('Type', '')
        hdr_type = dri.get('HDRType', '')
        dr_str = f"  {dr_type}" if dr_type else ""
        if hdr_type:
            dr_str += f"({hdr_type})"
        tag_str = f"/{codec_tag}" if codec_tag else ""
        print(f"{indent}Video Stream[{j}]: {codec}{tag_str}  {w}x{h}  {fps}fps  {br}{dr_str}")


def _print_audio_streams(streams, indent="    "):
    """Print audio stream information"""
    if not streams:
        return
    for j, aus in enumerate(streams):
        codec = aus.get('Codec', 'N/A')
        sr = aus.get('SamplingRate', 'N/A')
        br = _format_bitrate(aus.get('Bitrate'))
        print(f"{indent}Audio Stream[{j}]: {codec}  SampleRate={sr}Hz  {br}")


def _print_source_info(source_info, indent="  "):
    """Print source information"""
    if not source_info:
        return
    print(f"{indent}Source Type: {source_info.get('SourceType', 'N/A')}")
    ctx = source_info.get('SourceContext', '')
    if ctx:
        print(f"{indent}Source Context: {ctx}")

    live_info = source_info.get('LiveRecordInfo') or {}
    if live_info:
        print(f"{indent}Live Recording Info:")
        print(f"{indent}  Domain: {live_info.get('Domain', 'N/A')}")
        print(f"{indent}  Path: {live_info.get('Path', 'N/A')}")
        print(f"{indent}  Stream ID: {live_info.get('StreamId', 'N/A')}")
        print(f"{indent}  Record Start: {live_info.get('RecordStartTime', 'N/A')}")
        print(f"{indent}  Record End: {live_info.get('RecordEndTime', 'N/A')}")

    trtc_info = source_info.get('TrtcRecordInfo') or {}
    if trtc_info:
        print(f"{indent}TRTC Recording Info:")
        print(f"{indent}  SdkAppId: {trtc_info.get('SdkAppId', 'N/A')}")
        print(f"{indent}  RoomId: {trtc_info.get('RoomId', 'N/A')}")
        print(f"{indent}  TaskId: {trtc_info.get('TaskId', 'N/A')}")
        user_ids = trtc_info.get('UserIds') or []
        if user_ids:
            print(f"{indent}  Users: {', '.join(user_ids)}")

    web_info = source_info.get('WebPageRecordInfo') or {}
    if web_info:
        print(f"{indent}Web Page Recording Info:")
        print(f"{indent}  Record URL: {web_info.get('RecordUrl', 'N/A')}")
        print(f"{indent}  TaskId: {web_info.get('RecordTaskId', 'N/A')}")



# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def describe_media(args):
    """Query media information"""
    client = get_client(args.region)

    req = models.DescribeMediaInfosRequest()
    req.FileIds = args.file_id

    if args.filters:
        req.Filters = args.filters
    if args.sub_app_id:
        req.SubAppId = args.sub_app_id

    if args.dry_run:
        print("[DRY RUN] Request parameters:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return

    try:
        resp = client.DescribeMediaInfos(req)
        result = json.loads(resp.to_json_string())

        media_infos = result.get('MediaInfoSet', [])
        not_exist = result.get('NotExistFileIdSet', [])

        print(f"Query complete!")
        print(f"Media found: {len(media_infos)}")
        if not_exist:
            print(f"Non-existent FileId(s): {not_exist}")

        for idx, media in enumerate(media_infos):
            # FileId retrieved from top level
            file_id = media.get('FileId') or (args.file_id[idx] if idx < len(args.file_id) else 'N/A')

            # ===== Basic Info =====
            basic_info = media.get('BasicInfo') or {}
            if basic_info:
                print(f"\n  FileId: {file_id}")
                print(f"  Name: {basic_info.get('Name', 'N/A')}")
                desc = basic_info.get('Description', '')
                if desc:
                    print(f"  Description: {desc}")
                print(f"  Type: {basic_info.get('Type', 'N/A')}")
                print(f"  File Category: {basic_info.get('Category', 'N/A')}")
                print(f"  Status: {basic_info.get('Status', 'N/A')}")
                print(f"  Create Time: {basic_info.get('CreateTime', 'N/A')}")
                print(f"  Update Time: {basic_info.get('UpdateTime', 'N/A')}")
                expire = basic_info.get('ExpireTime', '')
                if expire and expire != '9999-12-31T23:59:59Z':
                    print(f"  Expire Time: {expire}")
                else:
                    print(f"  Expire Time: Never expires")

                class_name = basic_info.get('ClassName', '')
                class_path = basic_info.get('ClassPath', '')
                class_id = basic_info.get('ClassId')
                if class_name or class_path:
                    cls_str = class_path or class_name
                    if class_id is not None:
                        cls_str += f" (ID: {class_id})"
                    print(f"  Category: {cls_str}")

                cover = basic_info.get('CoverUrl', '')
                if cover:
                    print(f"  Cover URL: {cover}")
                media_url = basic_info.get('MediaUrl', '')
                if media_url:
                    print(f"  Media URL: {media_url}")

                tags = basic_info.get('TagSet') or []
                if tags:
                    print(f"  Tags: {', '.join(tags)}")

                print(f"  Storage Region: {basic_info.get('StorageRegion', 'N/A')}")
                storage_path = basic_info.get('StoragePath', '')
                if storage_path:
                    print(f"  Storage Path: {storage_path}")
                print(f"  Storage Class: {basic_info.get('StorageClass', 'N/A')}")

                vid = basic_info.get('Vid', '')
                if vid:
                    print(f"  Vid: {vid}")

                # Source information
                _print_source_info(basic_info.get('SourceInfo'), indent="  ")
            else:
                # Output at least FileId when Basic Info is absent
                print(f"\n  FileId: {file_id}")

            # ===== Meta Data =====
            meta_data = media.get('MetaData') or {}
            if meta_data:
                print(f"\n  --- Metadata ---")
                size = meta_data.get('Size')
                if size is not None:
                    print(f"  File Size: {_format_size(size)}")
                print(f"  Container: {meta_data.get('Container', 'N/A')}")
                print(f"  Duration: {_format_duration(meta_data.get('Duration'))}")
                vid_dur = meta_data.get('VideoDuration')
                aud_dur = meta_data.get('AudioDuration')
                if vid_dur is not None:
                    print(f"  Video Duration: {_format_duration(vid_dur)}")
                if aud_dur is not None:
                    print(f"  Audio Duration: {_format_duration(aud_dur)}")
                w = meta_data.get('Width')
                h = meta_data.get('Height')
                if w and h:
                    print(f"  Resolution: {w}x{h}")
                print(f"  Bitrate: {_format_bitrate(meta_data.get('Bitrate'))}")
                rotate = meta_data.get('Rotate')
                if rotate:
                    print(f"  Rotation: {rotate}°")
                md5 = meta_data.get('Md5', '')
                if md5:
                    print(f"  MD5: {md5}")

                _print_video_streams(meta_data.get('VideoStreamSet') or [], indent="  ")
                _print_audio_streams(meta_data.get('AudioStreamSet') or [], indent="  ")

            # ===== Transcode Info =====
            transcode_info = media.get('TranscodeInfo') or {}
            transcode_set = transcode_info.get('TranscodeSet') or []
            if transcode_set:
                print(f"\n  --- Transcode Results ({len(transcode_set)}) ---")
                for i, t in enumerate(transcode_set):
                    definition = t.get('Definition', 'N/A')
                    container = t.get('Container', 'N/A')
                    width = t.get('Width', '?')
                    height = t.get('Height', '?')
                    bitrate = t.get('Bitrate', 0)
                    size = t.get('Size', 0)
                    duration = t.get('Duration')
                    url = t.get('Url', 'N/A')
                    md5 = t.get('Md5', '')
                    dwm_type = t.get('DigitalWatermarkType', '')
                    crw_text = t.get('CopyRightWatermarkText', '')
                    bwm_def = t.get('BlindWatermarkDefinition')

                    bitrate_str = _format_bitrate(bitrate)
                    size_str = _format_size(size) if size else 'N/A'
                    dur_str = f"  Duration={_format_duration(duration)}" if duration else ""
                    print(f"    [{i+1}] TemplateID={definition}  Container={container}  {width}x{height}  Bitrate={bitrate_str}  Size={size_str}{dur_str}")
                    if md5:
                        print(f"        MD5: {md5}")
                    if dwm_type and dwm_type != 'None':
                        print(f"        Digital Watermark: {dwm_type}")
                    if crw_text and crw_text != 'None':
                        print(f"        Copyright Info: {crw_text}")
                    if bwm_def:
                        print(f"        Blind Watermark Template: {bwm_def}")
                    print(f"        URL: {url}")
                    _print_video_streams(t.get('VideoStreamSet') or [], indent="        ")
                    _print_audio_streams(t.get('AudioStreamSet') or [], indent="        ")

            # ===== Animated Graphics Info =====
            animated_info = media.get('AnimatedGraphicsInfo') or {}
            animated_set = animated_info.get('AnimatedGraphicsSet') or []
            if animated_set:
                print(f"\n  --- Animated Graphics Results ({len(animated_set)}) ---")
                for i, a in enumerate(animated_set):
                    container = a.get('Container', 'N/A')
                    start_off = a.get('StartTimeOffset')
                    end_off = a.get('EndTimeOffset')
                    time_str = ""
                    if start_off is not None and end_off is not None:
                        time_str = f"  Time={start_off}s→{end_off}s"
                    md5 = a.get('Md5', '')
                    print(f"    [{i+1}] TemplateID={a.get('Definition', 'N/A')}  Format={container}  {a.get('Width', '?')}x{a.get('Height', '?')}  Bitrate={_format_bitrate(a.get('Bitrate'))}  Size={_format_size(a.get('Size', 0))}{time_str}")
                    if md5:
                        print(f"        MD5: {md5}")
                    print(f"        URL: {a.get('Url', 'N/A')}")

            # ===== SnapshotBy Time Offset Info =====
            snapshot_info = media.get('SnapshotByTimeOffsetInfo') or {}
            snapshot_set = snapshot_info.get('SnapshotByTimeOffsetSet') or []
            if snapshot_set:
                print(f"\n  --- Snapshots by Time Offset ({len(snapshot_set)} group(s)) ---")
                for i, s in enumerate(snapshot_set):
                    pic_set = s.get('PicInfoSet') or []
                    print(f"    [{i+1}] TemplateID={s.get('Definition', 'N/A')}  Snapshot Count={len(pic_set)}")
                    for p in pic_set[:5]:
                        wm = p.get('WaterMarkDefinition') or []
                        wm_str = f"  WatermarkTemplate={wm}" if wm else ""
                        print(f"        Time={p.get('TimeOffset', 'N/A')}ms  URL: {p.get('Url', 'N/A')}{wm_str}")
                    if len(pic_set) > 5:
                        print(f"        ... {len(pic_set)-5} more snapshot(s)")

            # ===== Sample Snapshot Info =====
            sample_info = media.get('SampleSnapshotInfo') or {}
            sample_set = sample_info.get('SampleSnapshotSet') or []
            if sample_set:
                print(f"\n  --- Sample Snapshots ({len(sample_set)} group(s)) ---")
                for i, s in enumerate(sample_set):
                    pic_set = s.get('ImageUrlSet') or []
                    sample_type = s.get('SampleType', 'N/A')
                    interval = s.get('Interval', 'N/A')
                    wm = s.get('WaterMarkDefinition') or []
                    wm_str = f"  WatermarkTemplate={wm}" if wm else ""
                    print(f"    [{i+1}] TemplateID={s.get('Definition', 'N/A')}  SampleType={sample_type}  Interval={interval}  Snapshot Count={len(pic_set)}{wm_str}")
                    for url in pic_set[:3]:
                        print(f"        URL: {url}")
                    if len(pic_set) > 3:
                        print(f"        ... {len(pic_set)-3} more snapshot(s)")

            # ===== Image Sprite Info =====
            sprite_info = media.get('ImageSpriteInfo') or {}
            sprite_set = sprite_info.get('ImageSpriteSet') or []
            if sprite_set:
                print(f"\n  --- Image Sprites ({len(sprite_set)} group(s)) ---")
                for i, s in enumerate(sprite_set):
                    img_urls = s.get('ImageUrlSet') or []
                    print(f"    [{i+1}] TemplateID={s.get('Definition', 'N/A')}  Thumbnail={s.get('Width', '?')}x{s.get('Height', '?')}  Total={s.get('TotalCount', 'N/A')}  Sprite Count={len(img_urls)}")
                    for url in img_urls[:2]:
                        print(f"        Sprite URL: {url}")
                    vtt = s.get('WebVttUrl', '')
                    if vtt:
                        print(f"        WebVTT: {vtt}")

            # ===== Adaptive Dynamic Streaming Info =====
            adaptive_info = media.get('AdaptiveDynamicStreamingInfo') or {}
            adaptive_set = adaptive_info.get('AdaptiveDynamicStreamingSet') or []
            if adaptive_set:
                print(f"\n  --- Adaptive Dynamic Streaming ({len(adaptive_set)}) ---")
                for i, a in enumerate(adaptive_set):
                    drm = a.get('DrmType', '')
                    drm_str = f"  Encryption={drm}" if drm else ""
                    size = a.get('Size', 0)
                    size_str = f"  Size={_format_size(size)}" if size else ""
                    dwm = a.get('DigitalWatermarkType', '')
                    dwm_str = f"  DigitalWatermark={dwm}" if dwm and dwm != 'None' else ""
                    crw = a.get('CopyRightWatermarkText', '')
                    crw_str = f"  Copyright={crw}" if crw and crw != 'NONE' and crw != 'None' else ""
                    bwm = a.get('BlindWatermarkDefinition')
                    bwm_str = f"  BlindWatermarkTemplate={bwm}" if bwm else ""
                    default_sub = a.get('DefaultSubtitleId', '')
                    print(f"    [{i+1}] TemplateID={a.get('Definition', 'N/A')}  Package={a.get('Package', 'N/A')}{drm_str}{size_str}{dwm_str}{crw_str}{bwm_str}")
                    print(f"        URL: {a.get('Url', 'N/A')}")

                    # Sub-stream information
                    sub_streams = a.get('SubStreamSet') or []
                    for ss in sub_streams:
                        ss_type = ss.get('Type', 'N/A')
                        ss_w = ss.get('Width', '?')
                        ss_h = ss.get('Height', '?')
                        ss_size = _format_size(ss.get('Size', 0))
                        print(f"        SubStream: {ss_type}  {ss_w}x{ss_h}  Size={ss_size}")

                    # Subtitle information
                    subtitles = a.get('SubtitleSet') or []
                    for sub in subtitles:
                        print(f"        Subtitle: [{sub.get('Id', '')}] {sub.get('Name', '')} ({sub.get('Language', '')}) Format={sub.get('Format', '')} Source={sub.get('Source', '')}")
                        print(f"              URL: {sub.get('Url', 'N/A')}")
                    if default_sub:
                        print(f"        Default Subtitle: {default_sub}")

            # ===== Key Frame Desc Info =====
            kf_info = media.get('KeyFrameDescInfo') or {}
            kf_set = kf_info.get('KeyFrameDescSet') or []
            if kf_set:
                print(f"\n  --- Key Frame Markers ({len(kf_set)}) ---")
                for i, kf in enumerate(kf_set):
                    print(f"    [{i+1}] Time={kf.get('TimeOffset', 'N/A')}s  Content: {kf.get('Content', 'N/A')}")

            # ===== Subtitle Info =====
            subtitle_info = media.get('SubtitleInfo') or {}
            subtitle_set = subtitle_info.get('SubtitleSet') or []
            if subtitle_set:
                print(f"\n  --- Subtitle Info ({len(subtitle_set)}) ---")
                for i, sub in enumerate(subtitle_set):
                    print(f"    [{i+1}] ID={sub.get('Id', 'N/A')}  Name={sub.get('Name', 'N/A')}  Language={sub.get('Language', 'N/A')}  Format={sub.get('Format', 'N/A')}  Source={sub.get('Source', 'N/A')}")
                    print(f"        URL: {sub.get('Url', 'N/A')}")

            # ===== Mini Program Review Info =====
            mp_info = media.get('MiniProgramReviewInfo') or {}
            mp_list = mp_info.get('MiniProgramReviewList') or []
            if mp_list:
                print(f"\n  --- Mini Program Review ({len(mp_list)}) ---")
                for i, mp in enumerate(mp_list):
                    print(f"    [{i+1}] TemplateID={mp.get('Definition', 'N/A')}  Result={mp.get('ReviewResult', 'N/A')}")
                    print(f"        URL: {mp.get('Url', 'N/A')}")
                    # Meta Data sub-fields
                    mp_meta = mp.get('MetaData') or {}
                    if mp_meta:
                        size = mp_meta.get('Size')
                        w = mp_meta.get('Width')
                        h = mp_meta.get('Height')
                        br = mp_meta.get('Bitrate')
                        dur = mp_meta.get('Duration')
                        vid_dur = mp_meta.get('VideoDuration')
                        aud_dur = mp_meta.get('AudioDuration')
                        rotate = mp_meta.get('Rotate')
                        md5 = mp_meta.get('Md5', '')
                        parts = []
                        if mp_meta.get('Container'):
                            parts.append(f"Container={mp_meta['Container']}")
                        if w and h:
                            parts.append(f"{w}x{h}")
                        if br:
                            parts.append(f"Bitrate={_format_bitrate(br)}")
                        if dur is not None:
                            parts.append(f"Duration={_format_duration(dur)}")
                        if size:
                            parts.append(f"Size={_format_size(size)}")
                        if parts:
                            print(f"        Metadata: {' | '.join(parts)}")
                        if vid_dur is not None:
                            print(f"        Video Duration={_format_duration(vid_dur)}  Audio Duration={_format_duration(aud_dur)}")
                        if rotate:
                            print(f"        Rotation={rotate}°")
                        if md5:
                            print(f"        MD5={md5}")
                        _print_video_streams(mp_meta.get('VideoStreamSet') or [], indent="        ")
                        _print_audio_streams(mp_meta.get('AudioStreamSet') or [], indent="        ")
                    summaries = mp.get('ReviewSummary') or []
                    for s in summaries:
                        print(f"        Review: {s.get('Type', 'N/A')}  Suggestion={s.get('Suggestion', 'N/A')}  Confidence={s.get('Confidence', 'N/A')}")

            # ===== Review Info =====
            review_info = media.get('ReviewInfo') or {}
            if review_info:
                media_review = review_info.get('MediaReviewInfo') or {}
                cover_review = review_info.get('CoverReviewInfo') or {}
                if media_review or cover_review:
                    print(f"\n  --- Review Info ---")
                if media_review:
                    print(f"    Media Review: TemplateID={media_review.get('Definition', 'N/A')}  Suggestion={media_review.get('Suggestion', 'N/A')}  Time={media_review.get('ReviewTime', 'N/A')}")
                    types = media_review.get('TypeSet') or []
                    if types:
                        print(f"      Violation Types: {', '.join(types)}")
                if cover_review:
                    print(f"    Cover Review: TemplateID={cover_review.get('Definition', 'N/A')}  Suggestion={cover_review.get('Suggestion', 'N/A')}  Time={cover_review.get('ReviewTime', 'N/A')}")
                    types = cover_review.get('TypeSet') or []
                    if types:
                        print(f"      Violation Types: {', '.join(types)}")

            # ===== MPSAi Media Info =====
            mps_ai_info = media.get('MPSAiMediaInfo') or {}
            ai_list = mps_ai_info.get('AiMediaList') or []
            if ai_list:
                print(f"\n  --- MPS AI Media Info ({len(ai_list)} task type(s)) ---")
                for i, ai_item in enumerate(ai_list):
                    task_type = ai_item.get('TaskType', 'N/A')
                    tasks = ai_item.get('AiMediaTasks') or []
                    print(f"    [{i+1}] Task Type: {task_type}  Result Count={len(tasks)}")
                    for j, task in enumerate(tasks):
                        definition = task.get('Definition', 'N/A')
                        output_files = task.get('OutputFile') or []
                        output_text = task.get('OutputText', '')
                        print(f"      [{j+1}] TemplateID={definition}")
                        for of in output_files:
                            print(f"          FileType={of.get('FileType', 'N/A')}  URL: {of.get('Url', 'N/A')}")
                        if output_text:
                            # Truncate to first 200 characters to avoid overly long output
                            display_text = output_text[:200] + ('...' if len(output_text) > 200 else '')
                            print(f"          Output: {display_text}")

            # ===== Image Understanding Info =====
            img_understand = media.get('ImageUnderstandingInfo') or {}
            img_set = img_understand.get('ImageUnderstandingSet') or []
            if img_set:
                print(f"\n  --- Image Understanding Info ({len(img_set)}) ---")
                for i, item in enumerate(img_set):
                    definition = item.get('Definition', 'N/A')
                    output_files = item.get('OutputFile') or []
                    print(f"    [{i+1}] TemplateID={definition}")
                    for of in output_files:
                        print(f"        FileType={of.get('FileType', 'N/A')}  URL: {of.get('Url', 'N/A')}")

        # ===== Not Exist FileId Set =====
        not_exist = result.get('NotExistFileIdSet') or []
        if not_exist:
            print(f"\n⚠️  The following FileId(s) do not exist ({len(not_exist)}): {', '.join(not_exist)}")

        if args.json:
            print("\n" + json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"Query failed: {e}")
        sys.exit(1)



def main():
    check_sdk_version()
    parser = argparse.ArgumentParser(
        description='VOD media information query tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Query a single media
  python vod_describe_media.py --file-id 5285485487985271487

  # Query multiple media
  python vod_describe_media.py --file-id 5285485487985271487 5285485487985271488

  # Query basic info only
  python vod_describe_media.py --file-id 5285485487985271487 --filters basicInfo

  # Query transcode + subtitle info
  python vod_describe_media.py --file-id 5285485487985271487 --filters transcodeInfo subtitleInfo

  # Query review info
  python vod_describe_media.py --file-id 5285485487985271487 --filters reviewInfo
        '''
    )

    parser.add_argument('--file-id', nargs='+', required=True, help='Media FileId list')
    parser.add_argument('--filters', nargs='+',
                        help='Info type filters: basicInfo, metaData, transcodeInfo, animatedGraphicsInfo, '
                             'imageSpriteInfo, snapshotByTimeOffsetInfo, sampleSnapshotInfo, '
                             'keyFrameDescInfo, adaptiveDynamicStreamingInfo, miniProgramReviewInfo, '
                             'subtitleInfo, reviewInfo, mpsAiMediaInfo, imageUnderstandingInfo')
    parser.add_argument('--sub-app-id', type=int,
                        default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                        help='Sub-application ID (can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)')
    parser.add_argument('--region', default='ap-guangzhou', help='Region')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--dry-run', action='store_true', help='Preview request parameters')

    args = parser.parse_args()
    describe_media(args)


if __name__ == '__main__':
    main()
