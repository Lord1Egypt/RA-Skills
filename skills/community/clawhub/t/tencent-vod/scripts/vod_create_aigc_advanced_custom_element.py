#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD AIGC 高级自定义主体创建脚本
基于 CreateAigcAdvancedCustomElement API

功能：
  - 创建 AIGC 高级自定义主体（视频角色主体 / 多图主体）
  - 支持交互式引导输入（--interactive）
  - 创建成功后自动记录到 mem/elements.json
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime

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
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.common.common_client import CommonClient
except ImportError:
    print("错误：请先安装腾讯云 SDK: pip install tencentcloud-sdk-python")
    sys.exit(1)


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

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
    """获取 VOD CommonClient（支持 SDK 未收录的新接口）"""
    cred = get_credential()
    http_profile = HttpProfile()
    http_profile.endpoint = "vod.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return CommonClient("vod", "2018-07-17", cred, region, client_profile)


def get_mem_path():
    """获取 mem/elements.json 路径"""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mem_dir = os.path.join(skill_dir, "mem")
    os.makedirs(mem_dir, exist_ok=True)
    return os.path.join(mem_dir, "elements.json")


def save_element_record(record: dict):
    """将创建记录写入 mem/elements.json（以 task_id 为唯一 key，upsert）"""
    mem_path = get_mem_path()
    elements = []
    if os.path.exists(mem_path):
        try:
            with open(mem_path, "r", encoding="utf-8") as f:
                elements = json.load(f)
            if not isinstance(elements, list):
                elements = []
        except (json.JSONDecodeError, IOError):
            elements = []

    task_id = record.get("task_id")
    matched = False
    for rec in elements:
        if rec.get("task_id") == task_id:
            rec.update(record)
            matched = True
            break
    if not matched:
        elements.append(record)

    with open(mem_path, "w", encoding="utf-8") as f:
        json.dump(elements, f, ensure_ascii=False, indent=2)

    return mem_path


def prompt_input(prompt_text, max_len=None, required=True, default=None, choices=None):
    """交互式输入辅助函数"""
    while True:
        suffix = ""
        if default:
            suffix += f" [默认: {default}]"
        if choices:
            suffix += f"\n   可选值: {' / '.join(choices)}"
        if max_len:
            suffix += f"（最多 {max_len} 个字符）"

        val = input(f"{prompt_text}{suffix}: ").strip()

        if not val:
            if default:
                return default
            if not required:
                return None
            print("  ⚠️  此项为必填，请重新输入。")
            continue

        if max_len and len(val) > max_len:
            print(f"  ⚠️  输入超过 {max_len} 个字符限制（当前 {len(val)} 字符），请重新输入。")
            continue

        if choices and val not in choices:
            print(f"  ⚠️  请输入有效值: {' / '.join(choices)}")
            continue

        return val


def prompt_list_input(prompt_text, required=False):
    """交互式输入列表（逗号分隔），返回列表"""
    val = input(f"{prompt_text}（多个请用英文逗号分隔，不需要则直接回车跳过）: ").strip()
    if not val:
        if required:
            print("  ⚠️  此项为必填，请重新输入。")
            return prompt_list_input(prompt_text, required=True)
        return []
    return [v.strip() for v in val.split(",") if v.strip()]


# ─────────────────────────────────────────────
# 交互式引导
# ─────────────────────────────────────────────

def interactive_guide():
    """交互式引导用户输入创建主体所需参数"""
    print("\n" + "=" * 60)
    print("  VOD AIGC 高级自定义主体创建向导")
    print("=" * 60)
    print("本向导将引导您逐步填写创建主体所需的信息。\n")

    params = {}

    # ── 1. ElementName ──
    print("【1/7】主体名称 (ElementName)")
    print("  说明：主体的唯一标识名称，建议取一个能体现主体功能的好名字，方便后续查询。")
    params["element_name"] = prompt_input("  请输入主体名称", max_len=20, required=True)

    # ── 2. ElementDescription ──
    print("\n【2/7】主体描述 (ElementDescription)")
    print("  说明：对主体的详细功能描述，帮助后续快速了解主体用途。")
    params["element_description"] = prompt_input("  请输入主体描述", max_len=100, required=True)

    # ── 3. ReferenceType ──
    print("\n【3/7】主体参考方式 (ReferenceType)")
    print("  说明：决定主体定制方式，不同方式的可用范围不同：")
    print("    video_refer  —— 视频角色主体，通过参考视频定义外表，支持绑定音色")
    print("    image_refer  —— 多图主体，通过多张图片定义外表，不支持绑定音色")
    params["reference_type"] = prompt_input(
        "  请选择参考方式", required=True,
        choices=["video_refer", "image_refer"]
    )

    # ── 4. ElementVoiceId（仅 video_refer 支持）──
    if params["reference_type"] == "video_refer":
        print("\n【4/7】主体音色 (ElementVoiceId)")
        print("  说明：可绑定音色库中已有音色的 ID。留空表示不绑定音色。")
        print("  注意：仅视频定制的主体（video_refer）支持绑定音色。")
        val = input("  请输入音色 ID（可留空跳过）: ").strip()
        params["element_voice_id"] = val if val else None
    else:
        print("\n【4/7】主体音色 (ElementVoiceId)")
        print("  说明：多图主体（image_refer）不支持绑定音色，已自动跳过。")
        params["element_voice_id"] = None

    # ── 5. ElementVideoList / ElementImageList ──
    if params["reference_type"] == "video_refer":
        print("\n【5/7】主体参考视频列表 (ElementVideoList)")
        print("  说明：通过视频设定主体外表。支持有声视频（含人声则自动触发音色定制）。")
        print("  格式要求：")
        print("    - 格式仅支持 MP4/MOV")
        print("    - 时长 3s～8s，宽高比 16:9 或 9:16，1080P")
        print("    - 最多 1 段视频，大小不超过 200MB")
        print("  请输入视频 URL（video_url）：")
        video_urls = prompt_list_input("  视频 URL", required=True)
        # 构建 JSON 格式
        refer_videos = [{"video_url": url} for url in video_urls]
        params["element_video_list"] = json.dumps({"refer_videos": refer_videos}, ensure_ascii=False)
        params["element_image_list"] = None
    else:
        print("\n【5/7】主体参考图列表 (ElementImageList)")
        print("  说明：通过多张图片设定主体外表。")
        print("  要求：")
        print("    - 至少 1 张正面参考图（frontal_image）")
        print("    - 1～3 张其他角度或特写参考图（refer_images），需与正面图有差异")

        frontal = input("  请输入正面参考图 URL（frontal_image）: ").strip()
        while not frontal:
            print("  ⚠️  正面参考图为必填。")
            frontal = input("  请输入正面参考图 URL（frontal_image）: ").strip()

        print("  请输入其他参考图 URL（1～3 张，多个用英文逗号分隔）：")
        other_urls = prompt_list_input("  其他参考图 URL", required=False)

        refer_images = [{"image_url": url} for url in other_urls[:3]]
        img_payload = {"frontal_image": frontal}
        if refer_images:
            img_payload["refer_images"] = refer_images

        params["element_image_list"] = json.dumps(img_payload, ensure_ascii=False)
        params["element_video_list"] = None

    # ── 6. TagList ──
    print("\n【6/7】标签列表 (TagList)")
    print("  说明：为主体配置标签，便于分类管理。标签 ID 格式示例：o_101、o_102。")
    tag_ids = prompt_list_input("  标签 ID", required=False)
    if tag_ids:
        params["tag_list"] = json.dumps([{"tag_id": t} for t in tag_ids], ensure_ascii=False)
    else:
        params["tag_list"] = None

    # ── 7. SubAppId ──
    print("\n【7/7】子应用 ID (SubAppId)")
    print("  说明：点播子应用 ID。2023-12-25 后开通点播的用户必须填写。")
    env_sub = os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", "")
    default_sub = env_sub if env_sub else None
    val = input(f"  请输入子应用 ID{' [环境变量已配置: ' + env_sub + ']' if env_sub else '（必填）'}: ").strip()
    if val:
        params["sub_app_id"] = int(val)
    elif default_sub:
        params["sub_app_id"] = int(default_sub)
    else:
        print("  ⚠️  子应用 ID 为必填，请重新输入。")
        val = input("  请输入子应用 ID: ").strip()
        params["sub_app_id"] = int(val)

    print("\n" + "=" * 60)
    print("  参数确认")
    print("=" * 60)
    print(f"  主体名称       : {params['element_name']}")
    print(f"  主体描述       : {params['element_description']}")
    print(f"  参考方式       : {params['reference_type']}")
    print(f"  音色 ID        : {params['element_voice_id'] or '（不绑定）'}")
    if params.get("element_video_list"):
        print(f"  参考视频       : {params['element_video_list']}")
    if params.get("element_image_list"):
        print(f"  参考图         : {params['element_image_list']}")
    print(f"  标签           : {params['tag_list'] or '（无）'}")
    print(f"  子应用 ID      : {params['sub_app_id']}")
    print("=" * 60)

    confirm = input("\n确认以上信息并提交创建？[y/N]: ").strip().lower()
    if confirm != "y":
        print("已取消创建。")
        sys.exit(0)

    return params


# ─────────────────────────────────────────────
# 核心功能
# ─────────────────────────────────────────────

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def create_element(args):
    """调用 CreateAigcAdvancedCustomElement API 创建主体"""
    # 必需参数校验
    if not args.sub_app_id:
        print("错误：必须指定 --sub-app-id 或设置环境变量 TENCENTCLOUD_VOD_SUB_APP_ID")
        sys.exit(1)

    if not args.element_name:
        print("错误：必须指定 --element-name")
        sys.exit(1)

    if not args.element_description:
        print("错误：必须指定 --element-description")
        sys.exit(1)

    if not args.reference_type:
        print("错误：必须指定 --reference-type（video_refer 或 image_refer）")
        sys.exit(1)

    # 构建请求体
    req_body = {
        "SubAppId": args.sub_app_id,
        "ElementName": args.element_name,
        "ElementDescription": args.element_description,
        "ReferenceType": args.reference_type,
    }

    if args.element_voice_id:
        req_body["ElementVoiceId"] = args.element_voice_id

    if args.element_video_list:
        req_body["ElementVideoList"] = args.element_video_list

    if args.element_image_list:
        req_body["ElementImageList"] = args.element_image_list

    if args.tag_list:
        req_body["TagList"] = args.tag_list

    if args.session_id:
        req_body["SessionId"] = args.session_id

    if args.session_context:
        req_body["SessionContext"] = args.session_context

    if args.tasks_priority is not None:
        req_body["TasksPriority"] = args.tasks_priority

    if args.dry_run:
        print("[DRY RUN] 请求参数预览:")
        print(json.dumps(req_body, indent=2, ensure_ascii=False))
        return

    client = get_client(args.region)

    try:
        resp = client.call_json("CreateAigcAdvancedCustomElement", req_body)
        result = resp.get("Response", resp)

        task_id = result.get("TaskId", "N/A")
        request_id = result.get("RequestId", "N/A")

        print("\n" + "=" * 60)
        print("✅ AIGC 高级自定义主体创建任务已提交!")
        print("=" * 60)
        print(f"  TaskId     : {task_id}")
        print(f"  RequestId  : {request_id}")
        print("=" * 60)

        # 保存记录到 mem/elements.json
        record = {
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "task_id": task_id,
            "request_id": request_id,
            "sub_app_id": args.sub_app_id,
            "element_name": args.element_name,
            "element_description": args.element_description,
            "reference_type": args.reference_type,
            "element_voice_id": args.element_voice_id or None,
            "element_video_list": args.element_video_list or None,
            "element_image_list": args.element_image_list or None,
            "tag_list": args.tag_list or None,
            "session_id": args.session_id or None,
            "session_context": args.session_context or None,
            "tasks_priority": args.tasks_priority,
        }
        save_element_record(record)

        # 等待任务完成（默认等待）
        if not args.no_wait and task_id != "N/A":
            wait_result = wait_for_task(client, task_id, args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {task_id}")

        if args.json:
            print("\nJSON 响应:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result

    except TencentCloudSDKException as e:
        print(f"创建主体失败: {e}")
        sys.exit(1)
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)


def list_elements(args):
    """列出本地已记录的主体信息"""
    mem_path = get_mem_path()
    if not os.path.exists(mem_path):
        print("暂无已创建主体记录。")
        return

    with open(mem_path, "r", encoding="utf-8") as f:
        elements = json.load(f)

    if not elements:
        print("暂无已创建主体记录。")
        return

    if args.json:
        print(json.dumps(elements, indent=2, ensure_ascii=False))
        return

    print(f"\n共 {len(elements)} 条主体创建记录：\n")
    for i, elem in enumerate(elements, 1):
        print(f"[{i}] 主体名称: {elem.get('element_name', 'N/A')}")
        print(f"    创建时间: {elem.get('created_at', 'N/A')}")
        print(f"    TaskId  : {elem.get('task_id', 'N/A')}")
        print(f"    描述    : {elem.get('element_description', 'N/A')}")
        print(f"    参考方式: {elem.get('reference_type', 'N/A')}")
        print(f"    标签    : {elem.get('tag_list', '（无）')}")
        print()


def wait_for_task(client, task_id, sub_app_id=None, max_wait=600):
    """等待任务完成"""
    print(f"\n等待任务完成 (TaskId: {task_id})...")
    start_time = time.time()

    while time.time() - start_time < max_wait:
        try:
            req = {
                "TaskId": task_id
            }
            if sub_app_id:
                req["SubAppId"] = sub_app_id

            resp = client.call_json("DescribeTaskDetail", req)
            result = resp.get("Response", resp)

            status = result.get("Status", "PROCESSING")
            elapsed = int(time.time() - start_time)
            print(f"  [{elapsed}s] 状态: {status}")

            if status == "FINISH":
                print("✅ 任务完成!")
                return result
            elif status == "FAIL":
                err_msg = result.get("Message", "未知错误")
                print(f"❌ 任务失败: {err_msg}")
                return result

            time.sleep(5)
        # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
        except Exception as e:
            print(f"查询任务状态失败: {e}")
            time.sleep(5)

    print(f"⏱️ 等待超时（{max_wait}秒），任务仍在执行中")
    return None


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="VOD AIGC 高级自定义主体创建工具\n基于 CreateAigcAdvancedCustomElement API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式引导创建（推荐）
  python vod_create_aigc_advanced_custom_element.py create --interactive

  # 命令行直接创建（多图主体）
  python vod_create_aigc_advanced_custom_element.py create \\
    --sub-app-id 1500046725 \\
    --element-name "我的主体" \\
    --element-description "用于商品展示的主体" \\
    --reference-type image_refer \\
    --element-image-list '{"frontal_image":"https://example.com/front.jpg","refer_images":[{"image_url":"https://example.com/side.jpg"}]}' \\
    --tag-list '[{"tag_id":"o_101"}]'

  # 命令行直接创建（视频角色主体）
  python vod_create_aigc_advanced_custom_element.py create \\
    --sub-app-id 1500046725 \\
    --element-name "视频主体A" \\
    --element-description "从视频中定制的角色主体" \\
    --reference-type video_refer \\
    --element-video-list '{"refer_videos":[{"video_url":"https://example.com/ref.mp4"}]}' \\
    --element-voice-id "123333"

  # 预览请求参数（不实际执行）
  python vod_create_aigc_advanced_custom_element.py create \\
    --element-name "测试" --element-description "测试描述" \\
    --reference-type image_refer --sub-app-id 1500046725 --dry-run

  # 查看已创建主体记录
  python vod_create_aigc_advanced_custom_element.py list

参考方式说明:
  video_refer  —— 视频角色主体，通过参考视频定义外表，支持绑定音色
  image_refer  —— 多图主体，通过多张图片定义外表，不支持绑定音色
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # ── create 子命令 ──
    create_parser = subparsers.add_parser("create", help="创建 AIGC 高级自定义主体")

    create_parser.add_argument(
        "--interactive", "-i", action="store_true",
        help="启用交互式引导模式，逐步提示输入各参数（推荐新用户使用）"
    )

    # 必需参数（非交互模式）
    create_parser.add_argument(
        "--sub-app-id", type=int,
        default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
        help="点播应用 ID（必填，也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）"
    )
    create_parser.add_argument(
        "--element-name",
        help="主体名称，不能超过 20 个字符（必填）"
    )
    create_parser.add_argument(
        "--element-description",
        help="主体描述，不能超过 100 个字符（必填）"
    )
    create_parser.add_argument(
        "--reference-type",
        choices=["video_refer", "image_refer"],
        help="主体参考方式：video_refer（视频角色主体）/ image_refer（多图主体）（必填）"
    )

    # 可选参数
    create_parser.add_argument(
        "--element-voice-id",
        help="主体音色 ID，绑定音色库中已有音色。仅 video_refer 类型支持。留空不绑定音色。"
    )
    create_parser.add_argument(
        "--element-video-list",
        help=(
            "主体参考视频（JSON 字符串）。参考方式为 video_refer 时必填。\n"
            '格式: \'{"refer_videos":[{"video_url":"https://..."}]}\''
        )
    )
    create_parser.add_argument(
        "--element-image-list",
        help=(
            "主体参考图（JSON 字符串）。参考方式为 image_refer 时必填。\n"
            '格式: \'{"frontal_image":"https://...","refer_images":[{"image_url":"https://..."}]}\''
        )
    )
    create_parser.add_argument(
        "--tag-list",
        help=(
            "主体标签列表（JSON 字符串）。\n"
            '格式: \'[{"tag_id":"o_101"},{"tag_id":"o_102"}]\''
        )
    )
    create_parser.add_argument(
        "--session-id",
        help="用于去重的识别码（最长 50 字符，3天内重复会返回错误）"
    )
    create_parser.add_argument(
        "--session-context",
        help="来源上下文，用于透传用户请求信息（最长 1000 字符）"
    )
    create_parser.add_argument(
        "--tasks-priority", type=int,
        help="任务优先级（-10 到 10，数值越大优先级越高，默认 0）"
    )

    # 通用参数
    create_parser.add_argument("--region", default="ap-guangzhou", help="地域（默认 ap-guangzhou）")
    create_parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    create_parser.add_argument("--dry-run", action="store_true", help="预览请求参数，不实际执行")
    create_parser.add_argument("--no-wait", action="store_true", help="仅提交任务，不等待结果")
    create_parser.add_argument("--max-wait", type=int, default=600, help="最大等待时间(秒)，默认 600")

    # ── list 子命令 ──
    list_parser = subparsers.add_parser("list", help="查看本地已创建主体记录（mem/elements.json）")
    list_parser.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    if args.command == "create":
        if args.interactive:
            # 交互式引导
            params = interactive_guide()
            # 将引导结果合并到 args
            args.sub_app_id = params["sub_app_id"]
            args.element_name = params["element_name"]
            args.element_description = params["element_description"]
            args.reference_type = params["reference_type"]
            args.element_voice_id = params.get("element_voice_id")
            args.element_video_list = params.get("element_video_list")
            args.element_image_list = params.get("element_image_list")
            args.tag_list = params.get("tag_list")
            if not hasattr(args, "session_id"):
                args.session_id = None
            if not hasattr(args, "session_context"):
                args.session_context = None
            if not hasattr(args, "tasks_priority"):
                args.tasks_priority = None
            if not hasattr(args, "dry_run"):
                args.dry_run = False
            if not hasattr(args, "json"):
                args.json = False

        create_element(args)

    elif args.command == "list":
        list_elements(args)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
