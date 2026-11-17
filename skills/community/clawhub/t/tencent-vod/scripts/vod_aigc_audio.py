#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD AIGC 生音频任务脚本
使用 CreateAigcAudioTask API 创建 AIGC 生音频任务
支持能力：
  - 文生音效 / 视频生音效（Kling，SceneType=sfx）
  - 文生音乐（MiniMaxMusic / GL(Google Lyria)，SceneType=music）
"""

import os
import sys
import json
import argparse
import time

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
    print("错误：请先安装腾讯云 SDK: python3 -m pip install tencentcloud-sdk-python")
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
    # 检查所有必需变量（SECRET_ID/KEY/SUB_APP_ID）
    if _LOAD_ENV_AVAILABLE:
        from vod_load_env import check_required_vars, _print_setup_hint
        missing = check_required_vars()
        if missing:
            _print_setup_hint(missing)
            sys.exit(1)
    elif not secret_id or not secret_key:
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

# ── 模型/场景映射（文档 3.13.1 ②模型说明） ──────────────────────────────
# 模块        模型(ModelName)  版本(ModelVersion)      场景(SceneType)
# 文生音效     Kling            空（不填）              sfx
# 视频生音效   Kling            空（不填）              sfx
# 文生音乐     MiniMaxMusic     2.0/2.5/2.6/3.0        music
# 文生音乐     GL               3.0-clip/3.0-pro       music
MODEL_VERSIONS = {
    "Kling": [],  # ModelVersion 留空，使用系统默认稳定版本
    "MiniMaxMusic": ["2.0", "2.5", "2.6", "3.0"],
    "GL": ["3.0-clip", "3.0-pro"],
}

# 各模型对应的合法 SceneType（用于校验，避免传错场景导致接口报错）
MODEL_SCENE_TYPES = {
    "Kling": ["sfx"],
    "MiniMaxMusic": ["music"],
    "GL": ["music"],
}

def validate_model_scene(args):
    """校验 ModelName 与 SceneType 的搭配是否合法（文档 3.13.1 ②模型说明）。"""
    if not args.model:
        return
    valid_scenes = MODEL_SCENE_TYPES.get(args.model)
    if valid_scenes is None:
        return
    if args.scene_type and args.scene_type not in valid_scenes:
        print(f"错误：模型 {args.model} 不支持场景 {args.scene_type}，"
              f"可用场景: {valid_scenes}")
        sys.exit(1)
    if args.model in ("MiniMaxMusic", "GL") and args.model_version:
        allowed = MODEL_VERSIONS.get(args.model, [])
        if allowed and args.model_version not in allowed:
            print(f"错误：模型 {args.model} 不支持版本 {args.model_version}，"
                  f"可用版本: {allowed}")
            sys.exit(1)
    if args.model == "Kling" and args.model_version:
        print("提示：Kling 音效/音乐场景 ModelVersion 建议留空（使用系统默认稳定版本），"
              "文档示例中该字段为空")

def create_audio_task(args):
    """创建 AIGC 生音频任务（CreateAigcAudioTask）"""
    client = get_client(args.region)

    validate_model_scene(args)

    req = models.CreateAigcAudioTaskRequest()

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id

    if args.model:
        req.ModelName = args.model
    if args.model_version:
        req.ModelVersion = args.model_version
    if args.scene_type:
        req.SceneType = args.scene_type
    if args.prompt:
        req.Prompt = args.prompt

    # 参考视频信息（VideoInfos，视频生音效场景使用）
    if args.video_id or args.video_url:
        video_info = models.AigcAudioReferenceVideoInfo()
        if args.video_id:
            video_info.Type = "File"
            video_info.FileId = args.video_id
        elif args.video_url:
            video_info.Type = "Url"
            video_info.Url = args.video_url
        req.VideoInfos = [video_info]
    elif args.video_infos:
        try:
            video_infos_data = json.loads(args.video_infos)
            video_infos = []
            for vi in video_infos_data:
                video_info = models.AigcAudioReferenceVideoInfo()
                video_info.Type = vi.get("Type", "Url")
                if vi.get("FileId"):
                    video_info.FileId = vi["FileId"]
                if vi.get("Url"):
                    video_info.Url = vi["Url"]
                video_infos.append(video_info)
            req.VideoInfos = video_infos
        except json.JSONDecodeError as e:
            print(f"错误：--video-infos 参数 JSON 格式不正确: {e}")
            sys.exit(1)

    # 参考音频信息（AudioInfos，传入音频生成音乐等场景使用）
    if args.audio_id or args.audio_url:
        audio_info = models.AigcAudioReferenceAudioInfo()
        if args.audio_id:
            audio_info.Type = "File"
            audio_info.FileId = args.audio_id
        elif args.audio_url:
            audio_info.Type = "Url"
            audio_info.Url = args.audio_url
        req.AudioInfos = [audio_info]
    elif args.audio_infos:
        try:
            audio_infos_data = json.loads(args.audio_infos)
            audio_infos = []
            for ai in audio_infos_data:
                audio_info = models.AigcAudioReferenceAudioInfo()
                audio_info.Type = ai.get("Type", "Url")
                if ai.get("FileId"):
                    audio_info.FileId = ai["FileId"]
                if ai.get("Url"):
                    audio_info.Url = ai["Url"]
                audio_infos.append(audio_info)
            req.AudioInfos = audio_infos
        except json.JSONDecodeError as e:
            print(f"错误：--audio-infos 参数 JSON 格式不正确: {e}")
            sys.exit(1)

    # 输出配置（OutputConfig）
    if any([args.output_storage_mode, args.output_media_name, args.output_class_id,
            args.output_expire_time, args.output_duration is not None, args.output_audio_format]):
        output_config = models.AigcAudioOutputConfig()
        if args.output_storage_mode:
            output_config.StorageMode = args.output_storage_mode
        if args.output_media_name:
            output_config.MediaName = args.output_media_name
        if args.output_class_id is not None:
            output_config.ClassId = args.output_class_id
        if args.output_expire_time:
            output_config.ExpireTime = args.output_expire_time
        if args.output_duration is not None:
            output_config.Duration = args.output_duration
        if args.output_audio_format:
            output_config.OutputAudioFormat = args.output_audio_format
        req.OutputConfig = output_config

    # AdditionalParameters 构建
    # 优先级：--bgm-prompt/--asmr-mode/--lyrics（专用便捷参数，会合并进同一个 JSON）
    #        > --additional-parameters（用户直接透传的原始 JSON，会与专用参数合并，专用参数优先）
    additional = {}
    if args.additional_parameters:
        try:
            additional.update(json.loads(args.additional_parameters))
        except json.JSONDecodeError as e:
            print(f"错误：--additional-parameters 参数 JSON 格式不正确: {e}")
            sys.exit(1)
    if args.bgm_prompt:
        additional["bgm_prompt"] = args.bgm_prompt
    if args.asmr_mode:
        additional["asmr_mode"] = args.asmr_mode == "true"
    if args.lyrics:
        additional["lyrics"] = args.lyrics

    if additional:
        req.AdditionalParameters = json.dumps(additional, ensure_ascii=False)

    if args.dry_run:
        print("[DRY RUN] 请求参数:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return

    try:
        resp = client.CreateAigcAudioTask(req)
        result = json.loads(resp.to_json_string())

        print("AIGC 生音频任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python3 scripts/vod_describe_task.py --task-id {result['TaskId']}")
            else:
                print_task_outputs(wait_result)

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"创建生音频任务失败: {e}")
        sys.exit(1)

def print_task_outputs(result):
    """从任务返回结果中提取并打印产物（音频/视频 URL 或 FileId）。

    兼容两种返回结构：
    - DescribeTaskDetail 返回的 root（含 AigcAudioTask 子对象）
    - 已展开的 AigcAudioTask 对象本身
    """
    if not result:
        return
    task = result.get('AigcAudioTask') or result
    output = task.get('Output') or {}
    audio_infos = output.get('AudioInfos') or []
    video_infos = output.get('VideoInfos') or []

    if not audio_infos and not video_infos:
        err_msg = task.get('Message') or task.get('ErrCodeExt')
        if err_msg:
            print(f"⚠️  错误信息: {err_msg}")
        return

    if audio_infos:
        print(f"\n🎵 音频产物（{len(audio_infos)} 个文件）:")
        for i, fi in enumerate(audio_infos, 1):
            _print_output_file_info(fi, i, len(audio_infos))

    if video_infos:
        print(f"\n🎬 视频产物（{len(video_infos)} 个文件）:")
        for i, fi in enumerate(video_infos, 1):
            _print_output_file_info(fi, i, len(video_infos))

def _print_output_file_info(fi, index, total):
    """打印单个产物文件信息（FileUrl/FileId/Duration）。"""
    url = fi.get('FileUrl') or ''
    fid = fi.get('FileId') or ''
    duration = fi.get('Duration')
    prefix = f"  [{index}]" if total > 1 else "  •"
    if fid:
        print(f"{prefix} FileId : {fid}")
        print(f"     URL    : {url}")
    else:
        print(f"{prefix} URL: {url}")
    if duration:
        print(f"     时长   : {duration}s")

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

            status = result.get('Status', 'PROCESSING')
            print(f"  当前状态: {status}")

            if status == 'FINISH':
                print("任务完成!")
                return result
            elif status == 'FAIL':
                print("任务失败!")
                return result

            time.sleep(5)
        # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
        except Exception as e:
            print(f"查询任务状态失败: {e}")
            time.sleep(5)

    print(f"⏱️ 等待超时（{max_wait}秒），任务仍在执行中")
    return None

def list_models(args):
    """列出支持的模型和场景"""
    print("支持的模型和版本:")
    print("  Kling: ModelVersion 留空（使用系统默认稳定版本）")
    print(f"  MiniMaxMusic: 版本 {MODEL_VERSIONS['MiniMaxMusic']}")
    print(f"  GL: 版本 {MODEL_VERSIONS['GL']}")
    print("\n场景类型（SceneType）与模型对应关系:")
    print("  sfx（音效，文生音效/视频生音效）: Kling")
    print("  music（音乐，文生音乐）        : MiniMaxMusic, GL")

def main():
    # 先加载 .env，确保 argparse `default=os.environ.get(...)` 求值前环境变量已就绪
    if _LOAD_ENV_AVAILABLE:
        try:
            _ensure_env_loaded(verbose=False)
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description='VOD AIGC 生音频任务工具（CreateAigcAudioTask）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 文生音效（Kling，SceneType=sfx）
  python3 vod_aigc_audio.py create --model Kling --scene-type sfx \\
      --prompt "春节庆祝时的烟花声" --output-duration 6 \\
      --output-storage-mode Temporary

  # 视频生音效（Kling，参考视频 URL，附带配乐 + ASMR 模式）
  python3 vod_aigc_audio.py create --model Kling --scene-type sfx \\
      --video-url "https://example.com/ref.mp4" \\
      --prompt "温柔的风声，远处鸟鸣，偶尔的脚步声，翻书声，雨滴打在窗玻璃上的声音" \\
      --bgm-prompt "治愈系钢琴曲，轻柔的弦乐伴奏，温暖舒缓的旋律" \\
      --asmr-mode true \\
      --output-duration 6

  # 文生音乐（MiniMaxMusic，带歌词）
  python3 vod_aigc_audio.py create --model MiniMaxMusic --model-version 2.0 \\
      --scene-type music --prompt "一首欢乐的歌" \\
      --lyrics "大海啊，全是水，骏马啊，四条腿" \\
      --output-audio-format mp3

  # 文生音乐（GL/Google Lyria，风格+歌词需拼接进 prompt）
  python3 vod_aigc_audio.py create --model GL --model-version 3.0-clip \\
      --scene-type music \\
      --prompt "轻快民谣风格\\n\\nLyrics:\\n大海啊，全是水，骏马啊，四条腿" \\
      --output-audio-format mp3

  # 列出支持的模型
  python3 vod_aigc_audio.py models

  # 预览请求参数
  python3 vod_aigc_audio.py create --model Kling --scene-type sfx --prompt "test" --dry-run
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # ---- create 子命令 ----
    create_parser = subparsers.add_parser('create', help='创建 AIGC 生音频任务')

    create_parser.add_argument('--model', choices=list(MODEL_VERSIONS.keys()),
                               help='模型名称：Kling（音效）/MiniMaxMusic/GL（音乐）')
    create_parser.add_argument('--model-version',
                               help='模型版本；Kling 建议留空（使用系统默认稳定版本），'
                                    'MiniMaxMusic 支持 2.0/2.5/2.6/3.0，GL 支持 3.0-clip/3.0-pro')
    create_parser.add_argument('--scene-type', choices=['sfx', 'music'],
                               help='场景类型：sfx（音效，Kling）/music（音乐，MiniMaxMusic/GL）')
    create_parser.add_argument('--prompt', help='生成音频的描述（提示词）')

    # 参考视频（视频生音效场景）
    create_parser.add_argument('--video-id', help='参考视频的 VOD 文件 FileId（视频生音效场景）')
    create_parser.add_argument('--video-url', help='参考视频的 URL（视频生音效场景）')
    create_parser.add_argument('--video-infos',
                               help='多个参考视频的 JSON 数组，格式：[{"Type":"Url","Url":"..."}]')

    # 参考音频（传入音频生成音乐等场景）
    create_parser.add_argument('--audio-id', help='参考音频的 VOD 文件 FileId')
    create_parser.add_argument('--audio-url', help='参考音频的 URL')
    create_parser.add_argument('--audio-infos',
                               help='多个参考音频的 JSON 数组，格式：[{"Type":"Url","Url":"..."}]')

    # AdditionalParameters 便捷参数（视频生音效/文生音乐常用字段）
    create_parser.add_argument('--bgm-prompt', help='配乐生成提示词（视频生音效场景，Kling），并入 AdditionalParameters')
    create_parser.add_argument('--asmr-mode', choices=['true', 'false'],
                               help='是否开启 ASMR 模式（增强细节音效，适合高沉浸内容场景），并入 AdditionalParameters')
    create_parser.add_argument('--lyrics', help='歌词内容（文生音乐场景，MiniMaxMusic），并入 AdditionalParameters')
    create_parser.add_argument('--additional-parameters',
                               help='保留字段，特殊场景参数 JSON 字符串，例如 {"camera_control":{"type":"simple"}}；'
                                    '会与 --bgm-prompt/--asmr-mode/--lyrics 合并（后者优先）')

    # 输出配置
    create_parser.add_argument('--output-storage-mode', choices=['Permanent', 'Temporary'],
                               help='存储模式：Permanent（永久）/ Temporary（临时，默认）')
    create_parser.add_argument('--output-media-name', help='输出文件名，最长 64 字符')
    create_parser.add_argument('--output-class-id', type=int, help='输出文件分类 ID，默认 0')
    create_parser.add_argument('--output-expire-time', help='输出文件过期时间，ISO 8601 格式')
    create_parser.add_argument('--output-duration', type=int,
                               help='生成音频的时长（秒），取值范围 [0, 60]，默认不填')
    create_parser.add_argument('--output-audio-format', help='输出音频格式，如 wav、mp3，默认不填')

    create_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                               help='子应用 ID，2023-12-25 后开通点播的客户必填')
    create_parser.add_argument('--region', default=os.getenv('TENCENTCLOUD_REGION', 'ap-guangzhou'), help='地域，默认 ap-guangzhou')
    create_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    create_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)，默认 600')
    create_parser.add_argument('--json', action='store_true', help='JSON 格式输出完整响应')
    create_parser.add_argument('--dry-run', action='store_true', help='预览请求参数，不实际执行')

    # ---- models 子命令 ----
    _ = subparsers.add_parser('models', help='列出支持的模型和场景')

    args = parser.parse_args()

    if args.command == 'create':
        create_audio_task(args)
    elif args.command == 'models':
        list_models(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
