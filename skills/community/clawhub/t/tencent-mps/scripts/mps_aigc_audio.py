#!/usr/bin/env python3
"""
腾讯云 MPS AIGC 生音频脚本

功能：
  封装 CreateAigcAudioTask + DescribeAigcAudioTask 两个 API，
  支持创建任务 + 自动轮询等待结果 + 结果下载。

支持的模型与场景（均经真接口验证）：
  ┌──────────────┬────────────────────────┬──────────────┐
  │ 场景          │ 模型 (--model)          │ 版本          │
  ├──────────────┼────────────────────────┼──────────────┤
  │ 音效 sfx      │ Kling                  │ （不填）      │
  │ 音乐 music    │ MiniMaxMusic           │ 2.0/2.5/2.6/3.0 │
  │ 音乐 music    │ GL（Google Lyria）      │ 3.0-clip / 3.0-pro │
  │ 音乐 music    │ Tme（歌曲翻唱）          │ （不填）      │
  └──────────────┴────────────────────────┴──────────────┘

核心能力：
  - 文生音效（Kling，--scene-type sfx）：由文本描述生成音效
  - 视频生音效（Kling + --ref-video-url）：依据视频内容生成匹配音效
  - 文生音乐（MiniMaxMusic / GL，--scene-type music）：支持 --lyric 传入歌词
  - 纯音乐（MiniMaxMusic + --instrumental）：不含人声
  - 歌曲翻唱（Tme + --ref-audio-url + --song-id）
  - 输出格式可选 mp3 / wav，结果可存回自有 COS 桶

用法：
  # 文生音效（Kling）
  python3 mps_aigc_audio.py --prompt "雨声与远处的雷声，电影氛围" --scene-type sfx

  # 视频生音效：依据视频内容生成匹配音效
  python3 mps_aigc_audio.py --scene-type sfx --prompt "与画面匹配的环境音" \
      --ref-video-url https://example.com/src.mp4

  # 文生音乐 + 歌词（MiniMaxMusic）
  python3 mps_aigc_audio.py --model MiniMaxMusic --model-version 2.6 \
      --prompt "轻快的流行音乐，节奏明快" \
      --lyric "阳光洒在窗台上\n新的一天开始了"

  # 纯音乐（无人声）
  python3 mps_aigc_audio.py --model MiniMaxMusic --prompt "轻柔的钢琴曲" --instrumental

  # 文生音乐（GL / Google Lyria）
  python3 mps_aigc_audio.py --model GL --model-version 3.0-pro \
      --prompt "an epic orchestral soundtrack with rising tension"

  # 歌曲翻唱（Tme）：需提供授权歌曲 ID
  python3 mps_aigc_audio.py --model Tme --song-id 4758500_1 \
      --ref-audio-url https://example.com/source.wav

  # 指定输出格式 + 下载到本地
  python3 mps_aigc_audio.py --prompt "海浪声" --output-audio-format wav --download-dir ./out

  # 仅创建任务不等待 / 查询已有任务
  python3 mps_aigc_audio.py --prompt "鸟鸣" --no-wait
  python3 mps_aigc_audio.py --task-id 2600011633-AigcAudio-xxxxxxxx

  # Dry Run（仅打印请求参数）
  python3 mps_aigc_audio.py --prompt "测试" --dry-run

环境变量：
  TENCENTCLOUD_SECRET_ID   腾讯云 SecretId
  TENCENTCLOUD_SECRET_KEY  腾讯云 SecretKey
  TENCENTCLOUD_COS_BUCKET  COS Bucket 名称（可选，用于结果存储）
  TENCENTCLOUD_COS_REGION  COS Bucket 区域（默认 ap-guangzhou）
"""

import argparse
import json
import os
import sys
import time

# 依赖自动检查/升级：必须在 tencentcloud 首次 import 之前调用
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mps_auto_upgrade  # noqa: F401
from mps_auto_upgrade import check_sdk_version

check_sdk_version()

from mps_load_env import ensure_env_loaded

ensure_env_loaded()

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.mps.v20190612 import mps_client, models

# 复用生图脚本中已验证的 COS 与提示逻辑，避免重复实现
from mps_aigc_image import (
    get_cos_bucket,
    get_cos_region,
    get_cos_presigned_url,
    ensure_signed_url,
    print_storage_hint,
)

# =============================================================================
# 模型信息（取值全部来自真接口验证，2026-08-08）
# =============================================================================
SUPPORTED_MODELS = {
    "Kling": {
        "description": "可灵 — 文生音效 / 视频生音效",
        "versions": [],                 # 不接受版本号
        "scenes": ["sfx"],
        "supports_lyric": False,
    },
    "MiniMaxMusic": {
        "description": "MiniMax — 文生音乐（支持歌词 / 纯音乐）",
        # 3.0 已真接口验证可用（actions/*.json 仅收录到 2.6，实际更新）
        "versions": ["2.0", "2.5", "2.6", "3.0"],
        "scenes": ["music"],
        "supports_lyric": True,
        # 实测：不传 ModelVersion 时接口报 Not support this ModelVersion，故必填
        "requires_version": True,
    },
    "GL": {
        "description": "Google Lyria — 文生音乐",
        "versions": ["3.0-clip", "3.0-pro"],
        "scenes": ["music"],
        "supports_lyric": True,
        "requires_version": True,
        # 实测：3.0-pro 不传歌词会任务失败（no parts in response）；3.0-clip 无此限制
        "lyric_required_versions": ["3.0-pro"],
    },
    "Tme": {
        "description": "腾讯音乐 — 歌曲翻唱",
        "versions": [],
        "scenes": ["music"],
        "supports_lyric": False,
    },
}

# 接口实际支持的场景（实测报错原文：Invalid SceneType. Supported: tts,music,sfx）。
# tts 由语音合成链路承载（Kling 传 tts 报 Invalid model name for TTS），
# 本脚本不暴露，语音合成请用 mps_dubbing.py。
SUPPORTED_SCENES = ["sfx", "music"]

DEFAULT_POLL_INTERVAL = 5
DEFAULT_MAX_WAIT = 600      # 音乐生成较慢，实测可达 3~4 分钟


def create_mps_client(cred, region):
    """创建 MPS 客户端。"""
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    http_profile.reqMethod = "POST"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(cred, region, client_profile)


try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False


def get_credentials():
    """从环境变量获取腾讯云凭证。若缺失则尝试从 dotenv 文件自动加载后重试。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        # 凭证可能写在 ~/.env 等 dotenv 文件中而未导出，先尝试加载再重试
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] 环境变量未设置，尝试从系统文件自动加载...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from mps_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print(
                    "\n错误：TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY 未设置。\n"
                    "请在 ~/.env、~/.bashrc、~/.profile 或 <SKILL_DIR>/.env 中添加这些变量。\n",
                    file=sys.stderr,
                )
            sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def resolve_media_url(url, cos_key, cos_bucket, cos_region, label):
    """把 URL / COS Key 统一解析为可外网访问的 URL。

    CreateAigcAudioTask 的 VideoInfos / AudioInfos 只接受 URL，不支持 CosInputInfo，
    因此 COS 输入统一转为预签名 URL（与生图/生视频脚本一致）。
    """
    if url:
        return url
    if not cos_key:
        return None
    bucket = cos_bucket or get_cos_bucket()
    region = cos_region or get_cos_region()
    if not bucket:
        print(f"❌ 错误：{label} 需要指定 COS Bucket（--{label}-cos-bucket 或 TENCENTCLOUD_COS_BUCKET）",
              file=sys.stderr)
        sys.exit(1)
    signed = get_cos_presigned_url(bucket, region, cos_key.lstrip("/"))
    if not signed:
        print(f"❌ 错误：无法为 {label} 生成预签名 URL", file=sys.stderr)
        sys.exit(1)
    return signed


def build_create_params(args):
    """构建 CreateAigcAudioTask 请求参数。"""
    params = {"ModelName": args.model, "SceneType": args.scene_type}

    if args.model_version:
        params["ModelVersion"] = args.model_version
    if args.prompt:
        params["Prompt"] = args.prompt

    # 参考视频（视频生音效）
    video_url = resolve_media_url(args.ref_video_url, args.ref_video_cos_key,
                                  args.ref_video_cos_bucket, args.ref_video_cos_region,
                                  "ref-video")
    if video_url:
        params["VideoInfos"] = [{"VideoUrl": video_url}]

    # 参考音频（歌曲翻唱 / 音频生音乐）
    audio_url = resolve_media_url(args.ref_audio_url, args.ref_audio_cos_key,
                                  args.ref_audio_cos_bucket, args.ref_audio_cos_region,
                                  "ref-audio")
    if audio_url:
        params["AudioInfos"] = [{"AudioUrl": audio_url}]

    if args.output_audio_format:
        params["OutputAudioFormat"] = args.output_audio_format

    # Tme 歌曲翻唱通过 ExtraParameters.ResourceId 指定授权歌曲
    if args.song_id:
        params["ExtraParameters"] = {"ResourceId": args.song_id}

    # AdditionalParameters：歌词 / 纯音乐开关 / 用户自定义（JSON 字符串）
    additional = {}
    if args.additional_parameters:
        additional.update(json.loads(args.additional_parameters))
    if args.lyric:
        # 允许用户在命令行写字面量 \n 作为换行
        additional["lyric"] = args.lyric.replace("\\n", "\n")
    if args.instrumental:
        additional["is_instrumental"] = True
    if additional:
        params["AdditionalParameters"] = json.dumps(additional, ensure_ascii=False)

    cos_param = build_store_cos_param(args)
    if cos_param:
        params["StoreCosParam"] = cos_param

    if args.operator:
        params["Operator"] = args.operator

    return params


def build_store_cos_param(args):
    """构建结果存储 COS 参数；未配置则返回 None（走 MPS 临时存储）。"""
    bucket = args.cos_bucket_name or get_cos_bucket()
    if not bucket:
        return None
    return {
        "CosBucketName": bucket,
        "CosBucketRegion": args.cos_bucket_region or get_cos_region(),
        "CosBucketPath": args.cos_bucket_path,
    }


def create_aigc_audio_task(client, params):
    """提交生音频任务，返回 TaskId。"""
    req = models.CreateAigcAudioTaskRequest()
    req.from_json_string(json.dumps(params))
    return client.CreateAigcAudioTask(req)


def describe_aigc_audio_task(client, task_id):
    """查询生音频任务状态。"""
    req = models.DescribeAigcAudioTaskRequest()
    req.from_json_string(json.dumps({"TaskId": task_id}))
    return json.loads(client.DescribeAigcAudioTask(req).to_json_string())


def poll_task_result(client, task_id, poll_interval, max_wait):
    """轮询任务直到 DONE / FAIL 或超时。"""
    waited = 0
    status_text = {"WAIT": "等待中", "RUN": "执行中"}
    while waited < max_wait:
        result = describe_aigc_audio_task(client, task_id)
        status = result.get("Status")
        if status in ("DONE", "FAIL"):
            return result
        print(f"⏳ 任务状态: {status_text.get(status, status)}"
              f"（已等待 {waited}s / 最长 {max_wait}s）", end="\r", flush=True)
        time.sleep(poll_interval)
        waited += poll_interval
    print()
    print(f"⏱️  等待超时（{max_wait}秒），可稍后用 --task-id {task_id} 查询", file=sys.stderr)
    return None


def download_audios(audio_infos, download_dir):
    """下载生成的音频到本地目录。"""
    import urllib.request
    from urllib.parse import urlparse

    os.makedirs(download_dir, exist_ok=True)
    for idx, info in enumerate(audio_infos, 1):
        url = info.get("Url")
        if not url:
            continue
        ext = os.path.splitext(urlparse(url).path)[1] or ".mp3"
        dest = os.path.join(download_dir, f"aigc_audio_{int(time.time())}_{idx}{ext}")
        try:
            urllib.request.urlretrieve(url, dest)
            print(f"⬇️  已下载: {dest}")
        except Exception as exc:  # 下载失败不应影响主流程，URL 已打印
            print(f"⚠️  下载失败（音频 {idx}）: {exc}", file=sys.stderr)


def print_audio_results(result):
    """打印任务结果中的音频信息。"""
    audio_infos = result.get("AudioInfos") or []
    if not audio_infos:
        print("⚠️  任务已完成，但未返回音频信息")
        return audio_infos

    print(f"✅ 任务完成！生成音频数量: {len(audio_infos)}")
    statuses = []
    for idx, info in enumerate(audio_infos, 1):
        url, status = ensure_signed_url(info.get("Url", ""))
        info["Url"] = url
        statuses.append(status)
        duration = info.get("Duration")
        suffix = f"（时长 {duration}s）" if duration else ""
        print(f"  音频 {idx}{suffix}: {url}")
    print_storage_hint(statuses)
    return audio_infos


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def validate_args(args, parser):
    """校验参数。"""
    if args.task_id:
        return

    model_info = SUPPORTED_MODELS[args.model]

    # 版本必填校验（实测：MiniMaxMusic / GL 不传版本报 Not support this ModelVersion）
    if model_info.get("requires_version") and not args.model_version:
        parser.error(
            f"模型 {args.model} 必须通过 --model-version 指定版本"
            f"（可选：{', '.join(model_info['versions'])}）。"
            f"不指定会被接口拒绝（Not support this ModelVersion）"
        )

    # 歌词必填校验（实测：GL 3.0-pro 缺歌词任务会失败，报 no parts in response）
    lyric_required = model_info.get("lyric_required_versions", [])
    if args.model_version in lyric_required and not (args.lyric or args.additional_parameters):
        parser.error(
            f"{args.model} {args.model_version} 必须通过 --lyric 提供歌词，"
            f"否则任务会失败（no parts in response）。"
            f"如需纯音乐，请改用 {' / '.join(v for v in model_info['versions'] if v not in lyric_required)}"
        )

    # 版本校验：Kling / Tme 不接受版本号
    if args.model_version:
        valid = model_info["versions"]
        if not valid:
            parser.error(f"模型 {args.model} 不需要指定 --model-version")
        if args.model_version not in valid:
            parser.error(
                f"模型 {args.model} 支持的版本为: {', '.join(valid)}，"
                f"当前指定: {args.model_version}"
            )

    # 场景与模型必须匹配（实测：Kling 只支持 sfx，音乐类模型只支持 music）
    if args.scene_type not in model_info["scenes"]:
        supported = [m for m, i in SUPPORTED_MODELS.items() if args.scene_type in i["scenes"]]
        parser.error(
            f"模型 {args.model} 不支持场景 {args.scene_type}（该模型支持: "
            f"{', '.join(model_info['scenes'])}）。"
            f"支持 {args.scene_type} 的模型为: {' / '.join(supported)}"
        )

    # Tme 歌曲翻唱必须提供授权歌曲 ID 与参考音频（实测缺失时报 SongId is required for TME model）
    if args.model == "Tme":
        if not args.song_id:
            parser.error("Tme 歌曲翻唱必须通过 --song-id 指定已授权的歌曲 ID")
        if not (args.ref_audio_url or args.ref_audio_cos_key):
            parser.error("Tme 歌曲翻唱必须通过 --ref-audio-url / --ref-audio-cos-key 提供参考音频")
    elif args.song_id:
        parser.error("--song-id 仅 Tme 模型使用")

    # 歌词 / 纯音乐仅音乐类模型支持
    if args.lyric and not model_info["supports_lyric"]:
        parser.error(f"--lyric 仅 MiniMaxMusic / GL 支持，当前模型: {args.model}")
    if args.instrumental and args.model != "MiniMaxMusic":
        parser.error(f"--instrumental（纯音乐）仅 MiniMaxMusic 支持，当前模型: {args.model}")
    if args.lyric and args.instrumental:
        parser.error("--lyric 与 --instrumental 互斥：纯音乐不含人声，无法同时指定歌词")

    # 参考视频仅 Kling 音效场景支持
    if (args.ref_video_url or args.ref_video_cos_key) and args.model != "Kling":
        parser.error(f"参考视频（视频生音效）仅 Kling 支持，当前模型: {args.model}")

    # Prompt 必填性：除 Tme（以参考音频为输入）外都需要描述
    if not args.prompt and args.model != "Tme":
        parser.error("请指定 --prompt（音频描述，最多 2000 字符）")
    if args.prompt and len(args.prompt) > 2000:
        parser.error(f"--prompt 最多 2000 字符，当前 {len(args.prompt)} 字符")

    if args.additional_parameters:
        try:
            extra = json.loads(args.additional_parameters)
        except json.JSONDecodeError:
            parser.error("--additional-parameters 必须是有效的 JSON 字符串，"
                         "例如: '{\"is_instrumental\":true}'")
        # 必须是 JSON 对象：后续要与 --lyric / --instrumental 合并（dict.update），
        # 传数组或标量会在合并时抛 TypeError
        if not isinstance(extra, dict):
            parser.error("--additional-parameters 必须是 JSON 对象（键值对），"
                         f"当前为 {type(extra).__name__}。"
                         "例如: '{\"is_instrumental\":true}'")


def run(args):
    """执行主流程。"""
    region = args.region or os.environ.get("TENCENTCLOUD_API_REGION", "ap-guangzhou")

    # 模式1：查询已有任务
    if args.task_id:
        client = create_mps_client(get_credentials(), region)
        print("=" * 60)
        print("腾讯云 MPS AIGC 生音频 — 查询任务")
        print("=" * 60)
        print(f"TaskId: {args.task_id}")
        print("-" * 60)
        try:
            result = describe_aigc_audio_task(client, args.task_id)
        except TencentCloudSDKException as exc:
            print(f"❌ 查询失败: {exc}", file=sys.stderr)
            sys.exit(1)
        status = result.get("Status")
        if status == "DONE":
            audio_infos = print_audio_results(result)
            if args.download_dir and audio_infos:
                download_audios(audio_infos, args.download_dir)
        elif status == "FAIL":
            print(f"❌ 任务失败: {result.get('Message')}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"⏳ 任务进行中（状态: {status}），请稍后重试")
        return

    # 模式2：创建任务
    params = build_create_params(args)

    if args.dry_run:
        print("【Dry Run 模式】仅打印请求参数，不实际调用 API")
        print("=" * 60)
        print(json.dumps(params, ensure_ascii=False, indent=2))
        return

    model_info = SUPPORTED_MODELS[args.model]
    print("=" * 60)
    print("腾讯云 MPS AIGC 生音频")
    print("=" * 60)
    print(f"模型: {args.model}（{model_info['description']}）")
    if args.model_version:
        print(f"版本: {args.model_version}")
    print(f"场景: {args.scene_type}")
    if args.prompt:
        display = args.prompt[:80] + "..." if len(args.prompt) > 80 else args.prompt
        print(f"提示词: {display}")
    if args.lyric:
        print("歌词: 已指定")
    if args.instrumental:
        print("纯音乐: 开启（不含人声）")
    if "VideoInfos" in params:
        print("参考视频: 已指定（视频生音效）")
    if "AudioInfos" in params:
        print("参考音频: 已指定")
    if args.output_audio_format:
        print(f"输出格式: {args.output_audio_format}")
    print("-" * 60)

    client = create_mps_client(get_credentials(), region)
    try:
        resp = create_aigc_audio_task(client, params)
    except TencentCloudSDKException as exc:
        print(f"❌ 任务创建失败: {exc}", file=sys.stderr)
        sys.exit(1)

    task_id = resp.TaskId
    print("✅ AIGC 生音频任务提交成功！")
    print(f"   TaskId: {task_id}")
    print(f"   RequestId: {resp.RequestId}")
    print()
    print(f"## TaskId: {task_id}")
    print()

    if args.no_wait:
        print(f"ℹ️  已提交任务，稍后可用以下命令查询结果：")
        print(f"   python3 mps_aigc_audio.py --task-id {task_id}")
        return

    print(f"正在等待任务完成（轮询间隔 {args.poll_interval}s，最长等待 {args.max_wait}s）...")
    result = poll_task_result(client, task_id, args.poll_interval, args.max_wait)
    if result is None:
        sys.exit(1)
    print()

    if result.get("Status") == "FAIL":
        print(f"❌ 任务失败: {result.get('Message')}", file=sys.stderr)
        sys.exit(1)

    audio_infos = print_audio_results(result)
    if args.download_dir and audio_infos:
        download_audios(audio_infos, args.download_dir)


def main():
    parser = argparse.ArgumentParser(
        description="腾讯云 MPS AIGC 生音频（文生音效 / 视频生音效 / 文生音乐 / 歌曲翻唱）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
支持的模型与场景：
  Kling          文生音效 / 视频生音效（--scene-type sfx，无需版本号）
  MiniMaxMusic   文生音乐（版本 2.0 / 2.5 / 2.6 / 3.0，支持 --lyric、--instrumental）
  GL             文生音乐（Google Lyria，版本 3.0-clip / 3.0-pro，支持 --lyric）
  Tme            歌曲翻唱（需 --song-id + --ref-audio-url）

说明：
  - 语音合成（TTS）不在本脚本范围，请使用 mps_dubbing.py
  - 结果默认存于 MPS 临时存储，配置 COS 后写回自有桶并生成 24 小时签名链接
        """
    )

    query_group = parser.add_argument_group("任务查询（与创建任务互斥）")
    query_group.add_argument("--task-id", type=str, help="查询已有任务的 TaskId")

    model_group = parser.add_argument_group("模型与场景")
    model_group.add_argument("--model", type=str, default="Kling",
                             choices=list(SUPPORTED_MODELS.keys()),
                             help="模型名称（默认 Kling）")
    model_group.add_argument("--model-version", type=str,
                             help="模型版本号。MiniMaxMusic: 2.0/2.5/2.6/3.0；"
                                  "GL: 3.0-clip/3.0-pro；Kling / Tme 不需要指定")
    model_group.add_argument("--scene-type", type=str, default=None,
                             choices=SUPPORTED_SCENES,
                             help="场景：sfx（音效，Kling）/ music（音乐，MiniMaxMusic/GL/Tme）。"
                                  "默认按模型自动选择")

    content_group = parser.add_argument_group("生成内容")
    content_group.add_argument("--prompt", type=str,
                               help="音频描述文本（最多 2000 字符）。除 Tme 外必填")
    content_group.add_argument("--lyric", type=str,
                               help="歌词（仅 MiniMaxMusic / GL）。多行用 \\n 分隔")
    content_group.add_argument("--instrumental", action="store_true",
                               help="生成纯音乐（不含人声，仅 MiniMaxMusic）")
    content_group.add_argument("--song-id", type=str,
                               help="已授权的歌曲 ID（仅 Tme 歌曲翻唱，走 ExtraParameters.ResourceId）")

    ref_group = parser.add_argument_group("参考素材")
    ref_group.add_argument("--ref-video-url", type=str,
                           help="参考视频 URL（视频生音效，仅 Kling）。需外网可访问的真实视频")
    ref_group.add_argument("--ref-video-cos-key", type=str,
                           help="参考视频 COS Key（脚本自动生成预签名 URL）")
    ref_group.add_argument("--ref-video-cos-bucket", type=str, help="参考视频所在 COS Bucket")
    ref_group.add_argument("--ref-video-cos-region", type=str, help="参考视频所在 COS Region")
    ref_group.add_argument("--ref-audio-url", type=str,
                           help="参考音频 URL（歌曲翻唱等场景）。需外网可访问")
    ref_group.add_argument("--ref-audio-cos-key", type=str,
                           help="参考音频 COS Key（脚本自动生成预签名 URL）")
    ref_group.add_argument("--ref-audio-cos-bucket", type=str, help="参考音频所在 COS Bucket")
    ref_group.add_argument("--ref-audio-cos-region", type=str, help="参考音频所在 COS Region")

    output_group = parser.add_argument_group("输出配置")
    output_group.add_argument("--output-audio-format", type=str, choices=["mp3", "wav"],
                              help="输出音频格式（默认由模型决定）")
    output_group.add_argument("--additional-parameters", type=str,
                              help="附加参数（JSON 字符串），与 --lyric/--instrumental 合并")
    output_group.add_argument("--download-dir", type=str,
                              help="任务完成后将音频下载到指定目录（默认仅打印链接）")

    cos_group = parser.add_argument_group(
        "COS 存储配置（可选；不配置则用 MPS 临时存储，配置后写回自有桶并生成 24 小时签名链接）")
    cos_group.add_argument("--cos-bucket-name", type=str,
                           help="COS Bucket 名称（默认取 TENCENTCLOUD_COS_BUCKET）")
    cos_group.add_argument("--cos-bucket-region", type=str,
                           help="COS Bucket 区域（默认取 TENCENTCLOUD_COS_REGION）")
    cos_group.add_argument("--cos-bucket-path", type=str, default="/output/aigc-audio/",
                           help="COS 输出目录路径（默认 /output/aigc-audio/）")

    control_group = parser.add_argument_group("执行控制")
    control_group.add_argument("--no-wait", action="store_true",
                               help="仅创建任务，不等待结果")
    control_group.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
                               help=f"轮询间隔（秒），默认 {DEFAULT_POLL_INTERVAL}")
    control_group.add_argument("--max-wait", type=int, default=DEFAULT_MAX_WAIT,
                               help=f"最长等待时间（秒），默认 {DEFAULT_MAX_WAIT}（音乐生成较慢）")
    control_group.add_argument("--operator", type=str, help="操作者名称")

    other_group = parser.add_argument_group("其他配置")
    other_group.add_argument("--region", type=str, help="MPS 服务区域（默认 ap-guangzhou）")
    other_group.add_argument("--dry-run", action="store_true",
                             help="仅打印请求参数，不实际调用 API")

    args = parser.parse_args()

    # 场景默认值按模型推导：Kling→sfx，音乐类模型→music
    if args.scene_type is None:
        args.scene_type = SUPPORTED_MODELS[args.model]["scenes"][0]

    validate_args(args, parser)
    run(args)


if __name__ == "__main__":
    main()
