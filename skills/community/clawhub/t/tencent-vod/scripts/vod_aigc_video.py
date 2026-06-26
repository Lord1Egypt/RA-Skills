#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD AIGC 生视频任务脚本
使用 CreateAigcVideoTask API 创建 AIGC 生视频任务
支持模型：GV、Hailuo（海螺）、Kling（可灵）、Jimeng（即梦）、Vidu、Hunyuan（混元）、Mingmou（明眸）、OS
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


# 模型版本映射
MODEL_VERSIONS = {
    "GV": ["3.1", "3.1-fast"],
    "Hailuo": ["02", "2.3", "2.3-fast"],
    "Kling": ["1.6", "2.0", "2.1", "2.5", "O1", "3.0-Omni"],
    "Jimeng": ["3.0pro"],
    "Vidu": ["q2", "q2-pro", "q2-turbo", "q3-pro", "q3-turbo"],
    "Hunyuan": ["1.5"],
    "Mingmou": ["1.0"],
    "OS": ["2.0"],
}

MODEL_DEFAULT_VERSION = {
    "GV": "3.1",
    "Hailuo": "2.3",
    "Kling": "2.1",
    "Jimeng": "3.0pro",
    "Vidu": "q2",
    "Hunyuan": "1.5",
    "Mingmou": "1.0",
    "OS": "2.0",
}


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def create_video_task(args):
    """创建 AIGC 生视频任务"""
    client = get_client(args.region)

    req = models.CreateAigcVideoTaskRequest()

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id

    # 模型名称和版本（必填）
    req.ModelName = args.model
    if args.model_version:
        req.ModelVersion = args.model_version
    else:
        req.ModelVersion = MODEL_DEFAULT_VERSION.get(args.model, "")
        if not req.ModelVersion:
            print(f"错误：未知模型 {args.model}，可用模型: {list(MODEL_DEFAULT_VERSION.keys())}")
            sys.exit(1)

    # 提示词
    if args.prompt:
        req.Prompt = args.prompt

    if args.negative_prompt:
        req.NegativePrompt = args.negative_prompt

    if args.enhance_prompt:
        req.EnhancePrompt = args.enhance_prompt

    # 输入文件信息（参考图/首帧）
    if args.file_id or args.file_url:
        file_info = models.AigcVideoTaskInputFileInfo()
        if args.file_id:
            file_info.Type = "File"
            file_info.FileId = args.file_id
        elif args.file_url:
            file_info.Type = "Url"
            file_info.Url = args.file_url
        req.FileInfos = [file_info]
    elif args.file_infos:
        try:
            file_infos_data = json.loads(args.file_infos)
            file_infos = []
            for fi in file_infos_data:
                file_info = models.AigcVideoTaskInputFileInfo()
                file_info.Type = fi.get("Type", "Url")
                if fi.get("FileId"):
                    file_info.FileId = fi["FileId"]
                if fi.get("Url"):
                    file_info.Url = fi["Url"]
                if fi.get("ObjectId"):
                    file_info.ObjectId = fi["ObjectId"]
                file_infos.append(file_info)
            req.FileInfos = file_infos
        except json.JSONDecodeError as e:
            print(f"错误：--file-infos 参数 JSON 格式不正确: {e}")
            sys.exit(1)

    # 固定主体输入信息（SubjectInfos - SDK 中可能不支持，跳过）
    # if args.subject_infos: ...（SDK 暂不支持此字段）

    # 尾帧（首尾帧生视频）
    if args.last_frame_file_id:
        req.LastFrameFileId = args.last_frame_file_id
    if args.last_frame_url:
        req.LastFrameUrl = args.last_frame_url

    # 场景类型
    if args.scene_type:
        req.SceneType = args.scene_type

    # 输出配置
    if any([args.output_storage_mode, args.output_media_name, args.output_class_id,
            args.output_expire_time, args.output_resolution, args.output_duration,
            args.output_aspect_ratio, args.output_audio_generation, args.output_person_generation,
            args.output_enhance_switch, args.output_off_peak, args.output_frame_interpolate,
            args.output_logo_add, args.input_compliance_check, args.output_compliance_check]):
        output_config = models.AigcVideoOutputConfig()
        if args.output_storage_mode:
            output_config.StorageMode = args.output_storage_mode
        if args.output_media_name:
            output_config.MediaName = args.output_media_name
        if args.output_class_id is not None:
            output_config.ClassId = args.output_class_id
        if args.output_expire_time:
            output_config.ExpireTime = args.output_expire_time
        if args.output_resolution:
            output_config.Resolution = args.output_resolution
        if args.output_duration:
            output_config.Duration = args.output_duration
        if args.output_aspect_ratio:
            output_config.AspectRatio = args.output_aspect_ratio
        if args.output_audio_generation:
            output_config.AudioGeneration = args.output_audio_generation
        if args.output_person_generation:
            output_config.PersonGeneration = args.output_person_generation
        if args.output_enhance_switch:
            output_config.EnhanceSwitch = args.output_enhance_switch
        if args.output_off_peak:
            output_config.OffPeak = args.output_off_peak
        if args.output_frame_interpolate:
            output_config.FrameInterpolate = args.output_frame_interpolate
        if args.output_logo_add:
            output_config.LogoAdd = args.output_logo_add
        if args.input_compliance_check:
            output_config.InputComplianceCheck = args.input_compliance_check
        if args.output_compliance_check:
            output_config.OutputComplianceCheck = args.output_compliance_check
        req.OutputConfig = output_config

    if args.procedure:
        req.Procedure = args.procedure
    if args.seed is not None:
        req.Seed = args.seed
    if args.input_region:
        req.InputRegion = args.input_region
    if args.session_id:
        req.SessionId = args.session_id
    if args.session_context:
        req.SessionContext = args.session_context
    if args.tasks_priority is not None:
        req.TasksPriority = args.tasks_priority

    # ── ExtInfo 构建 ──────────────────────────────────────────────────────────
    # 优先级：--element-ids / --elements-file > --ext-info
    # 格式：ExtInfo = json.dumps({"AdditionalParameters": json.dumps({"element_list": [{"element_id": ...}]})})
    ext_info_val = None

    element_ids = []

    if args.element_ids:
        # --element-ids 支持逗号分隔的整数列表
        try:
            element_ids = [int(eid.strip()) for eid in args.element_ids.split(",") if eid.strip()]
        except ValueError as e:
            print(f"错误：--element-ids 格式不正确，应为逗号分隔的整数，如 865750283577090106: {e}")
            sys.exit(1)

    if not element_ids and args.elements_file:
        # 从 elements.json 文件读取所有 ElementId
        ef_path = args.elements_file
        if not os.path.isabs(ef_path):
            # 相对路径：相对于脚本目录的父目录（skill 根目录）
            ef_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                ef_path,
            )
        try:
            with open(ef_path, "r", encoding="utf-8") as f:
                elements_data = json.load(f)
            if isinstance(elements_data, list):
                element_ids = [int(item["ElementId"]) for item in elements_data if item.get("ElementId")]
            elif isinstance(elements_data, dict):
                element_ids = [int(v["ElementId"]) for v in elements_data.values() if v.get("ElementId")]
            print(f"从 {ef_path} 读取到 {len(element_ids)} 个主体 ElementId: {element_ids}")
        except FileNotFoundError:
            print(f"错误：主体文件不存在: {ef_path}")
            sys.exit(1)
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            print(f"错误：读取主体文件失败: {e}")
            sys.exit(1)

    if element_ids:
        # 构建嵌套 JSON 字符串
        # ExtInfo = '{"AdditionalParameters": "{\"element_list\": [{\"element_id\": 123}]}"}'
        element_list = [{"element_id": eid} for eid in element_ids]
        additional_params = json.dumps({"element_list": element_list}, ensure_ascii=False)
        ext_info_val = json.dumps({"AdditionalParameters": additional_params}, ensure_ascii=False)
        print(f"  使用主体 element_list: {element_ids}")
        print(f"  ExtInfo: {ext_info_val}")
    elif args.ext_info:
        ext_info_val = args.ext_info

    if ext_info_val:
        req.ExtInfo = ext_info_val

    if args.dry_run:
        print("[DRY RUN] 请求参数:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return

    try:
        resp = client.CreateAigcVideoTask(req)
        result = json.loads(resp.to_json_string())

        print(f"AIGC 生视频任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"创建生视频任务失败: {e}")
        sys.exit(1)


def wait_for_task(client, task_id, sub_app_id=None, max_wait=1800):
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

            time.sleep(15)
        # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
        except Exception as e:
            print(f"查询任务状态失败: {e}")
            time.sleep(15)

    print(f"⏱️ 等待超时（{max_wait}秒），任务仍在执行中")
    return None


def list_models(args):
    """列出支持的模型"""
    print("支持的模型和版本:")
    for model, versions in MODEL_VERSIONS.items():
        default = MODEL_DEFAULT_VERSION[model]
        print(f"  {model}: 版本 {versions}（默认 {default}）")
    print("\n场景类型（SceneType）:")
    print("  Kling 模型: motion_control（动作控制）、avatar_i2v（数字人）、lip_sync（对口型）")
    print("  Vidu 模型: template_effect（特效模板）, subject_reference（主体参考）")


def main():
    parser = argparse.ArgumentParser(
        description='VOD AIGC 生视频任务工具（CreateAigcVideoTask）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 文生视频（使用 GV 模型）
  python vod_aigc_video.py create --model GV --prompt "一只小狗在草地上奔跑"

  # 图生视频（指定参考图 FileId）
  python vod_aigc_video.py create --model Kling --model-version 2.1 \\
      --file-id 528548548798527148 --prompt "让图片中的人物走动起来"

  # 图生视频（指定参考图 URL）
  python vod_aigc_video.py create --model Vidu --model-version q2 \\
      --file-url "https://example.com/ref.jpg" --prompt "camera panning left"

  # 首尾帧生视频
  python vod_aigc_video.py create --model GV \\
      --file-url "https://example.com/first.jpg" \\
      --last-frame-url "https://example.com/last.jpg" \\
      --prompt "smooth transition"

  # 设置输出配置（永久存储，指定分辨率和时长）
  python vod_aigc_video.py create --model Hailuo --prompt "风景视频" \\
      --output-storage-mode Permanent --output-resolution 1080P --output-duration 5

  # 使用场景类型（Kling 数字人）
  python vod_aigc_video.py create --model Kling --model-version 2.1 \\
      --file-id 528548548798527148 --scene-type avatar_i2v

  # 使用自定义主体（Kling 3.0-Omni/O1，直接指定 ElementId）
  python vod_aigc_video.py create --model Kling --model-version 3.0-Omni \\
      --prompt "<<<element_1>>>跳舞" \\
      --element-ids 865750283577090106

  # 使用自定义主体（从 elements.json 自动读取所有主体）
  python vod_aigc_video.py create --model Kling --model-version 3.0-Omni \\
      --prompt "<<<element_1>>>跳舞" \\
      --elements-file mem/elements.json

  # 默认等待任务完成（生视频耗时较长，已设置默认 --max-wait 1800）
  python vod_aigc_video.py create --model GV --prompt "一只猫"
  
  # 不等待，仅提交任务
  python vod_aigc_video.py create --model GV --prompt "一只猫" --no-wait

  # 列出支持的模型
  python vod_aigc_video.py models

  # 预览请求参数
  python vod_aigc_video.py create --model GV --prompt "test" --dry-run
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # ---- create 子命令 ----
    create_parser = subparsers.add_parser('create', help='创建 AIGC 生视频任务')

    # 模型参数（必填）
    create_parser.add_argument('--model', required=True,
                               choices=list(MODEL_VERSIONS.keys()),
                               help='模型名称（必填）：GV/Hailuo/Kling/Jimeng/Vidu/Hunyuan/Mingmou/OS')
    create_parser.add_argument('--model-version', help='模型版本，不填则使用默认版本')

    # 内容参数
    create_parser.add_argument('--prompt', help='生成视频的提示词（当无输入文件时必填）')
    create_parser.add_argument('--negative-prompt', help='负面提示词，阻止模型生成的内容')
    create_parser.add_argument('--enhance-prompt', choices=['Enabled', 'Disabled'],
                               help='是否自动优化提示词：Enabled/Disabled')

    # 输入文件（参考图/首帧）
    create_parser.add_argument('--file-id', help='参考图/首帧的 VOD 文件 FileId')
    create_parser.add_argument('--file-url', help='参考图/首帧的 URL')
    create_parser.add_argument('--file-infos',
                               help='多个参考图的 JSON 数组，格式：[{"Type":"Url","Url":"..."}]')

    # 固定主体
    create_parser.add_argument('--subject-infos',
                               help='固定主体 JSON 数组，格式：[{"Id":"...","Name":"..."}]')

    # 尾帧（首尾帧生视频）
    create_parser.add_argument('--last-frame-file-id', help='尾帧图片的 VOD 文件 FileId（仅 GV/Kling/Vidu 支持）')
    create_parser.add_argument('--last-frame-url', help='尾帧图片的 URL（仅 GV/Kling/Vidu 支持）')

    # 场景类型
    create_parser.add_argument('--scene-type',
                               help='场景类型：Kling 支持 motion_control/avatar_i2v/lip_sync；Vidu 支持 template_effect/subject_reference')

    # 输出配置
    create_parser.add_argument('--output-storage-mode', choices=['Permanent', 'Temporary'],
                               help='存储模式：Permanent（永久）/ Temporary（临时，默认）')
    create_parser.add_argument('--output-media-name', help='输出文件名，最长 64 字符')
    create_parser.add_argument('--output-class-id', type=int, help='输出文件分类 ID，默认 0')
    create_parser.add_argument('--output-expire-time', help='输出文件过期时间，ISO 8601 格式')
    create_parser.add_argument('--output-resolution', help='生成视频分辨率，如 720P/1080P/2K/4K')
    create_parser.add_argument('--output-duration', type=int, help='生成视频时长（秒）')
    create_parser.add_argument('--output-aspect-ratio', help='视频宽高比，如 16:9、9:16、1:1')
    create_parser.add_argument('--output-audio-generation', choices=['Enabled', 'Disabled'],
                               help='是否生成音频（GV/OS/Vidu 支持）：Enabled/Disabled，默认 Disabled')
    create_parser.add_argument('--output-person-generation', choices=['AllowAdult', 'Disallowed'],
                               help='是否允许人物/人脸生成：AllowAdult/Disallowed')
    create_parser.add_argument('--output-enhance-switch', choices=['Enabled', 'Disabled'],
                               help='是否启用视频增强（分辨率超过模型直出时默认启用）：Enabled/Disabled')
    create_parser.add_argument('--output-off-peak', choices=['Enabled', 'Disabled'],
                               help='是否开启错峰：Enabled/Disabled')
    create_parser.add_argument('--output-frame-interpolate', choices=['Enabled', 'Disabled'],
                               help='是否开启 Vidu 智能插帧：Enabled/Disabled')
    create_parser.add_argument('--output-logo-add', choices=['Enabled', 'Disabled'],
                               help='是否开启图标水印（Vidu 支持）：Enabled/Disabled')
    create_parser.add_argument('--input-compliance-check', choices=['Enabled', 'Disabled'],
                               help='是否开启输入内容合规检查')
    create_parser.add_argument('--output-compliance-check', choices=['Enabled', 'Disabled'],
                               help='是否开启输出内容合规检查')

    # 其他参数
    create_parser.add_argument('--procedure', help='任务流名称，生成视频后自动执行指定任务流')
    create_parser.add_argument('--seed', type=int, help='模型随机种子')
    create_parser.add_argument('--input-region', choices=['Mainland', 'Oversea'],
                               help='输入文件区域：Mainland（默认）/ Oversea（国外地址时使用）')
    create_parser.add_argument('--session-id', help='去重识别码，三天内相同 ID 返回错误，最长 50 字符')
    create_parser.add_argument('--session-context', help='来源上下文，透传用户请求信息，最长 1000 字符')
    create_parser.add_argument('--tasks-priority', type=int, help='任务优先级，范围 -10 到 10，默认 0')
    create_parser.add_argument('--element-ids',
                               help='主体 ElementId 列表（逗号分隔整数），仅 Kling 3.0-Omni/O1 支持，'
                                    '例如: 865750283577090106,865750283577090107')
    create_parser.add_argument('--elements-file',
                               help='从 elements.json 文件读取主体 ElementId，支持相对路径（相对 skill 根目录）'
                                    '或绝对路径，例如: mem/elements.json')
    create_parser.add_argument('--ext-info', help='保留字段，特殊用途时使用（与 --element-ids 互斥，优先级更低）')
    create_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                               help='子应用 ID，2023-12-25 后开通点播的客户必填')
    create_parser.add_argument('--region', default='ap-guangzhou', help='地域，默认 ap-guangzhou')
    create_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    create_parser.add_argument('--max-wait', type=int, default=1800, help='最大等待时间(秒)，默认 1800')
    create_parser.add_argument('--json', action='store_true', help='JSON 格式输出完整响应')
    create_parser.add_argument('--dry-run', action='store_true', help='预览请求参数，不实际执行')

    # ---- models 子命令 ----
    _ = subparsers.add_parser('models', help='列出支持的模型和版本')

    args = parser.parse_args()

    if args.command == 'create':
        create_video_task(args)
    elif args.command == 'models':
        list_models(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
