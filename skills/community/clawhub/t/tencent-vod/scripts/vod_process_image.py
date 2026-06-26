#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD 图片处理脚本
支持异步图片处理（ProcessImageAsync）、图片理解（大语言模型）和图片超分增强

图片理解功能：
- 基于大语言模型（Gemini 系列）对图片进行智能理解和分析
- 支持自定义提示词（Prompts）引导模型分析方向
- 支持 FileId / URL / Base64 三种输入方式
- 支持选择模型：gemini-2.5-flash / gemini-2.5-flash-lite / gemini-2.5-pro / gemini-3-flash / gemini-3-pro

图片超分增强功能：
- 通过 CreateProcessImageAsyncTemplate 创建自定义超分模板（模板可复用）
- 支持三种超分模式：percent（倍率放大）、fixed（固定分辨率）、aspect（比例适配）
- 支持 standard（通用超分）和 super（高级超分）两种类型
- 支持自定义输出格式（JPEG/PNG/BMP/WebP）和质量参数
- 目标分辨率不超过 4096x4096
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


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def understand_image(args):
    """图片理解 - 基于大语言模型对图片进行智能理解和分析
    使用 ProcessImageAsync 接口，模板 Definition=14
    支持 Prompts 提示词和多种 Gemini 模型
    """
    # 验证输入
    if not args.file_id and not args.url and not args.base64:
        print("错误：请指定 --file-id、--url 或 --base64 之一")
        sys.exit(1)

    if not args.sub_app_id:
        print("错误：图片理解功能必须指定 --sub-app-id")
        sys.exit(1)

    prompt_text = args.prompt or "理解这张图片"

    # 构建请求参数
    req_params = {}
    if args.file_id:
        req_params["FileId"] = args.file_id
    elif args.url:
        req_params["Url"] = args.url
    elif args.base64:
        req_params["Base64"] = args.base64

    req_params["SubAppId"] = args.sub_app_id

    # 图片理解固定模板 14 + Prompts
    req_params["ImageTaskInput"] = {
        "Definition": 14,
        "ExtendedParameter": {
            "Prompts": [prompt_text]
        }
    }

    # 输出配置
    output_config = {}
    if args.output_name:
        output_config["MediaName"] = args.output_name
    if args.class_id is not None:
        output_config["ClassId"] = args.class_id
    if args.expire_time:
        output_config["ExpireTime"] = args.expire_time
    if output_config:
        req_params["OutputConfig"] = output_config

    # 设置模型（通过 ExtInfo）
    if args.model:
        model_map = {
            "gemini-2.5-flash": "Google/gemini-2.5-flash",
            "gemini-2.5-flash-lite": "Google/gemini-2.5-flash-lite",
            "gemini-2.5-pro": "Google/gemini-2.5-pro",
            "gemini-3-flash": "Google/gemini-3-flash",
            "gemini-3-pro": "Google/gemini-3-pro",
        }
        model_name = model_map.get(args.model, args.model)
        if "/" not in model_name:
            model_name = f"Google/{model_name}"
        req_params["ExtInfo"] = json.dumps({"ModelName": model_name})
    elif args.ext_info:
        req_params["ExtInfo"] = args.ext_info

    if args.session_id:
        req_params["SessionId"] = args.session_id
    if args.session_context:
        req_params["SessionContext"] = args.session_context
    if args.tasks_priority is not None:
        req_params["TasksPriority"] = args.tasks_priority

    if args.dry_run:
        print("[DRY RUN] 图片理解请求参数:")
        print(json.dumps(req_params, indent=2, ensure_ascii=False))
        return

    client = get_client(args.region)

    try:
        req = models.ProcessImageAsyncRequest()
        req.from_json_string(json.dumps(req_params))

        resp = client.ProcessImageAsync(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get('TaskId', 'N/A')
        print(f"图片理解任务已提交!")
        print(f"TaskId: {task_id}")
        print(f"提示词: {prompt_text}")
        if args.model:
            print(f"模型: {args.model}")

        # 默认等待任务完成并输出理解结果
        if not args.no_wait and task_id != 'N/A':
            understand_result = wait_for_understand(client, task_id, args.sub_app_id, args.max_wait)
            if understand_result:
                output_text = extract_output_text(understand_result)
                if output_text:
                    print(f"\n{'='*60}")
                    print(f"图片理解结果:")
                    print(f"{'='*60}")
                    print(output_text)
                    print(f"{'='*60}")

                if args.json:
                    print(json.dumps(understand_result, indent=2, ensure_ascii=False))

                return understand_result
        else:
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        print(f"图片理解失败: {e}")
        sys.exit(1)


def super_resolution_image(args):
    """图片超分增强 - 通过创建自定义模板 + ProcessImageAsync 实现高级超分
    流程：1.创建超分模板（或使用已有模板） → 2.发起超分任务 → 3.等待结果
    """
    if not args.sub_app_id:
        print("错误：图片超分增强必须指定 --sub-app-id")
        sys.exit(1)

    # 如果用户直接提供了模板 ID，跳过创建模板步骤
    if args.template_id:
        definition = args.template_id
        print(f"使用已有模板 Definition: {definition}")
    else:
        # 步骤 1：构建并创建超分模板
        template_params = build_super_resolution_template(args)

        if args.dry_run:
            print("[DRY RUN] 步骤 1 - 创建超分模板请求参数:")
            print(json.dumps(template_params, indent=2, ensure_ascii=False))
            # 继续展示步骤 2 的参数
            print("\n[DRY RUN] 步骤 2 - 发起超分任务请求参数:")
            task_params = {
                "SubAppId": args.sub_app_id,
                "FileId": args.file_id,
                "ImageTaskInput": {
                    "Definition": "<步骤1返回的模板ID>"
                }
            }
            print(json.dumps(task_params, indent=2, ensure_ascii=False))
            return

        client = get_client(args.region)
        print("步骤 1/3：创建超分模板...")
        definition = create_super_resolution_template(client, template_params)
        print(f"✅ 模板创建成功，Definition: {definition}")
        print("等待模板生效（10秒）...")
        time.sleep(10)

    if args.dry_run:
        return

    # 步骤 2：发起超分任务
    if not hasattr(args, '_client'):
        client = get_client(args.region)

    print(f"\n步骤 2/3：发起图片超分任务...")
    task_params = {
        "SubAppId": args.sub_app_id,
        "FileId": args.file_id,
        "ImageTaskInput": {
            "Definition": definition
        }
    }
    if args.session_id:
        task_params["SessionId"] = args.session_id
    if args.tasks_priority is not None:
        task_params["TasksPriority"] = args.tasks_priority

    try:
        req = models.ProcessImageAsyncRequest()
        req.from_json_string(json.dumps(task_params))

        resp = client.ProcessImageAsync(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get('TaskId', 'N/A')
        print(f"✅ 超分任务已提交，TaskId: {task_id}")

        # 步骤 3：等待任务完成
        if not args.no_wait and task_id != 'N/A':
            print(f"\n步骤 3/3：等待超分任务完成...")
            sr_result = wait_for_super_resolution(client, task_id, args.sub_app_id, args.max_wait)
            if sr_result:
                extract_super_resolution_output(sr_result)
                if args.json:
                    print(json.dumps(sr_result, indent=2, ensure_ascii=False))
                return sr_result
        else:
            print("提示：使用 DescribeTaskDetail 接口查询任务结果")
            if args.json:
                print(json.dumps(result, indent=2, ensure_ascii=False))
            return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        print(f"图片超分任务失败: {e}")
        sys.exit(1)


def build_super_resolution_template(args):
    """构建超分模板参数"""
    # 超分配置
    sr_config = {
        "Switch": "ON",
        "Type": args.sr_type,
    }

    if args.mode == 'percent':
        sr_config["Mode"] = "percent"
        sr_config["Percent"] = args.percent
    elif args.mode == 'fixed':
        sr_config["Mode"] = "fixed"
        if not args.width or not args.height:
            print("错误：fixed 模式必须同时指定 --width 和 --height")
            sys.exit(1)
        sr_config["Width"] = args.width
        sr_config["Height"] = args.height
    elif args.mode == 'aspect':
        sr_config["Mode"] = "aspect"
        if not args.width or not args.height:
            print("错误：aspect 模式必须同时指定 --width 和 --height")
            sys.exit(1)
        sr_config["Width"] = args.width
        sr_config["Height"] = args.height

    # 编码配置
    encode_config = {}
    if args.output_format:
        encode_config["Format"] = args.output_format
    if args.quality is not None:
        encode_config["Quality"] = args.quality

    # 组装模板
    process_image_configure = {
        "EnhanceConfig": {
            "AdvancedSuperResolution": sr_config
        }
    }
    if encode_config:
        process_image_configure["EncodeConfig"] = encode_config

    # 模板名称和描述
    mode_desc = {
        'percent': f"{args.percent}倍放大",
        'fixed': f"{args.width}x{args.height}固定分辨率",
        'aspect': f"{args.width}x{args.height}比例适配",
    }
    template_name = args.template_name or f"超分模板-{args.sr_type}-{mode_desc[args.mode]}"
    template_comment = args.template_comment or f"图片{args.sr_type}超分-{mode_desc[args.mode]}"

    template_params = {
        "ProcessImageConfigure": process_image_configure,
        "SubAppId": args.sub_app_id,
        "Name": template_name,
        "Comment": template_comment,
    }

    return template_params


def create_super_resolution_template(client, template_params):
    """调用 CreateProcessImageAsyncTemplate 创建超分模板"""
    try:
        action = "CreateProcessImageAsyncTemplate"
        resp_str = client.call(action, template_params)
        result = json.loads(resp_str)

        if 'Response' in result and 'Definition' in result['Response']:
            return result['Response']['Definition']
        elif 'Response' in result and 'Error' in result['Response']:
            error = result['Response']['Error']
            print(f"创建模板失败: [{error.get('Code')}] {error.get('Message')}")
            sys.exit(1)
        else:
            print(f"创建模板响应异常: {json.dumps(result, indent=2, ensure_ascii=False)}")
            sys.exit(1)
    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        print(f"创建超分模板失败: {e}")
        sys.exit(1)


def wait_for_super_resolution(client, task_id, sub_app_id=None, max_wait=300):
    """等待图片超分任务完成"""
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
            elapsed = int(time.time() - start_time)
            print(f"  [{elapsed}s] 状态: {status}")

            if status == 'FINISH':
                task_detail = result.get('ProcessImageAsyncTask') or {}
                err_code = task_detail.get('ErrCode', -1)
                if err_code == 0:
                    print("✅ 图片超分完成!")
                else:
                    print(f"❌ 图片超分失败: {task_detail.get('Message', '未知错误')}")
                return result
            elif status in ('FAIL', 'ABORTED'):
                print(f"❌ 任务失败: {status}")
                return result

            time.sleep(3)
        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
            print(f"  查询状态失败: {e}")
            time.sleep(5)

    print(f"⏱️ 等待超时（{max_wait}秒），任务仍在执行中")
    return None


def extract_super_resolution_output(result):
    """从超分任务结果中提取输出信息"""
    task_detail = result.get('ProcessImageAsyncTask') or {}
    output = task_detail.get('Output') or {}
    file_info = output.get('FileInfo') or {}

    if file_info:
        print(f"\n{'='*60}")
        print(f"图片超分结果:")
        print(f"{'='*60}")
        if file_info.get('FileId'):
            print(f"  FileId:   {file_info['FileId']}")
        if file_info.get('FileType'):
            print(f"  格式:     {file_info['FileType']}")
        if file_info.get('FileUrl'):
            print(f"  URL:      {file_info['FileUrl']}")

        meta = file_info.get('MetaData') or {}
        if meta:
            if meta.get('Width') and meta.get('Height'):
                print(f"  分辨率:   {meta['Width']}x{meta['Height']}")
            if meta.get('Size'):
                size_mb = meta['Size'] / 1024 / 1024
                print(f"  文件大小: {meta['Size']} bytes ({size_mb:.2f} MB)")
        print(f"{'='*60}")



def wait_for_understand(client, task_id, sub_app_id=None, max_wait=600):
    """等待图片理解任务完成，返回完整结果"""
    print(f"\n等待图片理解任务完成...")
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
            elapsed = int(time.time() - start_time)
            print(f"  [{elapsed}s] 状态: {status}")

            if status == 'FINISH':
                task_detail = result.get('ProcessImageAsyncTask') or {}
                err_code = task_detail.get('ErrCode', -1)
                if err_code == 0:
                    print("✅ 图片理解完成!")
                else:
                    print(f"❌ 图片理解失败: {task_detail.get('Message', '未知错误')}")
                return result
            elif status in ('FAIL', 'ABORTED'):
                print(f"❌ 任务失败: {status}")
                return result

            time.sleep(3)
        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
            print(f"  查询状态失败: {e}")
            time.sleep(5)

    print(f"⏱️ 等待超时（{max_wait}秒），任务仍在执行中")
    return None


def extract_output_text(result):
    """从图片理解任务结果中提取 OutputText"""
    task_detail = result.get('ProcessImageAsyncTask') or {}
    output = task_detail.get('Output') or {}
    return output.get('OutputText', '')


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
        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
            print(f"查询任务状态失败: {e}")
            time.sleep(5)

    print(f"⏱️ 等待超时（{max_wait}秒），任务仍在执行中")
    return None


def main():
    parser = argparse.ArgumentParser(
        description='VOD 图片处理工具（图片超分增强 + 图片理解）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 图片超分增强（默认2倍高级超分，自动等待结果）
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154

  # 超分到固定分辨率 1920x1080
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154 \\
      --mode fixed --width 1920 --height 1080

  # 使用已有模板 ID 进行超分
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154 \\
      --template-id 7

  # 图片理解（默认提示词"理解这张图片"，自动等待结果）
  python vod_process_image.py understand --file-id <id> --sub-app-id 1500046154

  # 图片理解，自定义提示词 + 指定模型
  python vod_process_image.py understand --file-id <id> --sub-app-id 1500046154 \\
      --model gemini-2.5-pro --prompt "分析这张图片的构图和色彩"

  # 使用模板 ID 进行图片理解
  python vod_process_image.py understand --url 'https://example.com/img.jpg' --sub-app-id 1500046154 \\
      --template-id 10

支持的图片理解模型: gemini-2.5-flash, gemini-2.5-flash-lite, gemini-2.5-pro, gemini-3-flash, gemini-3-pro
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # ---- super-resolution 子命令（图片超分增强）----
    understand_parser = subparsers.add_parser('understand', help='图片理解（基于大语言模型，对图片进行智能理解和分析）')

    # 输入来源（三选一）
    understand_input = understand_parser.add_mutually_exclusive_group(required=True)
    understand_input.add_argument('--file-id', help='图片文件 FileId（与 --url、--base64 互斥）')
    understand_input.add_argument('--url', help='图片 URL（与 --file-id、--base64 互斥）')
    understand_input.add_argument('--base64', help='图片 Base64 编码（与 --file-id、--url 互斥，文件需 <4MB）')

    # 图片理解参数
    understand_parser.add_argument('--prompt', default='理解这张图片',
                                   help='提示词，指导模型如何理解图片（默认: "理解这张图片"）')
    understand_parser.add_argument('--model', choices=[
        'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-2.5-pro',
        'gemini-3-flash', 'gemini-3-pro'
    ], help='指定大语言模型（默认由服务端决定）')

    # 输出配置
    understand_parser.add_argument('--output-name', help='输出文件名称')
    understand_parser.add_argument('--class-id', type=int, help='分类 ID')
    understand_parser.add_argument('--expire-time', help='过期时间，ISO 8601 格式，如 2025-12-31T23:59:59Z')

    # 通用参数
    understand_parser.add_argument('--sub-app-id', type=int,
                                   default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                                   help='子应用 ID（必填）')
    understand_parser.add_argument('--session-id', help='去重识别码，三天内相同 ID 的请求会返回错误')
    understand_parser.add_argument('--session-context', help='来源上下文，透传用户请求信息')
    understand_parser.add_argument('--tasks-priority', type=int, help='任务优先级，范围 -10 到 10')
    understand_parser.add_argument('--ext-info', help='扩展信息（JSON 字符串，如指定模型名称）')
    understand_parser.add_argument('--region', default='ap-guangzhou', help='地域，默认 ap-guangzhou')
    understand_parser.add_argument('--no-wait', action='store_true',
                                   help='仅提交任务，不等待结果（默认自动等待）')
    understand_parser.add_argument('--max-wait', type=int, default=120, help='最大等待时间(秒)，默认 120')
    understand_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    understand_parser.add_argument('--dry-run', action='store_true', help='预览请求参数，不实际执行')

    # ---- super-resolution 子命令（图片超分增强）----
    sr_parser = subparsers.add_parser('super-resolution',
        help='图片超分增强（创建自定义超分模板 + 发起超分任务）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
超分模式说明:
  percent  按倍率放大（默认），如 --percent 2.0 表示放大2倍
  fixed    固定分辨率输出，需指定 --width 和 --height
  aspect   比例适配，超分至指定宽高的较大矩形，保持比例

超分类型说明:
  standard  通用超分，处理速度较快
  super     高级超分，画质更好但处理时间较长

示例:
  # 2倍超分（默认高级超分，倍率模式）
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154

  # 固定分辨率超分到 1920x1080
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154 \\
      --mode fixed --width 1920 --height 1080

  # 比例适配超分到 4K
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154 \\
      --mode aspect --width 3840 --height 2160

  # 使用已有模板
  python vod_process_image.py super-resolution --file-id <id> --sub-app-id 1500046154 \\
      --template-id 30023
        ''')

    sr_parser.add_argument('--file-id', required=True, help='图片文件 FileId（必填）')

    # 超分参数
    sr_parser.add_argument('--mode', choices=['percent', 'fixed', 'aspect'], default='percent',
                           help='超分模式：percent=倍率放大（默认）, fixed=固定分辨率, aspect=比例适配')
    sr_parser.add_argument('--percent', type=float, default=2.0,
                           help='超分倍率，可以为小数（mode=percent 时使用，默认 2.0）')
    sr_parser.add_argument('--width', type=int,
                           help='目标图片宽度，不超过 4096（mode=fixed/aspect 时必填）')
    sr_parser.add_argument('--height', type=int,
                           help='目标图片高度，不超过 4096（mode=fixed/aspect 时必填）')
    sr_parser.add_argument('--sr-type', choices=['standard', 'super'], default='super',
                           help='超分类型：standard=通用超分, super=高级超分（默认）')

    # 输出格式
    sr_parser.add_argument('--output-format', choices=['JPEG', 'PNG', 'BMP', 'WebP'],
                           help='输出图片格式（默认为原图格式）')
    sr_parser.add_argument('--quality', type=int,
                           help='图片相对质量（JPEG/WebP 有效，1-100），默认为原图质量')

    # 模板相关
    sr_parser.add_argument('--template-id', type=int,
                           help='使用已有的超分模板 ID（跳过创建模板步骤）')
    sr_parser.add_argument('--template-name', help='自定义模板名称')
    sr_parser.add_argument('--template-comment', help='自定义模板描述')

    # 通用参数
    sr_parser.add_argument('--sub-app-id', type=int,
                           default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                           help='子应用 ID（必填）')
    sr_parser.add_argument('--session-id', help='去重识别码，三天内相同 ID 的请求会返回错误')
    sr_parser.add_argument('--tasks-priority', type=int, help='任务优先级，范围 -10 到 10')
    sr_parser.add_argument('--region', default='ap-guangzhou', help='地域，默认 ap-guangzhou')
    sr_parser.add_argument('--no-wait', action='store_true',
                           help='仅提交任务，不等待结果（默认自动等待）')
    sr_parser.add_argument('--max-wait', type=int, default=300,
                           help='最大等待时间(秒)，默认 300')
    sr_parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    sr_parser.add_argument('--dry-run', action='store_true', help='预览请求参数，不实际执行')

    args = parser.parse_args()

    if args.command == 'understand':
        understand_image(args)
    elif args.command == 'super-resolution':
        super_resolution_image(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
