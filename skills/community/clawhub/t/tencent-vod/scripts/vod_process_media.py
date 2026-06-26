#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD 媒体处理脚本
支持普通转码、极速高清转码、转封装、视频增强、场景转码、截图、转动图、自适应码流等处理任务

极速高清转码模板：
- 在保证画质甚至提升画质的前提下，节省50%+带宽成本
- 支持同源/流畅/标清/高清等多种规格

转封装模板：
- 无需对视频、音频进行重新编码，仅转换封装格式
- 支持 MP4、HLS 格式

视频增强模板（大模型增强V2）：
- 降噪+超分+综合增强，帧率随源
- 通用场景 / 漫剧场景 / 真人短剧场景
- 支持 720P / 1080P / 2K / 4K

场景转码模板：
- 短剧场景：专项提升人物辨识度
- 电商场景：高效压缩视频大小
- 信息流场景：提升播放流畅性
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

# 软依赖：vod_load_env 用于在凭证缺失时从 ~/.env 等 dotenv 文件兜底加载
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


# 极速高清转码模板定义（TESHD - Top Speed Codec）
# 能够对不同类型的视频做自适应优化处理，以更低的带宽给用户提供更高清的观看体验
# 在保证画质甚至提升画质的前提下，节省50%+带宽成本
TESHD_TRANSCODE_TEMPLATES = {
    "same": {
        "id": 100800,
        "desc": "极速高清，MP4封装，同源分辨率，保留原视频分辨率和音频参数，高画质低码率",
        "resolution": "同源",
    },
    "flu": {
        "id": 100810,
        "desc": "极速高清，MP4封装，流畅画质(360P)，低码率省流量，适合移动网络快速加载",
        "resolution": "按比例缩放 × 360",
    },
    "sd": {
        "id": 100820,
        "desc": "极速高清，MP4封装，标清画质(540P)，低码率省成本，适合常规视频多终端分发",
        "resolution": "按比例缩放 × 540",
    },
    "hd": {
        "id": 100830,
        "desc": "极速高清，MP4封装，高清画质(720P)，低码率省成本，适合高清视频分发、在线教育",
        "resolution": "按比例缩放 × 720",
    },
}

# 转封装模板定义（Remux）
# 无需对视频、音频进行重新编码，仅转换视频的封装格式，无画质音质损失
REMUX_TEMPLATES = {
    "mp4": {
        "id": 875,
        "desc": "转封装为MP4格式，无需重新编码，无画质音质损失，适合全终端兼容播放",
    },
    "hls": {
        "id": 876,
        "desc": "转封装为HLS格式，无需重新编码，无画质音质损失，适合网页播放、直播分发",
    },
}

# 视频增强模板定义（大模型增强 V2）
# 降噪+超分+综合增强，帧率随源
VIDEO_ENHANCE_TEMPLATES = {
    # 通用场景
    "general": {
        "720":  {"id": 101410, "desc": "大模型增强-V2-720P-降噪+超分+综合增强"},
        "1080": {"id": 101430, "desc": "大模型增强-V2-1080P-降噪+超分+综合增强"},
        "2k":   {"id": 101450, "desc": "大模型增强-V2-2K-降噪+超分+综合增强"},
        "4k":   {"id": 101470, "desc": "大模型增强-V2-4K-降噪+超分+综合增强"},
    },
    # 漫剧场景
    "anime": {
        "720":  {"id": 101510, "desc": "漫剧场景-大模型增强-720P-降噪+超分+综合增强"},
        "1080": {"id": 101530, "desc": "漫剧场景-大模型增强-1080P-降噪+超分+综合增强"},
        "2k":   {"id": 101550, "desc": "漫剧场景-大模型增强-2K-降噪+超分+综合增强"},
        "4k":   {"id": 101570, "desc": "漫剧场景-大模型增强-4K-降噪+超分+综合增强"},
    },
    # 真人/短剧场景
    "live_action": {
        "720":  {"id": 101520, "desc": "真人/短剧场景-大模型增强-720P-降噪+超分+综合增强"},
        "1080": {"id": 101540, "desc": "真人/短剧场景-大模型增强-1080P-降噪+超分+综合增强"},
        "2k":   {"id": 101560, "desc": "真人/短剧场景-大模型增强-2K-降噪+超分+综合增强"},
        "4k":   {"id": 101580, "desc": "真人/短剧场景-大模型增强-4K-降噪+超分+综合增强"},
    },
}

# 场景转码模板定义
SCENE_TRANSCODE_TEMPLATES = {
    # 短剧场景 - 专项提升人物辨识度
    "short_drama": {
        "1080_best": 101300,      # 短剧_综合最佳_1080
        "1080_quality": 101301,   # 短剧_画质优先_1080
        "1080_bitrate": 101302,   # 短剧_码率优先_1080
        "720_best": 101303,       # 短剧_综合最佳_720
        "720_quality": 101304,    # 短剧_画质优先_720
        "720_bitrate": 101305,    # 短剧_码率优先_720
        "480_best": 101306,       # 短剧_综合最佳_480
        "480_quality": 101307,    # 短剧_画质优先_480
        "480_bitrate": 101308,    # 短剧_码率优先_480
    },
    # 电商场景 - 高效压缩视频大小
    "ecommerce": {
        "1080_best": 101309,      # 电商_综合最佳_1080
        "1080_quality": 101310,   # 电商_画质优先_1080
        "1080_bitrate": 101311,   # 电商_码率优先_1080
        "720_best": 101312,       # 电商_综合最佳_720
        "720_quality": 101313,    # 电商_画质优先_720
        "720_bitrate": 101314,    # 电商_码率优先_720
        "480_best": 101315,       # 电商_综合最佳_480
        "480_quality": 101316,    # 电商_画质优先_480
        "480_bitrate": 101317,    # 电商_码率优先_480
    },
    # 信息流场景 - 提升播放流畅性
    "feed": {
        "1080_best": 101318,      # 信息流_综合最佳_1080
        "1080_quality": 101319,   # 信息流_画质优先_1080
        "1080_bitrate": 101320,   # 信息流_码率优先_1080
        "720_best": 101321,       # 信息流_综合最佳_720
        "720_quality": 101322,    # 信息流_画质优先_720
        "720_bitrate": 101323,    # 信息流_码率优先_720
        "480_best": 101324,       # 信息流_综合最佳_480
        "480_quality": 101325,    # 信息流_画质优先_480
        "480_bitrate": 101326,    # 信息流_码率优先_480
    },
}


def get_scene_transcode_template_id(scene, resolution="1080", priority="best"):
    """
    获取场景转码模板ID

    Args:
        scene: 场景类型 (short_drama/ecommerce/feed)
        resolution: 分辨率 (1080/720/480)
        priority: 优先级 (best/quality/bitrate)

    Returns:
        模板ID 或 None
    """
    scene_templates = SCENE_TRANSCODE_TEMPLATES.get(scene)
    if not scene_templates:
        return None

    key = f"{resolution}_{priority}"
    return scene_templates.get(key)


def process_by_procedure(args):
    """使用任务流处理媒体"""
    # dry-run 模式不需要认证，先检查
    if args.dry_run:
        print("[DRY RUN] 请求参数:")
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

        print(f"处理任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"处理失败: {e}")
        sys.exit(1)


def teshd_transcode(args):
    """极速高清转码 - 以更低的带宽提供更高清的观看体验，节省50%+带宽成本"""
    # 获取模板
    template = TESHD_TRANSCODE_TEMPLATES.get(args.quality)
    if not template:
        print(f"错误：无效的画质等级: {args.quality}")
        print(f"可用等级: same(同源), flu(流畅360P), sd(标清540P), hd(高清720P)")
        sys.exit(1)

    template_id = template["id"]

    if args.dry_run:
        print("[DRY RUN] 极速高清转码请求参数:")
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

    # 构建转码任务
    transcode_task = models.TranscodeTaskInput()
    transcode_task.Definition = template_id

    # 构建水印列表
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
            "same": "同源",
            "flu": "流畅(360P)",
            "sd": "标清(540P)",
            "hd": "高清(720P)",
        }

        print(f"极速高清转码任务已提交!")
        print(f"画质等级: {quality_names.get(args.quality, args.quality)}")
        print(f"模板ID: {template_id}")
        print(f"说明: {template['desc']}")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"极速高清转码失败: {e}")
        sys.exit(1)


def remux(args):
    """转封装 - 无需重新编码，仅转换视频的封装格式，无画质音质损失"""
    # 获取模板
    template = REMUX_TEMPLATES.get(args.target_format)
    if not template:
        print(f"错误：无效的目标格式: {args.target_format}")
        print(f"可用格式: mp4, hls")
        sys.exit(1)

    template_id = template["id"]

    if args.dry_run:
        print("[DRY RUN] 转封装请求参数:")
        print(f"  FileId: {args.file_id}")
        print(f"  SubAppId: {args.sub_app_id}")
        print(f"  Format: {args.target_format}")
        print(f"  TemplateId: {template_id}")
        print(f"  Description: {template['desc']}")
        return

    client = get_client(args.region)

    req = models.ProcessMediaRequest()
    req.FileId = args.file_id

    # 转封装使用转码任务，但模板是转封装模板（无需重新编码）
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

        print(f"转封装任务已提交!")
        print(f"目标格式: {args.target_format.upper()}")
        print(f"模板ID: {template_id}")
        print(f"说明: {template['desc']}")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"转封装失败: {e}")
        sys.exit(1)


def video_enhance(args):
    """视频增强 - 大模型增强V2，降噪+超分+综合增强"""
    # 获取场景模板
    scene_templates = VIDEO_ENHANCE_TEMPLATES.get(args.scene)
    if not scene_templates:
        print(f"错误：无效的增强场景: {args.scene}")
        print(f"可用场景: general(通用), anime(漫剧), live_action(真人/短剧)")
        sys.exit(1)

    template = scene_templates.get(args.resolution)
    if not template:
        print(f"错误：无效的分辨率: {args.resolution}")
        print(f"可用分辨率: 720, 1080, 2k, 4k")
        sys.exit(1)

    template_id = template["id"]

    if args.dry_run:
        print("[DRY RUN] 视频增强请求参数:")
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

    # 视频增强使用转码任务，模板为视频增强预置模板
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
            "general": "通用",
            "anime": "漫剧",
            "live_action": "真人/短剧",
        }

        print(f"视频增强任务已提交!")
        print(f"增强场景: {scene_names.get(args.scene, args.scene)}")
        print(f"目标分辨率: {args.resolution}")
        print(f"模板ID: {template_id}")
        print(f"说明: {template['desc']}")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"视频增强失败: {e}")
        sys.exit(1)


def scene_transcode(args):
    """场景转码 - 基于极速高清的场景化转码"""
    # 获取模板ID
    template_id = get_scene_transcode_template_id(args.scene, args.resolution, args.priority)
    if not template_id:
        print(f"错误：无效的场景转码参数")
        print(f"场景: {args.scene}, 分辨率: {args.resolution}, 优先级: {args.priority}")
        print(f"可用场景: short_drama(短剧), ecommerce(电商), feed(信息流)")
        sys.exit(1)

    # dry-run 模式不需要认证，先检查
    if args.dry_run:
        print("[DRY RUN] 请求参数:")
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

    # 构建转码任务
    transcode_task = models.TranscodeTaskInput()
    transcode_task.Definition = template_id

    # 构建媒体处理任务
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
            "short_drama": "短剧",
            "ecommerce": "电商",
            "feed": "信息流"
        }
        priority_names = {
            "best": "综合最佳",
            "quality": "画质优先",
            "bitrate": "码率优先"
        }

        print(f"场景转码任务已提交!")
        print(f"场景: {scene_names.get(args.scene, args.scene)}")
        print(f"分辨率: {args.resolution}P")
        print(f"策略: {priority_names.get(args.priority, args.priority)}")
        print(f"模板ID: {template_id}")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"场景转码失败: {e}")
        sys.exit(1)


def make_snapshot(args):
    """对媒体截图 - 使用 ProcessMedia API"""
    # dry-run 模式不需要认证，先检查
    if args.dry_run:
        print("[DRY RUN] 请求参数:")
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

    # 构建截图任务
    snapshot_task = models.SnapshotByTimeOffsetTaskInput()
    snapshot_task.Definition = args.definition
    if args.ext_time_offset_set:
        snapshot_task.ExtTimeOffsetSet = args.ext_time_offset_set.split(',')

    # 构建水印列表
    if args.watermark_set:
        watermark_list = []
        for wm_def in args.watermark_set.split(','):
            wm = models.WatermarkInput()
            wm.Definition = int(wm_def.strip())
            watermark_list.append(wm)
        snapshot_task.WatermarkSet = watermark_list

    # 构建媒体处理任务
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

        print(f"截图任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"截图失败: {e}")
        sys.exit(1)


def make_animated_graphics(args):
    """转动图 - 使用 ProcessMedia API"""
    # dry-run 模式不需要认证，先检查
    if args.dry_run:
        print("[DRY RUN] 请求参数:")
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

    # 构建转动图任务
    gif_task = models.AnimatedGraphicTaskInput()
    gif_task.Definition = args.definition
    if args.start_time is not None:
        gif_task.StartTimeOffset = args.start_time
    if args.end_time is not None:
        gif_task.EndTimeOffset = args.end_time

    # 构建媒体处理任务
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

        print(f"转动图任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"转动图失败: {e}")
        sys.exit(1)


def sample_snapshot(args):
    """采样截图 - 使用 ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] 请求参数:")
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

    # 构建采样截图任务
    sample_task = models.SampleSnapshotTaskInput()
    sample_task.Definition = args.definition

    # 构建水印列表
    if args.watermark_set:
        watermark_list = []
        for wm_def in args.watermark_set.split(','):
            wm = models.WatermarkInput()
            wm.Definition = int(wm_def.strip())
            watermark_list.append(wm)
        sample_task.WatermarkSet = watermark_list

    # 构建媒体处理任务
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

        print(f"采样截图任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"采样截图失败: {e}")
        sys.exit(1)


def image_sprite(args):
    """雪碧图 - 使用 ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] 请求参数:")
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

    # 构建雪碧图任务
    sprite_task = models.ImageSpriteTaskInput()
    sprite_task.Definition = args.definition

    # 构建水印列表
    if args.watermark_set:
        watermark_list = []
        for wm_def in args.watermark_set.split(','):
            wm = models.WatermarkInput()
            wm.Definition = int(wm_def.strip())
            watermark_list.append(wm)
        sprite_task.WatermarkSet = watermark_list

    # 构建媒体处理任务
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

        print(f"雪碧图任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"雪碧图失败: {e}")
        sys.exit(1)


def cover_by_snapshot(args):
    """截图做封面 - 使用 ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] 请求参数:")
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

    # 构建截图做封面任务
    cover_task = models.CoverBySnapshotTaskInput()
    cover_task.Definition = args.definition
    cover_task.PositionType = args.position_type
    cover_task.PositionValue = args.position_value

    # 构建水印列表
    if args.watermark_set:
        watermark_list = []
        for wm_def in args.watermark_set.split(','):
            wm = models.WatermarkInput()
            wm.Definition = int(wm_def.strip())
            watermark_list.append(wm)
        cover_task.WatermarkSet = watermark_list

    # 构建媒体处理任务
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

        print(f"截图做封面任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"截图做封面失败: {e}")
        sys.exit(1)


def adaptive_streaming(args):
    """自适应码流 - 使用 ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] 请求参数:")
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

    # 构建自适应码流任务
    adaptive_task = models.AdaptiveDynamicStreamingTaskInput()
    adaptive_task.Definition = args.definition
    if args.subtitle_set:
        adaptive_task.SubtitleSet = args.subtitle_set.split(',')

    # 构建媒体处理任务
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

        print(f"自适应码流任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"自适应码流失败: {e}")
        sys.exit(1)


def ai_content_review(args):
    """AI内容审核 - 使用 ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] 请求参数:")
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

    # 构建AI内容审核任务
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

        print(f"AI内容审核任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"AI内容审核失败: {e}")
        sys.exit(1)


def ai_analysis(args):
    """AI内容分析 - 使用 ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] 请求参数:")
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

    # 构建AI内容分析任务
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

        print(f"AI内容分析任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"AI内容分析失败: {e}")
        sys.exit(1)


def ai_recognition(args):
    """AI内容识别 - 使用 ProcessMedia API"""
    if args.dry_run:
        print("[DRY RUN] 请求参数:")
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

    # 构建AI内容识别任务
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

        print(f"AI内容识别任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")
        if args.json or args.verbose:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:
        print(f"AI内容识别失败: {e}")
        sys.exit(1)


def wait_for_task(client, task_id, sub_app_id=None, max_wait=600):
    """等待任务完成"""
    print(f"\n等待任务完成 (TaskId: {task_id})...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        req = models.DescribeTaskDetailRequest()
        req.TaskId = task_id
        if sub_app_id:
            req.SubAppId = sub_app_id
        
        try:
            resp = client.DescribeTaskDetail(req)
            result = json.loads(resp.to_json_string())
            
            # VOD DescribeTaskDetail API 的 Status 在顶层，不在嵌套的 TaskDetail 中
            status = result.get('Status', 'PROCESSING')
            print(f"  当前状态: {status}")
            
            if status == 'FINISH':
                print("任务完成!")
                return result
            elif status == 'FAIL':
                err_msg = result.get('ErrCodeExt', '') or result.get('Message', '')
                print(f"任务失败! {err_msg}")
                return result
            
            time.sleep(5)
        except Exception as e:
            print(f"查询任务状态失败: {e}")
            time.sleep(5)
    
    print(f"⏱️ 等待超时（{max_wait}秒），任务仍在执行中")
    return None


def main():
    parser = argparse.ArgumentParser(
        description='VOD 媒体处理工具 - 支持极速高清转码/转封装/场景转码/截图/转动图等',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python vod_process_media.py procedure --file-id <id> --procedure "SimpleAes"
  python vod_process_media.py transcode --file-id <id>                        # 极速高清(同源)
  python vod_process_media.py transcode --file-id <id> --quality hd           # 极速高清(720P)
  python vod_process_media.py remux --file-id <id> --target-format mp4        # 转封装MP4
  python vod_process_media.py enhance --file-id <id>                          # 视频增强(通用1080P)
  python vod_process_media.py enhance --file-id <id> --scene anime --resolution 4k  # 漫剧4K增强
  python vod_process_media.py scene-transcode --file-id <id> --scene short_drama
  python vod_process_media.py snapshot --file-id <id> --definition 10001 --ext-time-offset-set "5s,10s"

TESHD: same(100800)/flu(100810,360P)/sd(100820,540P)/hd(100830,720P)
Remux: mp4(875)/hls(876)
Enhance: general/anime/live_action x 720/1080/2k/4k (default: general 1080, id=101430)
Scene: short_drama/ecommerce/feed x 1080/720/480 x best/quality/bitrate
        '''
    )

    # 公共参数（通过 parent parser 让所有子命令继承 -v/--verbose）
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('-v', '--verbose', action='store_true', help='输出详细信息（含完整 API 响应）')

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # 任务流处理
    proc_parser = subparsers.add_parser('procedure', help='使用任务流处理', parents=[common_parser])
    proc_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    proc_parser.add_argument('--procedure', required=True, help='任务流名称')
    proc_parser.add_argument('--sub-app-id', type=int,
                              default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                              help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    proc_parser.add_argument('--media-storage-path', help='媒体存储路径（仅FileID + Path模式子应用可用）')
    proc_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='任务流状态变更通知模式')
    proc_parser.add_argument('--session-id', help='用于去重的识别码（三天内重复会返回错误）')
    proc_parser.add_argument('--ext-info', help='扩展信息')
    proc_parser.add_argument('--tasks-priority', type=int, help='任务优先级')
    proc_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    proc_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    proc_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    proc_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    proc_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # 极速高清转码
    teshd_parser = subparsers.add_parser('transcode', help='极速高清转码(TESHD), 以更低带宽提供更高清体验, 节省一半以上带宽成本', parents=[common_parser])
    teshd_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    teshd_parser.add_argument('--quality', default='same',
                              choices=['same', 'flu', 'sd', 'hd'],
                              help='画质等级: same(同源,默认100800)/flu(流畅360P,100810)/sd(标清540P,100820)/hd(高清720P,100830)')
    teshd_parser.add_argument('--watermark-set', help='水印模板ID列表，逗号分隔，如 "10001,10002"')
    teshd_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                               help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    teshd_parser.add_argument('--session-context', help='来源上下文，用于透传用户请求信息')
    teshd_parser.add_argument('--tasks-priority', type=int, help='任务优先级 (-10到10)')
    teshd_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    teshd_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    teshd_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    teshd_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    teshd_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # 转封装
    remux_parser = subparsers.add_parser('remux', help='转封装（无需重新编码，仅转换封装格式，无画质音质损失）', parents=[common_parser])
    remux_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    remux_parser.add_argument('--target-format', required=True, dest='target_format',
                              choices=['mp4', 'hls'],
                              help='目标封装格式: mp4(模板875)/hls(模板876)')
    remux_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                               help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    remux_parser.add_argument('--session-context', help='来源上下文，用于透传用户请求信息')
    remux_parser.add_argument('--tasks-priority', type=int, help='任务优先级 (-10到10)')
    remux_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    remux_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    remux_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    remux_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    remux_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # 视频增强
    enhance_parser = subparsers.add_parser('enhance', help='视频增强(大模型增强V2), 降噪+超分+综合增强', parents=[common_parser])
    enhance_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    enhance_parser.add_argument('--scene', default='general',
                                choices=['general', 'anime', 'live_action'],
                                help='增强场景: general(通用,默认)/anime(漫剧)/live_action(真人/短剧)')
    enhance_parser.add_argument('--resolution', default='1080',
                                choices=['720', '1080', '2k', '4k'],
                                help='目标分辨率: 720/1080(默认)/2k/4k')
    enhance_parser.add_argument('--sub-app-id', type=int,
                                 default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                 help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    enhance_parser.add_argument('--session-context', help='来源上下文，用于透传用户请求信息')
    enhance_parser.add_argument('--tasks-priority', type=int, help='任务优先级 (-10到10)')
    enhance_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    enhance_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    enhance_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    enhance_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    enhance_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # 场景转码
    scene_parser = subparsers.add_parser('scene-transcode', help='场景转码（极速高清）', parents=[common_parser])
    scene_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    scene_parser.add_argument('--scene', required=True,
                              choices=['short_drama', 'ecommerce', 'feed'],
                              help='场景类型: short_drama(短剧)/ecommerce(电商)/feed(信息流)')
    scene_parser.add_argument('--resolution', default='1080',
                              choices=['1080', '720', '480'],
                              help='输出分辨率 (默认: 1080)')
    scene_parser.add_argument('--priority', default='best',
                              choices=['best', 'quality', 'bitrate'],
                              help='转码策略: best(综合最佳)/quality(画质优先)/bitrate(码率优先) (默认: best)')
    scene_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                               help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    scene_parser.add_argument('--session-context', help='来源上下文，用于透传用户请求信息')
    scene_parser.add_argument('--tasks-priority', type=int, help='任务优先级 (-10到10)')
    scene_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    scene_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    scene_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    scene_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    scene_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # 截图
    snap_parser = subparsers.add_parser('snapshot', help='截图', parents=[common_parser])
    snap_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    snap_parser.add_argument('--definition', type=int, required=True, help='截图模板 ID')
    snap_parser.add_argument('--ext-time-offset-set', help='截图时间点列表, 逗号分隔, 如 "5s,10s,15s" 或 "10pct,20pct,30pct"')
    snap_parser.add_argument('--watermark-set', help='水印模板ID列表，逗号分隔，如 "10001,10002"')
    snap_parser.add_argument('--sub-app-id', type=int,
                              default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                              help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    snap_parser.add_argument('--media-storage-path', help='媒体存储路径（仅FileID + Path模式子应用可用）')
    snap_parser.add_argument('--session-id', help='用于去重的识别码（三天内重复会返回错误）')
    snap_parser.add_argument('--ext-info', help='扩展信息')
    snap_parser.add_argument('--tasks-priority', type=int, help='任务优先级')
    snap_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='任务状态变更通知模式')
    snap_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    snap_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    snap_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    snap_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    snap_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # 转动图
    gif_parser = subparsers.add_parser('gif', help='转动图', parents=[common_parser])
    gif_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    gif_parser.add_argument('--definition', type=int, required=True, help='转动图模板 ID')
    gif_parser.add_argument('--start-time', type=float, help='开始时间偏移(秒)')
    gif_parser.add_argument('--end-time', type=float, help='结束时间偏移(秒)')
    gif_parser.add_argument('--sub-app-id', type=int,
                             default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                             help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    gif_parser.add_argument('--media-storage-path', help='媒体存储路径（仅FileID + Path模式子应用可用）')
    gif_parser.add_argument('--session-id', help='用于去重的识别码（三天内重复会返回错误）')
    gif_parser.add_argument('--ext-info', help='扩展信息')
    gif_parser.add_argument('--tasks-priority', type=int, help='任务优先级')
    gif_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='任务状态变更通知模式')
    gif_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    gif_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    gif_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    gif_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    gif_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # 采样截图
    sample_parser = subparsers.add_parser('sample-snapshot', help='采样截图', parents=[common_parser])
    sample_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    sample_parser.add_argument('--definition', type=int, required=True, help='采样截图模板 ID')
    sample_parser.add_argument('--watermark-set', help='水印模板ID列表，逗号分隔，如 "10001,10002"')
    sample_parser.add_argument('--sub-app-id', type=int,
                                default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    sample_parser.add_argument('--media-storage-path', help='媒体存储路径（仅FileID + Path模式子应用可用）')
    sample_parser.add_argument('--session-id', help='用于去重的识别码（三天内重复会返回错误）')
    sample_parser.add_argument('--ext-info', help='扩展信息')
    sample_parser.add_argument('--tasks-priority', type=int, help='任务优先级')
    sample_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='任务状态变更通知模式')
    sample_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    sample_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    sample_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    sample_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    sample_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # 雪碧图
    sprite_parser = subparsers.add_parser('image-sprite', help='雪碧图', parents=[common_parser])
    sprite_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    sprite_parser.add_argument('--definition', type=int, required=True, help='雪碧图模板 ID')
    sprite_parser.add_argument('--watermark-set', help='水印模板ID列表，逗号分隔，如 "10001,10002"')
    sprite_parser.add_argument('--sub-app-id', type=int,
                                default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    sprite_parser.add_argument('--media-storage-path', help='媒体存储路径（仅FileID + Path模式子应用可用）')
    sprite_parser.add_argument('--session-id', help='用于去重的识别码（三天内重复会返回错误）')
    sprite_parser.add_argument('--ext-info', help='扩展信息')
    sprite_parser.add_argument('--tasks-priority', type=int, help='任务优先级')
    sprite_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='任务状态变更通知模式')
    sprite_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    sprite_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    sprite_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    sprite_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    sprite_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # 截图做封面
    cover_parser = subparsers.add_parser('cover-by-snapshot', help='截图做封面', parents=[common_parser])
    cover_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    cover_parser.add_argument('--definition', type=int, required=True, help='截图模板 ID')
    cover_parser.add_argument('--position-type', required=True, choices=['Time', 'Percent'], help='截图方式: Time(时间点)/Percent(百分比)')
    cover_parser.add_argument('--position-value', type=float, required=True, help='截图位置: Time方式单位为秒，Percent方式为0-100的百分比')
    cover_parser.add_argument('--watermark-set', help='水印模板ID列表，逗号分隔，如 "10001,10002"')
    cover_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                               help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    cover_parser.add_argument('--media-storage-path', help='媒体存储路径（仅FileID + Path模式子应用可用）')
    cover_parser.add_argument('--session-id', help='用于去重的识别码（三天内重复会返回错误）')
    cover_parser.add_argument('--ext-info', help='扩展信息')
    cover_parser.add_argument('--tasks-priority', type=int, help='任务优先级')
    cover_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='任务状态变更通知模式')
    cover_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    cover_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    cover_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    cover_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    cover_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # 自适应码流
    adaptive_parser = subparsers.add_parser('adaptive-streaming', help='自适应码流', parents=[common_parser])
    adaptive_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    adaptive_parser.add_argument('--definition', type=int, required=True, help='自适应码流模板 ID')
    adaptive_parser.add_argument('--subtitle-set', help='字幕ID列表，逗号分隔')
    adaptive_parser.add_argument('--sub-app-id', type=int,
                                  default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                  help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    adaptive_parser.add_argument('--media-storage-path', help='媒体存储路径（仅FileID + Path模式子应用可用）')
    adaptive_parser.add_argument('--session-id', help='用于去重的识别码（三天内重复会返回错误）')
    adaptive_parser.add_argument('--ext-info', help='扩展信息')
    adaptive_parser.add_argument('--tasks-priority', type=int, help='任务优先级')
    adaptive_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='任务状态变更通知模式')
    adaptive_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    adaptive_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    adaptive_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    adaptive_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    adaptive_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # AI内容审核
    review_parser = subparsers.add_parser('ai-review', help='AI内容审核（不建议使用，推荐使用 ReviewAudioVideo）', parents=[common_parser])
    review_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    review_parser.add_argument('--definition', type=int, required=True, help='音视频审核模板 ID')
    review_parser.add_argument('--sub-app-id', type=int,
                                default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    review_parser.add_argument('--media-storage-path', help='媒体存储路径（仅FileID + Path模式子应用可用）')
    review_parser.add_argument('--session-id', help='用于去重的识别码（三天内重复会返回错误）')
    review_parser.add_argument('--ext-info', help='扩展信息')
    review_parser.add_argument('--tasks-priority', type=int, help='任务优先级')
    review_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='任务状态变更通知模式')
    review_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    review_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    review_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    review_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    review_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # AI内容分析
    analysis_parser = subparsers.add_parser('ai-analysis', help='AI内容分析', parents=[common_parser])
    analysis_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    analysis_parser.add_argument('--definition', type=int, required=True, help='视频内容分析模板 ID')
    analysis_parser.add_argument('--sub-app-id', type=int,
                                  default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                  help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    analysis_parser.add_argument('--media-storage-path', help='媒体存储路径（仅FileID + Path模式子应用可用）')
    analysis_parser.add_argument('--session-id', help='用于去重的识别码（三天内重复会返回错误）')
    analysis_parser.add_argument('--ext-info', help='扩展信息')
    analysis_parser.add_argument('--tasks-priority', type=int, help='任务优先级')
    analysis_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='任务状态变更通知模式')
    analysis_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    analysis_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    analysis_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    analysis_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    analysis_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

    # AI内容识别
    recognition_parser = subparsers.add_parser('ai-recognition', help='AI内容识别', parents=[common_parser])
    recognition_parser.add_argument('--file-id', required=True, help='媒体 FileId')
    recognition_parser.add_argument('--definition', type=int, required=True, help='视频智能识别模板 ID')
    recognition_parser.add_argument('--sub-app-id', type=int,
                                     default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                                     help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    recognition_parser.add_argument('--media-storage-path', help='媒体存储路径（仅FileID + Path模式子应用可用）')
    recognition_parser.add_argument('--session-id', help='用于去重的识别码（三天内重复会返回错误）')
    recognition_parser.add_argument('--ext-info', help='扩展信息')
    recognition_parser.add_argument('--tasks-priority', type=int, help='任务优先级')
    recognition_parser.add_argument('--tasks-notify-mode', choices=['Finish', 'Change', 'None'], help='任务状态变更通知模式')
    recognition_parser.add_argument('--region', default='ap-guangzhou', help='地域')
    recognition_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    recognition_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)')
    recognition_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    recognition_parser.add_argument('--dry-run', action='store_true', help='预览请求参数')

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