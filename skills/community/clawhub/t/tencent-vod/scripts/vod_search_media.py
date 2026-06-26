#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD 搜索媒体脚本
使用 SearchMedia API 搜索媒体信息，支持多种条件筛选。

场景说明：
  - SearchMedia：支持按名称模糊搜索、分类、标签、文件类型等条件筛选
  - DescribeMediaInfos：按 FileId 精确查询（已有独立脚本 vod_describe_media.py）

本脚本统一处理搜索场景，当只有 FileId 时也可使用（通过 SearchMedia 的 FileIds 参数）。

接口冲突决策：
  - 用户提供 FileId → 本脚本使用 SearchMedia.FileIds 参数搜索（也可使用 vod_describe_media.py 精确查询）
  - 用户提供名称/描述/标签等 → 本脚本使用 SearchMedia 模糊搜索
  - 用户通过应用名称指定应用 → 先调用 DescribeSubAppIds 匹配应用，再搜索

API 文档：https://cloud.tencent.com/document/api/266/31813
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


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def resolve_sub_app_id(client, app_name):
    """通过应用名称/描述/标签模糊匹配子应用 ID。

    查询所有子应用列表，然后按 名称、描述、标签值 进行模糊匹配。
    - 精确匹配名称优先
    - 其次模糊匹配名称、描述、标签
    - 匹配到唯一结果直接返回
    - 匹配到多个结果列出供选择并退出
    - 无匹配则报错退出
    """
    print(f"正在查询子应用列表，匹配关键词: '{app_name}' ...")

    # 分页拉取所有子应用
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
            print(f"查询子应用列表失败: {e}")
            sys.exit(1)

        items = result.get("SubAppIdInfoSet", [])
        all_apps.extend(items)
        total = result.get("TotalCount", 0)
        if len(all_apps) >= total or not items:
            break
        offset += limit

    if not all_apps:
        print("错误：当前账号下没有任何子应用")
        sys.exit(1)

    keyword = app_name.lower()

    # 1) 精确匹配名称
    exact = [a for a in all_apps
             if (a.get("SubAppIdName") or a.get("Name") or "").lower() == keyword]
    if len(exact) == 1:
        matched = exact[0]
        sub_id = matched.get("SubAppId")
        name = matched.get("SubAppIdName") or matched.get("Name") or "N/A"
        print(f"✅ 精确匹配到应用: {name} (SubAppId: {sub_id})")
        return sub_id

    # 2) 模糊匹配（名称、描述、标签值）
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
        print(f"错误：未找到与 '{app_name}' 匹配的子应用。")
        print("当前可用的子应用列表：")
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
        print(f"✅ 匹配到应用: {name} (SubAppId: {sub_id}){' — ' + desc if desc else ''}")
        return sub_id

    # 多个匹配
    print(f"找到 {len(fuzzy)} 个匹配的子应用，请通过 --sub-app-id 指定具体的应用 ID：")
    for a in fuzzy:
        n = a.get("SubAppIdName") or a.get("Name") or "N/A"
        sid = a.get("SubAppId", "N/A")
        d = a.get("Description") or ""
        print(f"  - {n} (SubAppId: {sid}){' — ' + d if d else ''}")
    sys.exit(1)


def format_duration(seconds):
    """格式化时长为可读字符串"""
    if seconds is None:
        return "N/A"
    seconds = float(seconds)
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        m = int(seconds // 60)
        s = seconds % 60
        return f"{m}分{s:.0f}秒"
    else:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        return f"{h}时{m}分"


def format_size(size_bytes):
    """格式化文件大小为可读字符串"""
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
    """格式化码率"""
    if not bps:
        return 'N/A'
    if bps >= 1000000:
        return f"{bps/1000000:.2f} Mbps"
    elif bps >= 1000:
        return f"{bps/1000:.0f} kbps"
    return f"{bps} bps"


def print_video_streams(streams, indent="    "):
    """输出视频流信息"""
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
        print(f"{indent}视频流[{j}]: {codec}{tag_str}  {w}x{h}  {fps}fps  {br}{dr_str}")


def print_audio_streams(streams, indent="    "):
    """输出音频流信息"""
    if not streams:
        return
    for j, aus in enumerate(streams):
        codec = aus.get('Codec', 'N/A')
        sr = aus.get('SamplingRate', 'N/A')
        br = format_bitrate(aus.get('Bitrate'))
        print(f"{indent}音频流[{j}]: {codec}  采样率={sr}Hz  {br}")


def print_source_info(source_info, indent="  "):
    """输出来源信息"""
    if not source_info:
        return
    print(f"{indent}来源类型: {source_info.get('SourceType', 'N/A')}")
    ctx = source_info.get('SourceContext', '')
    if ctx:
        print(f"{indent}来源上下文: {ctx}")
    live_info = source_info.get('LiveRecordInfo') or {}
    if live_info:
        print(f"{indent}直播录制: 域名={live_info.get('Domain','N/A')}  Path={live_info.get('Path','N/A')}  流ID={live_info.get('StreamId','N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
        print(f"{indent}  录制时间: {live_info.get('RecordStartTime','N/A')} → {live_info.get('RecordEndTime','N/A')}")
    trtc_info = source_info.get('TrtcRecordInfo') or {}
    if trtc_info:
        print(f"{indent}TRTC录制: SdkAppId={trtc_info.get('SdkAppId','N/A')}  RoomId={trtc_info.get('RoomId','N/A')}  TaskId={trtc_info.get('TaskId','N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
        user_ids = trtc_info.get('UserIds') or []
        if user_ids:
            print(f"{indent}  用户: {', '.join(user_ids)}")
    web_info = source_info.get('WebPageRecordInfo') or {}
    if web_info:
        print(f"{indent}全景录制: URL={web_info.get('RecordUrl','N/A')}  TaskId={web_info.get('RecordTaskId','N/A')}")


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def print_media_info(media, index=None, verbose=False):
    """格式化输出单个媒体信息"""
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
    print(f"  类型:     {category} ({media_type})")
    print(f"  状态:     {status}")
    print(f"  创建时间: {create_time}")
    if update_time:
        print(f"  更新时间: {update_time}")
    if expire_time and expire_time != "9999-12-31T23:59:59Z":
        print(f"  过期时间: {expire_time}")

    if duration is not None:
        print(f"  时长:     {format_duration(duration)}")
    if vid_dur is not None and verbose:
        print(f"  视频时长: {format_duration(vid_dur)}  音频时长: {format_duration(aud_dur)}")
    if size is not None:
        print(f"  大小:     {format_size(size)}")
    if width and height:
        print(f"  分辨率:   {width}x{height}")
    if bitrate:
        print(f"  码率:     {format_bitrate(bitrate)}")
    if rotate and verbose:
        print(f"  旋转:     {rotate}°")
    if md5 and verbose:
        print(f"  MD5:      {md5}")

    if description:
        print(f"  描述:     {description}")
    if class_name or class_path:
        cls_str = class_path or class_name
        if class_id is not None:
            cls_str += f" (ID: {class_id})"
        print(f"  分类:     {cls_str}")
    if tags:
        print(f"  标签:     {', '.join(tags)}")
    if storage_region:
        print(f"  存储地域: {storage_region}")
    if storage_path and verbose:
        print(f"  存储路径: {storage_path}")
    if storage_class:
        print(f"  存储类型: {storage_class}")
    if vid and verbose:
        print(f"  Vid:      {vid}")

    if verbose:
        if media_url:
            print(f"  媒体URL:  {media_url}")
        if cover_url:
            print(f"  封面URL:  {cover_url}")
        # 来源信息
        source_info = basic.get("SourceInfo")
        if source_info:
            print_source_info(source_info, indent="  ")
        # 视频流/音频流
        print_video_streams(meta.get("VideoStreamSet") or [], indent="  ")
        print_audio_streams(meta.get("AudioStreamSet") or [], indent="  ")
        # TranscodeInfo
        transcode_set = (media.get('TranscodeInfo') or {}).get('TranscodeSet') or []
        if transcode_set:
            print(f"  转码结果: {len(transcode_set)} 个")
            for t in transcode_set[:3]:
                print(f"    模板ID={t.get('Definition','N/A')}  {t.get('Width','?')}x{t.get('Height','?')}  {format_bitrate(t.get('Bitrate'))}  {t.get('Container','N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
                print(f"    URL: {t.get('Url','N/A')}")
            if len(transcode_set) > 3:
                print(f"    ... 还有 {len(transcode_set)-3} 个转码结果")
        # AnimatedGraphicsInfo
        anim_set = (media.get('AnimatedGraphicsInfo') or {}).get('AnimatedGraphicsSet') or []
        if anim_set:
            print(f"  转动图: {len(anim_set)} 个")
            for a in anim_set[:2]:
                print(f"    模板ID={a.get('Definition','N/A')}  {a.get('Container','N/A')}  URL: {a.get('Url','N/A')}")
        # SnapshotByTimeOffsetInfo
        snap_set = (media.get('SnapshotByTimeOffsetInfo') or {}).get('SnapshotByTimeOffsetSet') or []
        if snap_set:
            print(f"  指定时间点截图: {len(snap_set)} 组")
        # SampleSnapshotInfo
        sample_set = (media.get('SampleSnapshotInfo') or {}).get('SampleSnapshotSet') or []
        if sample_set:
            print(f"  采样截图: {len(sample_set)} 组")
        # ImageSpriteInfo
        sprite_set = (media.get('ImageSpriteInfo') or {}).get('ImageSpriteSet') or []
        if sprite_set:
            print(f"  雪碧图: {len(sprite_set)} 组")
        # AdaptiveDynamicStreamingInfo
        adaptive_set = (media.get('AdaptiveDynamicStreamingInfo') or {}).get('AdaptiveDynamicStreamingSet') or []
        if adaptive_set:
            print(f"  自适应码流: {len(adaptive_set)} 个")
            for a in adaptive_set[:2]:
                print(f"    模板ID={a.get('Definition','N/A')}  {a.get('Package','N/A')}  URL: {a.get('Url','N/A')}")
        # KeyFrameDescInfo
        kf_set = (media.get('KeyFrameDescInfo') or {}).get('KeyFrameDescSet') or []
        if kf_set:
            print(f"  打点信息: {len(kf_set)} 个")
        # SubtitleInfo
        sub_set = (media.get('SubtitleInfo') or {}).get('SubtitleSet') or []
        if sub_set:
            print(f"  字幕: {len(sub_set)} 个")
            for s in sub_set:
                print(f"    [{s.get('Id','')}] {s.get('Name','')} ({s.get('Language','')}) {s.get('Format','')} URL: {s.get('Url','N/A')}")  # NOCA:line-too-long(long SDK parameter or URL string)
        # ReviewInfo
        review_info = media.get('ReviewInfo') or {}
        if review_info:
            mr = review_info.get('MediaReviewInfo') or {}
            cr = review_info.get('CoverReviewInfo') or {}
            if mr:
                print(f"  媒体审核: 建议={mr.get('Suggestion','N/A')}  时间={mr.get('ReviewTime','N/A')}")
            if cr:
                print(f"  封面审核: 建议={cr.get('Suggestion','N/A')}  时间={cr.get('ReviewTime','N/A')}")
        # MiniProgramReviewInfo
        mp_list = (media.get('MiniProgramReviewInfo') or {}).get('MiniProgramReviewList') or []
        if mp_list:
            print(f"  小程序审核: {len(mp_list)} 个")
        # MPSAiMediaInfo
        ai_list = (media.get('MPSAiMediaInfo') or {}).get('AiMediaList') or []
        if ai_list:
            print(f"  MPS智能媒资: {len(ai_list)} 个任务类型")
        # ImageUnderstandingInfo
        img_set = (media.get('ImageUnderstandingInfo') or {}).get('ImageUnderstandingSet') or []
        if img_set:
            print(f"  图片理解: {len(img_set)} 个")


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def search_media(args):
    """搜索媒体文件"""

    # 构造请求参数（dry-run 不需要认证）
    payload = {}

    # 处理 SubAppId
    sub_app_id = args.sub_app_id

    # 通过应用名称解析 SubAppId（需要客户端，非 dry-run）
    if args.app_name and not args.dry_run:
        if args.sub_app_id:
            print("错误：--app-name 和 --sub-app-id 不能同时指定")
            sys.exit(1)
        client = get_client(args.region)
        sub_app_id = resolve_sub_app_id(client, args.app_name)

    if sub_app_id:
        payload["SubAppId"] = sub_app_id

    # 搜索条件
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

    # 时间范围
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

    # 排序
    if args.sort_field:
        payload["Sort"] = {
            "Field": args.sort_field,
            "Order": args.sort_order or "Desc"
        }

    # 分页
    if args.offset is not None:
        payload["Offset"] = args.offset
    if args.limit is not None:
        payload["Limit"] = args.limit

    # 返回信息过滤
    if args.filters:
        payload["Filters"] = args.filters

    # dry-run 模式
    if args.dry_run:
        if args.app_name:
            payload["_app_name"] = args.app_name
            payload["_note"] = "app_name 将在实际执行时解析为 SubAppId"
        print("[DRY RUN] 请求参数:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return None

    # 构造请求
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

        # 人类可读输出
        print(f"🔍 搜索完成!")
        print(f"  匹配总数: {total}")
        print(f"  本次返回: {len(media_list)} 条")
        print(f"  RequestId: {request_id}")

        if not media_list:
            print("\n未找到匹配的媒体文件。")
            return result

        for i, media in enumerate(media_list, 1):
            print_media_info(media, index=i, verbose=args.verbose)

        # 分页提示
        offset = args.offset or 0
        limit = args.limit or 10
        if total > offset + limit:
            next_offset = offset + limit
            print(f"\n📄 还有 {total - next_offset} 条结果，使用 --offset {next_offset} 查看下一页")

        return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        error_msg = str(e)
        print(f"❌ 搜索失败: {error_msg}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='VOD 搜索媒体工具（SearchMedia）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
场景说明:
  SearchMedia 用于按条件搜索媒体（名称模糊匹配、分类、标签等）
  DescribeMediaInfos（vod_describe_media.py）用于按 FileId 精确查询

  当用户提供 FileId 时，两个脚本都可使用：
    - 精确查询详情 → vod_describe_media.py --file-id xxx
    - 搜索式查询   → vod_search_media.py --file-ids xxx

示例:
  # ✅ 模糊搜索名称（主应用）
  python vod_search_media.py --names "我的视频"

  # 通过 FileId 搜索（主应用）
  python vod_search_media.py --file-ids 387702292285462759

  # ✅ 模糊搜索名称（指定应用）
  python vod_search_media.py --names "我的视频" --sub-app-id 1500046806

  # ✅ 通过应用名称模糊匹配 + 名称搜索
  python vod_search_media.py --names "我的视频" --app-name "测试应用"

  # 搜索视频文件
  python vod_search_media.py --names "测试" --categories Video

  # 搜索图片文件
  python vod_search_media.py --names "封面" --categories Image

  # 按标签搜索
  python vod_search_media.py --tags "体育" "篮球"

  # 按创建时间范围搜索
  python vod_search_media.py --names "会议" \\
      --create-after "2026-01-01T00:00:00+08:00" \\
      --create-before "2026-03-31T23:59:59+08:00"

  # 按创建时间降序排序
  python vod_search_media.py --names "测试" \\
      --sort-field CreateTime --sort-order Desc

  # 分页查询
  python vod_search_media.py --names "视频" --offset 0 --limit 20

  # 只返回基础信息
  python vod_search_media.py --names "视频" --filters basicInfo

  # JSON 格式输出
  python vod_search_media.py --names "视频" --json

  # 预览请求参数
  python vod_search_media.py --names "视频" --dry-run
        '''
    )

    # 应用选择（互斥）
    app_group = parser.add_argument_group('应用选择')
    app_group.add_argument('--sub-app-id', type=int,
                           default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                           help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    app_group.add_argument('--app-name',
                           help='通过应用名称/描述模糊匹配子应用（与 --sub-app-id 互斥）')

    # 搜索条件
    search_group = parser.add_argument_group('搜索条件')
    search_group.add_argument('--file-ids', nargs='+',
                              help='文件 ID 列表（精确匹配，最多10个）')
    search_group.add_argument('--names', nargs='+',
                              help='文件名列表（模糊匹配，最多10个）')
    search_group.add_argument('--name-prefixes', nargs='+',
                              help='文件名前缀列表（前缀匹配，最多10个）')
    search_group.add_argument('--descriptions', nargs='+',
                              help='描述信息列表（模糊匹配，最多10个）')
    search_group.add_argument('--tags', nargs='+',
                              help='标签列表（匹配任一标签，最多16个）')
    search_group.add_argument('--class-ids', nargs='+', type=int,
                              help='分类 ID 列表（匹配分类及子分类，最多10个）')
    search_group.add_argument('--categories', nargs='+',
                              choices=['Video', 'Audio', 'Image'],
                              help='文件类型: Video/Audio/Image')
    search_group.add_argument('--source-types', nargs='+',
                              help='来源类型: Record/Upload/VideoProcessing/TrtcRecord 等')
    search_group.add_argument('--media-types', nargs='+',
                              help='封装格式: mp4/mp3/flv/jpg 等')
    search_group.add_argument('--status', nargs='+',
                              choices=['Normal', 'SystemForbidden', 'Forbidden'],
                              help='文件状态: Normal/SystemForbidden/Forbidden')
    search_group.add_argument('--review-results', nargs='+',
                              choices=['pass', 'review', 'block', 'notModerated'],
                              help='审核结果: pass/review/block/notModerated')
    search_group.add_argument('--storage-regions', nargs='+',
                              help='存储地区: ap-chongqing 等')
    search_group.add_argument('--storage-classes', nargs='+',
                              choices=['STANDARD', 'STANDARD_IA', 'ARCHIVE', 'DEEP_ARCHIVE'],
                              help='存储类型: STANDARD/STANDARD_IA/ARCHIVE/DEEP_ARCHIVE')
    search_group.add_argument('--stream-ids', nargs='+',
                              help='推流直播码列表（匹配任一，最多10个）')
    search_group.add_argument('--trtc-sdk-app-ids', nargs='+', type=int,
                              help='TRTC 应用 ID 列表（匹配任一，最多10个）')
    search_group.add_argument('--trtc-room-ids', nargs='+',
                              help='TRTC 房间 ID 列表（匹配任一，最多10个）')
    search_group.add_argument('--stream-domains', nargs='+',
                              help='直播推流 Domain 列表（直播录制时有效）')
    search_group.add_argument('--stream-paths', nargs='+',
                              help='直播推流 Path 列表（直播录制时有效）')

    # 时间范围
    time_group = parser.add_argument_group('时间范围')
    time_group.add_argument('--create-after',
                            help='创建时间起始（ISO 8601，如 2026-01-01T00:00:00+08:00）')
    time_group.add_argument('--create-before',
                            help='创建时间结束（ISO 8601，如 2026-12-31T23:59:59+08:00）')
    time_group.add_argument('--expire-after',
                            help='过期时间起始（ISO 8601，无法检索已过期文件）')
    time_group.add_argument('--expire-before',
                            help='过期时间结束（ISO 8601）')

    # 排序和分页
    page_group = parser.add_argument_group('排序和分页')
    page_group.add_argument('--sort-field', choices=['CreateTime'],
                            help='排序字段（当有 Names/Descriptions 时按匹配度排序，此参数无效）')
    page_group.add_argument('--sort-order', choices=['Asc', 'Desc'], default='Desc',
                            help='排序方式: Asc(升序)/Desc(降序)，默认 Desc')
    page_group.add_argument('--offset', type=int,
                            help='分页偏移量，默认 0')
    page_group.add_argument('--limit', type=int,
                            help='返回条数，默认 10（Offset+Limit 不超过 5000）')

    # 输出控制
    output_group = parser.add_argument_group('输出控制')
    output_group.add_argument('--filters', nargs='+',
                              help='返回信息过滤: basicInfo/metaData/transcodeInfo/animatedGraphicsInfo 等')
    output_group.add_argument('--verbose', '-v', action='store_true',
                              help='显示详细信息（包含 URL 等）')
    output_group.add_argument('--json', action='store_true',
                              help='JSON 格式输出完整响应')
    output_group.add_argument('--region', default='ap-guangzhou',
                              help='地域，默认 ap-guangzhou')
    output_group.add_argument('--dry-run', action='store_true',
                              help='预览请求参数，不实际执行')

    args = parser.parse_args()

    # 验证：至少需要一个搜索条件
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
        print("错误：至少需要指定一个搜索条件。")
        print("使用 --help 查看可用的搜索条件。")
        print("\n常用搜索条件:")
        print("  --names \"视频名称\"     按名称模糊搜索")
        print("  --file-ids FileId      按文件 ID 搜索")
        print("  --tags \"标签\"          按标签搜索")
        print("  --categories Video     按文件类型搜索")
        sys.exit(1)

    # 验证 app-name 和 sub-app-id 互斥
    if args.app_name and args.sub_app_id:
        print("错误：--app-name 和 --sub-app-id 不能同时指定")
        sys.exit(1)

    search_media(args)


if __name__ == '__main__':
    main()
