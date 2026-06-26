#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD AIGC 生图任务脚本
使用 CreateAigcImageTask API 创建 AIGC 生图任务
支持模型：Hunyuan（混元）、Qwen（千问）、Vidu（生数）、Kling（可灵）、MJ（Midjourney）、GEM
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
    "Qwen": ["0925"],
    "Hunyuan": ["3.0"],
    "Vidu": ["q2"],
    "Kling": ["2.1", "3.0", "3.0-Omni"],
    "MJ": ["v7"],
    "GEM": ["2.5", "3.0"],
}

# 模型默认版本
MODEL_DEFAULT_VERSION = {
    "Qwen": "0925",
    "Hunyuan": "3.0",
    "Vidu": "q2",
    "Kling": "2.1",
    "MJ": "v7",
    "GEM": "2.5",
}


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def create_image_task(args):
    """创建 AIGC 生图任务"""
    client = get_client(args.region)

    req = models.CreateAigcImageTaskRequest()

    if args.sub_app_id:
        req.SubAppId = args.sub_app_id

    # 模型名称和版本（必填）
    req.ModelName = args.model
    if args.model_version:
        req.ModelVersion = args.model_version
    else:
        # 使用默认版本
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

    # 输入文件信息（参考图）
    if args.file_id or args.file_url:
        file_info = models.AigcImageTaskInputFileInfo()
        if args.file_id:
            file_info.Type = "File"
            file_info.FileId = args.file_id
        elif args.file_url:
            file_info.Type = "Url"
            file_info.Url = args.file_url
        if args.file_text:
            file_info.Text = args.file_text
        req.FileInfos = [file_info]
    elif args.file_infos:
        # 支持 JSON 格式多个文件信息
        try:
            file_infos_data = json.loads(args.file_infos)
            file_infos = []
            for fi in file_infos_data:
                file_info = models.AigcImageTaskInputFileInfo()
                file_info.Type = fi.get("Type", "Url")
                if fi.get("FileId"):
                    file_info.FileId = fi["FileId"]
                if fi.get("Url"):
                    file_info.Url = fi["Url"]
                if fi.get("Text"):
                    file_info.Text = fi["Text"]
                file_infos.append(file_info)
            req.FileInfos = file_infos
        except json.JSONDecodeError as e:
            print(f"错误：--file-infos 参数 JSON 格式不正确: {e}")
            sys.exit(1)

    # 输出配置
    if any([args.output_storage_mode, args.output_media_name, args.output_class_id,
            args.output_expire_time, args.output_resolution, args.output_aspect_ratio,
            args.output_person_generation, args.input_compliance_check, args.output_compliance_check]):
        output_config = models.AigcImageOutputConfig()
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
        if args.output_aspect_ratio:
            output_config.AspectRatio = args.output_aspect_ratio
        if args.output_person_generation:
            output_config.PersonGeneration = args.output_person_generation
        if args.input_compliance_check:
            output_config.InputComplianceCheck = args.input_compliance_check
        if args.output_compliance_check:
            output_config.OutputComplianceCheck = args.output_compliance_check
        req.OutputConfig = output_config

    if args.scene_type:
        req.SceneType = args.scene_type
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
    if args.ext_info:
        req.ExtInfo = args.ext_info

    if args.dry_run:
        print("[DRY RUN] 请求参数:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return

    try:
        resp = client.CreateAigcImageTask(req)
        result = json.loads(resp.to_json_string())

        print(f"AIGC 生图任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")

        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_aigc_image.py query --task-id {result['TaskId']}")

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"创建生图任务失败: {e}")
        sys.exit(1)


def wait_for_task(client, task_id, sub_app_id=None, max_wait=600, poll_interval=10):
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

            time.sleep(poll_interval)
        # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
        except Exception as e:
            print(f"查询任务状态失败: {e}")
            time.sleep(poll_interval)

    print(f"⏱️ 等待超时（{max_wait}秒），任务仍在执行中")
    return None


def list_models(args):
    """列出支持的模型"""
    print("支持的模型和版本:")
    for model, versions in MODEL_VERSIONS.items():
        default = MODEL_DEFAULT_VERSION[model]
        print(f"  {model}: 版本 {versions}（默认 {default}）")


def query_task(args):
    """查询 AIGC 生图任务状态"""
    if hasattr(args, 'dry_run') and args.dry_run:
        print(f"[DRY RUN] DescribeTaskDetail 请求预览:")
        print(f"  TaskId: {args.task_id}")
        if getattr(args, 'sub_app_id', None):
            print(f"  SubAppId: {args.sub_app_id}")
        return

    client = get_client(args.region)

    if not args.no_wait:
        result = wait_for_task(client, args.task_id, args.sub_app_id, args.max_wait, args.poll_interval)
        if result is None:
            print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
    else:
        req = models.DescribeTaskDetailRequest()
        req.TaskId = args.task_id
        if args.sub_app_id:
            req.SubAppId = args.sub_app_id
        try:
            resp = client.DescribeTaskDetail(req)
            result = json.loads(resp.to_json_string())
            status = result.get('Status', 'N/A')
            print(f"任务状态: {status}")
        # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
        except Exception as e:
            print(f"查询失败: {e}")
            sys.exit(1)

    if result and args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(
        description='VOD AIGC 生图任务工具（CreateAigcImageTask）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 使用混元模型生图（文生图）
  python vod_aigc_image.py create --model Hunyuan --prompt "一只可爱的小猫在草地上玩耍"

  # 使用千问模型，指定版本
  python vod_aigc_image.py create --model Qwen --model-version 0925 --prompt "a beautiful sunset"

  # 图生图（指定参考图 FileId）
  python vod_aigc_image.py create --model GEM --model-version 2.5 \\
      --file-id 528548548798527148 --prompt "将图片风格改为水彩画"

  # 图生图（指定参考图 URL）
  python vod_aigc_image.py create --model Kling --model-version 2.1 \\
      --file-url "https://example.com/ref.jpg" --prompt "保持主体，改变背景为星空"

  # 设置输出配置（永久存储，指定分辨率和宽高比）
  python vod_aigc_image.py create --model Hunyuan --prompt "风景画" \\
      --output-storage-mode Permanent --output-resolution 2K --output-aspect-ratio 16:9

  # 开启提示词优化
  python vod_aigc_image.py create --model GEM --prompt "cat" --enhance-prompt Enabled

  # 默认等待任务完成（加 --no-wait 可不等待）
  python vod_aigc_image.py create --model Hunyuan --prompt "一只狗"

  # 列出支持的模型
  python vod_aigc_image.py models

  # 预览请求参数
  python vod_aigc_image.py create --model Hunyuan --prompt "test" --dry-run
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # ---- create 子命令 ----
    create_parser = subparsers.add_parser('create', help='创建 AIGC 生图任务')

    # 模型参数（必填）
    create_parser.add_argument('--model', required=True,
                               choices=list(MODEL_VERSIONS.keys()),
                               help='模型名称（必填）：Hunyuan/Qwen/Vidu/Kling/MJ/GEM')
    create_parser.add_argument('--model-version', help='模型版本，不填则使用默认版本')

    # 内容参数
    create_parser.add_argument('--prompt', help='生成图片的提示词（当无输入文件时必填）')
    create_parser.add_argument('--negative-prompt', help='负面提示词，阻止模型生成的内容')
    create_parser.add_argument('--enhance-prompt', choices=['Enabled', 'Disabled'],
                               help='是否自动优化提示词：Enabled/Disabled')

    # 输入文件（参考图，三选一）
    create_parser.add_argument('--file-id', help='参考图的 VOD 文件 FileId（与 --file-url 互斥）')
    create_parser.add_argument('--file-url', help='参考图的 URL（与 --file-id 互斥）')
    create_parser.add_argument('--file-text', help='参考图的描述信息（仅 GEM 2.5/3.0 有效）')
    create_parser.add_argument('--file-infos', help='多个参考图的 JSON 数组，格式：[{"Type":"Url","Url":"..."}]')

    # 输出配置
    create_parser.add_argument('--output-storage-mode', choices=['Permanent', 'Temporary'],
                               help='存储模式：Permanent（永久）/ Temporary（临时，默认）')
    create_parser.add_argument('--output-media-name', help='输出文件名，最长 64 字符')
    create_parser.add_argument('--output-class-id', type=int, help='输出文件分类 ID，默认 0')
    create_parser.add_argument('--output-expire-time', help='输出文件过期时间，ISO 8601 格式')
    create_parser.add_argument('--output-resolution',
                               help='生成图片分辨率，如 1K/2K/4K（GEM）、1080p/2K/4K（Vidu）、720P/1080P/2K/4K（Hunyuan）')
    create_parser.add_argument('--output-aspect-ratio',
                               help='图片宽高比，如 16:9、9:16、1:1、4:3、3:4 等')
    create_parser.add_argument('--output-person-generation',
                               choices=['AllowAdult', 'Disallowed'],
                               help='是否允许人物生成：AllowAdult/Disallowed')
    create_parser.add_argument('--input-compliance-check', choices=['Enabled', 'Disabled'],
                               help='是否开启输入内容合规检查')
    create_parser.add_argument('--output-compliance-check', choices=['Enabled', 'Disabled'],
                               help='是否开启输出内容合规检查')

    # 其他参数
    create_parser.add_argument('--scene-type',
                               help='场景类型（当 ModelName 为 Hunyuan 时：3d_panorama 表示全景图；其他模型暂不支持）')
    create_parser.add_argument('--seed', type=int, help='模型随机种子')
    create_parser.add_argument('--input-region', choices=['Mainland', 'Oversea'],
                               help='输入文件区域：Mainland（默认）/ Oversea（国外地址时使用）')
    create_parser.add_argument('--session-id', help='去重识别码，三天内相同 ID 返回错误，最长 50 字符')
    create_parser.add_argument('--session-context', help='来源上下文，透传用户请求信息，最长 1000 字符')
    create_parser.add_argument('--tasks-priority', type=int, help='任务优先级，范围 -10 到 10，默认 0')
    create_parser.add_argument('--ext-info', help='保留字段，特殊用途时使用')
    create_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                               help='子应用 ID，2023-12-25 后开通点播的客户必填')
    create_parser.add_argument('--region', default='ap-guangzhou', help='地域，默认 ap-guangzhou')
    create_parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    create_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)，默认 600')
    create_parser.add_argument('--json', action='store_true', help='JSON 格式输出完整响应')
    create_parser.add_argument('--dry-run', action='store_true', help='预览请求参数，不实际执行')

    # ---- models 子命令 ----
    _ = subparsers.add_parser('models', help='列出支持的模型和版本')

    # ---- query 子命令（查询任务状态）----
    query_parser = subparsers.add_parser('query', help='查询 AIGC 生图任务状态（通过 DescribeTaskDetail）')
    query_parser.add_argument('--task-id', required=True, help='任务 ID（必填）')
    query_parser.add_argument('--sub-app-id', type=int,
                              default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                              help='子应用 ID')
    query_parser.add_argument('--region', default='ap-guangzhou', help='地域，默认 ap-guangzhou')
    query_parser.add_argument('--no-wait', action='store_true', help='仅查询状态，不等待完成')
    query_parser.add_argument('--poll-interval', type=int, default=10, help='轮询间隔（秒），默认 10')
    query_parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)，默认 600')
    query_parser.add_argument('--json', action='store_true', help='JSON 格式输出完整响应')
    query_parser.add_argument('--dry-run', action='store_true', help='预览请求参数，不实际执行')

    args = parser.parse_args()

    if args.command == 'create':
        create_image_task(args)
    elif args.command == 'models':
        list_models(args)
    elif args.command == 'query':
        query_task(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
