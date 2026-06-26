#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD 媒体信息查询脚本
"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vod_auto_upgrade import check_sdk_version


# 软依赖：vod_load_env 用于在凭证缺失时从 ~/.env 等 dotenv 文件兜底加载
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
    print("错误：请先安装腾讯云 SDK: pip install tencentcloud-sdk-python")
    sys.exit(1)


def get_credential():
    """获取腾讯云认证信息。若环境变量缺失则尝试从 dotenv 文件自动加载。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        # 兜底：尝试从 ~/.env 等 dotenv 文件加载
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] 环境变量未设置，尝试从 dotenv 文件自动加载...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from vod_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print("错误：请设置环境变量 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
            sys.exit(1)

    return credential.Credential(secret_id, secret_key)


def get_client(region="ap-guangzhou"):
    """获取 VOD 客户端"""
    cred = get_credential()
    http_profile = HttpProfile()
    http_profile.endpoint = "vod.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return vod_client.VodClient(cred, region, client_profile)


def _format_size(size_bytes):
    """格式化文件大小"""
    if not size_bytes:
        return 'N/A'
    for unit in ['B', 'KB', 'MB', 'GB']:
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


def _format_bitrate(bps):
    """格式化码率"""
    if not bps:
        return 'N/A'
    if bps >= 1000000:
        return f"{bps/1000000:.2f} Mbps"
    elif bps >= 1000:
        return f"{bps/1000:.0f} kbps"
    return f"{bps} bps"


def _format_duration(seconds):
    """格式化时长"""
    if seconds is None:
        return 'N/A'
    seconds = float(seconds)
    if seconds < 60:
        return f"{seconds:.3f} 秒"
    elif seconds < 3600:
        m = int(seconds // 60)
        s = seconds % 60
        return f"{m}分{s:.1f}秒"
    else:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        return f"{h}时{m}分{s:.0f}秒"


def _print_video_streams(streams, indent="    "):
    """输出视频流信息"""
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
        print(f"{indent}视频流[{j}]: {codec}{tag_str}  {w}x{h}  {fps}fps  {br}{dr_str}")


def _print_audio_streams(streams, indent="    "):
    """输出音频流信息"""
    if not streams:
        return
    for j, aus in enumerate(streams):
        codec = aus.get('Codec', 'N/A')
        sr = aus.get('SamplingRate', 'N/A')
        br = _format_bitrate(aus.get('Bitrate'))
        print(f"{indent}音频流[{j}]: {codec}  采样率={sr}Hz  {br}")


def _print_source_info(source_info, indent="  "):
    """输出来源信息"""
    if not source_info:
        return
    print(f"{indent}来源类型: {source_info.get('SourceType', 'N/A')}")
    ctx = source_info.get('SourceContext', '')
    if ctx:
        print(f"{indent}来源上下文: {ctx}")

    live_info = source_info.get('LiveRecordInfo') or {}
    if live_info:
        print(f"{indent}直播录制信息:")
        print(f"{indent}  域名: {live_info.get('Domain', 'N/A')}")
        print(f"{indent}  Path: {live_info.get('Path', 'N/A')}")
        print(f"{indent}  流ID: {live_info.get('StreamId', 'N/A')}")
        print(f"{indent}  录制起始: {live_info.get('RecordStartTime', 'N/A')}")
        print(f"{indent}  录制结束: {live_info.get('RecordEndTime', 'N/A')}")

    trtc_info = source_info.get('TrtcRecordInfo') or {}
    if trtc_info:
        print(f"{indent}TRTC录制信息:")
        print(f"{indent}  SdkAppId: {trtc_info.get('SdkAppId', 'N/A')}")
        print(f"{indent}  RoomId: {trtc_info.get('RoomId', 'N/A')}")
        print(f"{indent}  TaskId: {trtc_info.get('TaskId', 'N/A')}")
        user_ids = trtc_info.get('UserIds') or []
        if user_ids:
            print(f"{indent}  用户: {', '.join(user_ids)}")

    web_info = source_info.get('WebPageRecordInfo') or {}
    if web_info:
        print(f"{indent}全景录制信息:")
        print(f"{indent}  录制URL: {web_info.get('RecordUrl', 'N/A')}")
        print(f"{indent}  TaskId: {web_info.get('RecordTaskId', 'N/A')}")


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def describe_media(args):
    """查询媒体信息"""
    client = get_client(args.region)

    req = models.DescribeMediaInfosRequest()
    req.FileIds = args.file_id

    if args.filters:
        req.Filters = args.filters
    if args.sub_app_id:
        req.SubAppId = args.sub_app_id

    if args.dry_run:
        print("[DRY RUN] 请求参数:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return

    try:
        resp = client.DescribeMediaInfos(req)
        result = json.loads(resp.to_json_string())

        media_infos = result.get('MediaInfoSet', [])
        not_exist = result.get('NotExistFileIdSet', [])

        print(f"查询完成!")
        print(f"找到媒体: {len(media_infos)} 个")
        if not_exist:
            print(f"不存在的 FileId: {not_exist}")

        for idx, media in enumerate(media_infos):
            # FileId 从顶层获取
            file_id = media.get('FileId') or (args.file_id[idx] if idx < len(args.file_id) else 'N/A')

            # ===== BasicInfo =====
            basic_info = media.get('BasicInfo') or {}
            if basic_info:
                print(f"\n  FileId: {file_id}")
                print(f"  名称: {basic_info.get('Name', 'N/A')}")
                desc = basic_info.get('Description', '')
                if desc:
                    print(f"  描述: {desc}")
                print(f"  类型: {basic_info.get('Type', 'N/A')}")
                print(f"  文件类别: {basic_info.get('Category', 'N/A')}")
                print(f"  状态: {basic_info.get('Status', 'N/A')}")
                print(f"  创建时间: {basic_info.get('CreateTime', 'N/A')}")
                print(f"  更新时间: {basic_info.get('UpdateTime', 'N/A')}")
                expire = basic_info.get('ExpireTime', '')
                if expire and expire != '9999-12-31T23:59:59Z':
                    print(f"  过期时间: {expire}")
                else:
                    print(f"  过期时间: 永不过期")

                class_name = basic_info.get('ClassName', '')
                class_path = basic_info.get('ClassPath', '')
                class_id = basic_info.get('ClassId')
                if class_name or class_path:
                    cls_str = class_path or class_name
                    if class_id is not None:
                        cls_str += f" (ID: {class_id})"
                    print(f"  分类: {cls_str}")

                cover = basic_info.get('CoverUrl', '')
                if cover:
                    print(f"  封面URL: {cover}")
                media_url = basic_info.get('MediaUrl', '')
                if media_url:
                    print(f"  媒体URL: {media_url}")

                tags = basic_info.get('TagSet') or []
                if tags:
                    print(f"  标签: {', '.join(tags)}")

                print(f"  存储地域: {basic_info.get('StorageRegion', 'N/A')}")
                storage_path = basic_info.get('StoragePath', '')
                if storage_path:
                    print(f"  存储路径: {storage_path}")
                print(f"  存储类型: {basic_info.get('StorageClass', 'N/A')}")

                vid = basic_info.get('Vid', '')
                if vid:
                    print(f"  Vid: {vid}")

                # 来源信息
                _print_source_info(basic_info.get('SourceInfo'), indent="  ")
            else:
                # 没有 BasicInfo 时至少输出 FileId
                print(f"\n  FileId: {file_id}")

            # ===== MetaData =====
            meta_data = media.get('MetaData') or {}
            if meta_data:
                print(f"\n  --- 元数据 ---")
                size = meta_data.get('Size')
                if size is not None:
                    print(f"  文件大小: {_format_size(size)}")
                print(f"  容器: {meta_data.get('Container', 'N/A')}")
                print(f"  时长: {_format_duration(meta_data.get('Duration'))}")
                vid_dur = meta_data.get('VideoDuration')
                aud_dur = meta_data.get('AudioDuration')
                if vid_dur is not None:
                    print(f"  视频时长: {_format_duration(vid_dur)}")
                if aud_dur is not None:
                    print(f"  音频时长: {_format_duration(aud_dur)}")
                w = meta_data.get('Width')
                h = meta_data.get('Height')
                if w and h:
                    print(f"  分辨率: {w}x{h}")
                print(f"  码率: {_format_bitrate(meta_data.get('Bitrate'))}")
                rotate = meta_data.get('Rotate')
                if rotate:
                    print(f"  旋转角度: {rotate}°")
                md5 = meta_data.get('Md5', '')
                if md5:
                    print(f"  MD5: {md5}")

                _print_video_streams(meta_data.get('VideoStreamSet') or [], indent="  ")
                _print_audio_streams(meta_data.get('AudioStreamSet') or [], indent="  ")

            # ===== TranscodeInfo =====
            transcode_info = media.get('TranscodeInfo') or {}
            transcode_set = transcode_info.get('TranscodeSet') or []
            if transcode_set:
                print(f"\n  --- 转码结果 ({len(transcode_set)} 个) ---")
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
                    dur_str = f"  时长={_format_duration(duration)}" if duration else ""
                    print(f"    [{i+1}] 模板ID={definition}  容器={container}  {width}x{height}  码率={bitrate_str}  大小={size_str}{dur_str}")  # NOCA:line-too-long(long SDK parameter or URL string)
                    if md5:
                        print(f"        MD5: {md5}")
                    if dwm_type and dwm_type != 'None':
                        print(f"        数字水印: {dwm_type}")
                    if crw_text and crw_text != 'None':
                        print(f"        版权信息: {crw_text}")
                    if bwm_def:
                        print(f"        盲水印模板: {bwm_def}")
                    print(f"        URL: {url}")
                    _print_video_streams(t.get('VideoStreamSet') or [], indent="        ")
                    _print_audio_streams(t.get('AudioStreamSet') or [], indent="        ")

            # ===== AnimatedGraphicsInfo =====
            animated_info = media.get('AnimatedGraphicsInfo') or {}
            animated_set = animated_info.get('AnimatedGraphicsSet') or []
            if animated_set:
                print(f"\n  --- 转动图结果 ({len(animated_set)} 个) ---")
                for i, a in enumerate(animated_set):
                    container = a.get('Container', 'N/A')
                    start_off = a.get('StartTimeOffset')
                    end_off = a.get('EndTimeOffset')
                    time_str = ""
                    if start_off is not None and end_off is not None:
                        time_str = f"  时间={start_off}s→{end_off}s"
                    md5 = a.get('Md5', '')
                    print(f"    [{i+1}] 模板ID={a.get('Definition', 'N/A')}  格式={container}  {a.get('Width', '?')}x{a.get('Height', '?')}  码率={_format_bitrate(a.get('Bitrate'))}  大小={_format_size(a.get('Size', 0))}{time_str}")  # NOCA:line-too-long(long SDK parameter or URL string)
                    if md5:
                        print(f"        MD5: {md5}")
                    print(f"        URL: {a.get('Url', 'N/A')}")

            # ===== SnapshotByTimeOffsetInfo =====
            snapshot_info = media.get('SnapshotByTimeOffsetInfo') or {}
            snapshot_set = snapshot_info.get('SnapshotByTimeOffsetSet') or []
            if snapshot_set:
                print(f"\n  --- 指定时间点截图 ({len(snapshot_set)} 组) ---")
                for i, s in enumerate(snapshot_set):
                    pic_set = s.get('PicInfoSet') or []
                    print(f"    [{i+1}] 模板ID={s.get('Definition', 'N/A')}  截图数={len(pic_set)}")
                    for p in pic_set[:5]:
                        wm = p.get('WaterMarkDefinition') or []
                        wm_str = f"  水印模板={wm}" if wm else ""
                        print(f"        时间={p.get('TimeOffset', 'N/A')}ms  URL: {p.get('Url', 'N/A')}{wm_str}")
                    if len(pic_set) > 5:
                        print(f"        ... 还有 {len(pic_set)-5} 张截图")

            # ===== SampleSnapshotInfo =====
            sample_info = media.get('SampleSnapshotInfo') or {}
            sample_set = sample_info.get('SampleSnapshotSet') or []
            if sample_set:
                print(f"\n  --- 采样截图 ({len(sample_set)} 组) ---")
                for i, s in enumerate(sample_set):
                    pic_set = s.get('ImageUrlSet') or []
                    sample_type = s.get('SampleType', 'N/A')
                    interval = s.get('Interval', 'N/A')
                    wm = s.get('WaterMarkDefinition') or []
                    wm_str = f"  水印模板={wm}" if wm else ""
                    print(f"    [{i+1}] 模板ID={s.get('Definition', 'N/A')}  采样方式={sample_type}  间隔={interval}  截图数={len(pic_set)}{wm_str}")  # NOCA:line-too-long(long SDK parameter or URL string)
                    for url in pic_set[:3]:
                        print(f"        URL: {url}")
                    if len(pic_set) > 3:
                        print(f"        ... 还有 {len(pic_set)-3} 张截图")

            # ===== ImageSpriteInfo =====
            sprite_info = media.get('ImageSpriteInfo') or {}
            sprite_set = sprite_info.get('ImageSpriteSet') or []
            if sprite_set:
                print(f"\n  --- 雪碧图 ({len(sprite_set)} 组) ---")
                for i, s in enumerate(sprite_set):
                    img_urls = s.get('ImageUrlSet') or []
                    print(f"    [{i+1}] 模板ID={s.get('Definition', 'N/A')}  小图={s.get('Width', '?')}x{s.get('Height', '?')}  总数={s.get('TotalCount', 'N/A')}  大图数={len(img_urls)}")  # NOCA:line-too-long(long SDK parameter or URL string)
                    for url in img_urls[:2]:
                        print(f"        大图URL: {url}")
                    vtt = s.get('WebVttUrl', '')
                    if vtt:
                        print(f"        WebVTT: {vtt}")

            # ===== AdaptiveDynamicStreamingInfo =====
            adaptive_info = media.get('AdaptiveDynamicStreamingInfo') or {}
            adaptive_set = adaptive_info.get('AdaptiveDynamicStreamingSet') or []
            if adaptive_set:
                print(f"\n  --- 自适应码流 ({len(adaptive_set)} 个) ---")
                for i, a in enumerate(adaptive_set):
                    drm = a.get('DrmType', '')
                    drm_str = f"  加密={drm}" if drm else ""
                    size = a.get('Size', 0)
                    size_str = f"  大小={_format_size(size)}" if size else ""
                    dwm = a.get('DigitalWatermarkType', '')
                    dwm_str = f"  数字水印={dwm}" if dwm and dwm != 'None' else ""
                    crw = a.get('CopyRightWatermarkText', '')
                    crw_str = f"  版权={crw}" if crw and crw != 'NONE' and crw != 'None' else ""
                    bwm = a.get('BlindWatermarkDefinition')
                    bwm_str = f"  盲水印模板={bwm}" if bwm else ""
                    default_sub = a.get('DefaultSubtitleId', '')
                    print(f"    [{i+1}] 模板ID={a.get('Definition', 'N/A')}  封装={a.get('Package', 'N/A')}{drm_str}{size_str}{dwm_str}{crw_str}{bwm_str}")  # NOCA:line-too-long(long SDK parameter or URL string)
                    print(f"        URL: {a.get('Url', 'N/A')}")

                    # 子流信息
                    sub_streams = a.get('SubStreamSet') or []
                    for ss in sub_streams:
                        ss_type = ss.get('Type', 'N/A')
                        ss_w = ss.get('Width', '?')
                        ss_h = ss.get('Height', '?')
                        ss_size = _format_size(ss.get('Size', 0))
                        print(f"        子流: {ss_type}  {ss_w}x{ss_h}  大小={ss_size}")

                    # 字幕信息
                    subtitles = a.get('SubtitleSet') or []
                    for sub in subtitles:
                        print(f"        字幕: [{sub.get('Id', '')}] {sub.get('Name', '')} ({sub.get('Language', '')}) 格式={sub.get('Format', '')} 来源={sub.get('Source', '')}")  # NOCA:line-too-long(long SDK parameter or URL string)
                        print(f"              URL: {sub.get('Url', 'N/A')}")
                    if default_sub:
                        print(f"        默认字幕: {default_sub}")

            # ===== KeyFrameDescInfo =====
            kf_info = media.get('KeyFrameDescInfo') or {}
            kf_set = kf_info.get('KeyFrameDescSet') or []
            if kf_set:
                print(f"\n  --- 打点信息 ({len(kf_set)} 个) ---")
                for i, kf in enumerate(kf_set):
                    print(f"    [{i+1}] 时间={kf.get('TimeOffset', 'N/A')}s  内容: {kf.get('Content', 'N/A')}")

            # ===== SubtitleInfo =====
            subtitle_info = media.get('SubtitleInfo') or {}
            subtitle_set = subtitle_info.get('SubtitleSet') or []
            if subtitle_set:
                print(f"\n  --- 字幕信息 ({len(subtitle_set)} 个) ---")
                for i, sub in enumerate(subtitle_set):
                    print(f"    [{i+1}] ID={sub.get('Id', 'N/A')}  名称={sub.get('Name', 'N/A')}  语言={sub.get('Language', 'N/A')}  格式={sub.get('Format', 'N/A')}  来源={sub.get('Source', 'N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
                    print(f"        URL: {sub.get('Url', 'N/A')}")

            # ===== MiniProgramReviewInfo =====
            mp_info = media.get('MiniProgramReviewInfo') or {}
            mp_list = mp_info.get('MiniProgramReviewList') or []
            if mp_list:
                print(f"\n  --- 小程序审核 ({len(mp_list)} 个) ---")
                for i, mp in enumerate(mp_list):
                    print(f"    [{i+1}] 模板ID={mp.get('Definition', 'N/A')}  结果={mp.get('ReviewResult', 'N/A')}")
                    print(f"        URL: {mp.get('Url', 'N/A')}")
                    # MetaData 子字段
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
                            parts.append(f"容器={mp_meta['Container']}")
                        if w and h:
                            parts.append(f"{w}x{h}")
                        if br:
                            parts.append(f"码率={_format_bitrate(br)}")
                        if dur is not None:
                            parts.append(f"时长={_format_duration(dur)}")
                        if size:
                            parts.append(f"大小={_format_size(size)}")
                        if parts:
                            print(f"        元数据: {' | '.join(parts)}")
                        if vid_dur is not None:
                            print(f"        视频时长={_format_duration(vid_dur)}  音频时长={_format_duration(aud_dur)}")
                        if rotate:
                            print(f"        旋转={rotate}°")
                        if md5:
                            print(f"        MD5={md5}")
                        _print_video_streams(mp_meta.get('VideoStreamSet') or [], indent="        ")
                        _print_audio_streams(mp_meta.get('AudioStreamSet') or [], indent="        ")
                    summaries = mp.get('ReviewSummary') or []
                    for s in summaries:
                        print(f"        审核: {s.get('Type', 'N/A')}  建议={s.get('Suggestion', 'N/A')}  置信度={s.get('Confidence', 'N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)

            # ===== ReviewInfo =====
            review_info = media.get('ReviewInfo') or {}
            if review_info:
                media_review = review_info.get('MediaReviewInfo') or {}
                cover_review = review_info.get('CoverReviewInfo') or {}
                if media_review or cover_review:
                    print(f"\n  --- 审核信息 ---")
                if media_review:
                    print(f"    媒体审核: 模板ID={media_review.get('Definition', 'N/A')}  建议={media_review.get('Suggestion', 'N/A')}  时间={media_review.get('ReviewTime', 'N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
                    types = media_review.get('TypeSet') or []
                    if types:
                        print(f"      违规类型: {', '.join(types)}")
                if cover_review:
                    print(f"    封面审核: 模板ID={cover_review.get('Definition', 'N/A')}  建议={cover_review.get('Suggestion', 'N/A')}  时间={cover_review.get('ReviewTime', 'N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
                    types = cover_review.get('TypeSet') or []
                    if types:
                        print(f"      违规类型: {', '.join(types)}")

            # ===== MPSAiMediaInfo =====
            mps_ai_info = media.get('MPSAiMediaInfo') or {}
            ai_list = mps_ai_info.get('AiMediaList') or []
            if ai_list:
                print(f"\n  --- MPS智能媒资信息 ({len(ai_list)} 个任务类型) ---")
                for i, ai_item in enumerate(ai_list):
                    task_type = ai_item.get('TaskType', 'N/A')
                    tasks = ai_item.get('AiMediaTasks') or []
                    print(f"    [{i+1}] 任务类型: {task_type}  结果数={len(tasks)}")
                    for j, task in enumerate(tasks):
                        definition = task.get('Definition', 'N/A')
                        output_files = task.get('OutputFile') or []
                        output_text = task.get('OutputText', '')
                        print(f"      [{j+1}] 模板ID={definition}")
                        for of in output_files:
                            print(f"          文件类型={of.get('FileType', 'N/A')}  URL: {of.get('Url', 'N/A')}")
                        if output_text:
                            # 截取前200字符避免过长
                            display_text = output_text[:200] + ('...' if len(output_text) > 200 else '')
                            print(f"          输出结果: {display_text}")

            # ===== ImageUnderstandingInfo =====
            img_understand = media.get('ImageUnderstandingInfo') or {}
            img_set = img_understand.get('ImageUnderstandingSet') or []
            if img_set:
                print(f"\n  --- 图片理解信息 ({len(img_set)} 个) ---")
                for i, item in enumerate(img_set):
                    definition = item.get('Definition', 'N/A')
                    output_files = item.get('OutputFile') or []
                    print(f"    [{i+1}] 模板ID={definition}")
                    for of in output_files:
                        print(f"        文件类型={of.get('FileType', 'N/A')}  URL: {of.get('Url', 'N/A')}")

        # ===== NotExistFileIdSet =====
        not_exist = result.get('NotExistFileIdSet') or []
        if not_exist:
            print(f"\n⚠️  以下 FileId 不存在 ({len(not_exist)} 个): {', '.join(not_exist)}")

        if args.json:
            print("\n" + json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        print(f"查询失败: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='VOD 媒体信息查询工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 查询单个媒体
  python vod_describe_media.py --file-id 5285485487985271487

  # 查询多个媒体
  python vod_describe_media.py --file-id 5285485487985271487 5285485487985271488

  # 只查询基础信息
  python vod_describe_media.py --file-id 5285485487985271487 --filters basicInfo

  # 查询转码+字幕信息
  python vod_describe_media.py --file-id 5285485487985271487 --filters transcodeInfo subtitleInfo

  # 查询审核信息
  python vod_describe_media.py --file-id 5285485487985271487 --filters reviewInfo
        '''
    )

    parser.add_argument('--file-id', nargs='+', required=True, help='媒体 FileId 列表')
    parser.add_argument('--filters', nargs='+',
                        help='信息类型过滤器: basicInfo, metaData, transcodeInfo, animatedGraphicsInfo, '
                             'imageSpriteInfo, snapshotByTimeOffsetInfo, sampleSnapshotInfo, '
                             'keyFrameDescInfo, adaptiveDynamicStreamingInfo, miniProgramReviewInfo, '
                             'subtitleInfo, reviewInfo, mpsAiMediaInfo, imageUnderstandingInfo')
    parser.add_argument('--sub-app-id', type=int,
                        default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                        help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    parser.add_argument('--region', default='ap-guangzhou', help='地域')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    args = parser.parse_args()
    describe_media(args)


if __name__ == '__main__':
    main()
