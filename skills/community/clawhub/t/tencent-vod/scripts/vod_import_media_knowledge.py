#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD 导入媒体知识库脚本
使用 ImportMediaKnowledge API 对视频进行大模型内容理解，并将理解结果存入知识库。

核心流程：
1. 对指定视频发起大模型内容理解任务（包括摘要生成、ASR 语音识别等）
2. 将理解后的结构化内容（摘要、字幕、关键信息等）持久化存储到 VOD 知识库中
3. 存储后的内容可通过 SearchMediaBySemantics 等接口进行语义搜索和知识检索

典型使用场景：
- 对已上传的视频进行智能分析，提取视频核心内容
- 构建视频知识库，支持后续基于语义的内容检索和问答
- 批量处理视频库，为大规模视频资产建立可搜索的知识索引

默认模板 100：包含音频级别的摘要和 ASR（语音识别）。

API 文档：https://cloud.tencent.com/document/api/266/126286
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


# 预置模板说明
DEFINITION_TEMPLATES = {
    100: "音频级别的摘要和 ASR（语音识别）",
}


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


def import_media_knowledge(args):
    """导入媒体到知识库"""

    req = models.ImportMediaKnowledgeRequest()

    # 必填参数
    if not args.sub_app_id:
        print("错误：必须指定 --sub-app-id 或设置环境变量 TENCENTCLOUD_VOD_SUB_APP_ID")
        sys.exit(1)
    req.SubAppId = args.sub_app_id
    req.FileId = args.file_id

    # 可选参数：大模型理解模板 ID，默认 100
    if args.definition is not None:
        req.Definition = args.definition

    # dry-run 模式（不需要认证）
    if args.dry_run:
        print("[DRY RUN] 请求参数:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return None

    client = get_client(args.region)

    try:
        resp = client.ImportMediaKnowledge(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get("TaskId", "N/A")
        request_id = result.get("RequestId", "N/A")

        print(f"✅ 导入媒体知识库任务已提交!")
        print(f"  TaskId:    {task_id}")
        print(f"  RequestId: {request_id}")
        print(f"  FileId:    {args.file_id}")
        print(f"  SubAppId:  {args.sub_app_id}")
        if args.definition is not None:
            desc = DEFINITION_TEMPLATES.get(args.definition, "自定义模板")
            print(f"  Definition: {args.definition} ({desc})")

        # 等待任务完成
        if not args.no_wait and task_id != "N/A":
            wait_result = wait_for_task(client, task_id, args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {task_id}")

        if args.json:
            print("\n完整响应:")
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        error_msg = str(e)
        print(f"❌ 导入媒体知识库失败: {error_msg}")
        sys.exit(1)


def wait_for_task(client, task_id, sub_app_id=None, max_wait=600):
    """等待任务完成

    通过 DescribeTaskDetail 轮询任务状态。

    Args:
        client: VOD 客户端
        task_id: 任务 ID
        sub_app_id: 子应用 ID
        max_wait: 最大等待时间（秒），默认 600
    """
    print(f"\n⏳ 等待任务完成 (TaskId: {task_id})...")
    start_time = time.time()
    poll_interval = 5  # 初始轮询间隔 5 秒

    while time.time() - start_time < max_wait:
        try:
            req = models.DescribeTaskDetailRequest()
            req.TaskId = task_id
            if sub_app_id:
                req.SubAppId = sub_app_id

            resp = client.DescribeTaskDetail(req)
            result = json.loads(resp.to_json_string())

            status = result.get("Status", "PROCESSING")
            elapsed = int(time.time() - start_time)
            print(f"  [{elapsed}s] 状态: {status}")

            if status == "FINISH":
                print("✅ 任务完成!")

                # 尝试输出任务结果
                task_result = result.get("ImportMediaKnowledgeTask") or result.get("Output")
                if task_result:
                    print("\n任务结果:")
                    print(json.dumps(task_result, indent=2, ensure_ascii=False))

                return result

            elif status == "FAIL":
                err_code = result.get("ErrCode", "N/A")
                err_msg = result.get("Message", "未知错误")
                print(f"❌ 任务失败!")
                print(f"  错误码: {err_code}")
                print(f"  错误信息: {err_msg}")
                return result

            # 动态调整轮询间隔
            if elapsed > 60:
                poll_interval = 15
            elif elapsed > 30:
                poll_interval = 10

            time.sleep(poll_interval)

        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
            print(f"  查询任务状态失败: {e}")
            time.sleep(poll_interval)

    elapsed = int(time.time() - start_time)
    print(f"⏱️ 等待超时（{elapsed}秒），任务仍在执行中")
    print(f"  可使用以下命令手动查询任务状态:")
    print(f"  python scripts/vod_describe_task.py --task-id {task_id}")
    return None


def batch_import(args):
    """批量导入多个媒体文件到知识库"""
    if not args.sub_app_id:
        print("错误：必须指定 --sub-app-id 或设置环境变量 TENCENTCLOUD_VOD_SUB_APP_ID")
        sys.exit(1)
    client = get_client(args.region)

    file_ids = args.file_ids
    success_count = 0
    fail_count = 0
    results = []

    print(f"📦 批量导入 {len(file_ids)} 个媒体文件到知识库...")
    print(f"  SubAppId:  {args.sub_app_id}")
    if args.definition is not None:
        desc = DEFINITION_TEMPLATES.get(args.definition, "自定义模板")
        print(f"  Definition: {args.definition} ({desc})")
    print()

    for i, file_id in enumerate(file_ids, 1):
        print(f"[{i}/{len(file_ids)}] FileId: {file_id}")

        req = models.ImportMediaKnowledgeRequest()
        req.SubAppId = args.sub_app_id
        req.FileId = file_id
        if args.definition is not None:
            req.Definition = args.definition

        if args.dry_run:
            print(f"  [DRY RUN] 跳过")
            continue

        try:
            resp = client.ImportMediaKnowledge(req)
            result = json.loads(resp.to_json_string())
            task_id = result.get("TaskId", "N/A")
            print(f"  ✅ 提交成功 (TaskId: {task_id})")
            success_count += 1
            results.append({"file_id": file_id, "task_id": task_id, "status": "success"})
        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
            print(f"  ❌ 提交失败: {e}")
            fail_count += 1
            results.append({"file_id": file_id, "error": str(e), "status": "failed"})

    print(f"\n📊 批量导入结果: 成功 {success_count}/{len(file_ids)}，失败 {fail_count}/{len(file_ids)}")

    if args.json:
        print("\n完整结果:")
        print(json.dumps(results, indent=2, ensure_ascii=False))

    return results


def list_templates(args):
    """列出可用的大模型理解模板"""
    print("可用的大模型理解模板 (Definition):")
    print()
    for def_id, desc in DEFINITION_TEMPLATES.items():
        print(f"  {def_id}: {desc}")
    print()
    print("说明：")
    print("  - 模板 100 为默认模板，包含音频级别的摘要和 ASR（语音识别）")
    print("  - 如需使用自定义模板，请通过 --definition 参数指定模板 ID")
    print("  - 更多模板信息请参考 API 文档：https://cloud.tencent.com/document/api/266/126286")


def main():
    parser = argparse.ArgumentParser(
        description='VOD 导入媒体知识库工具 —— 对视频进行大模型内容理解，将理解结果存入知识库，以供后续语义搜索查询',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 导入单个媒体到知识库（使用默认模板 100）
  python vod_import_media_knowledge.py import \\
      --sub-app-id 1500046806 \\
      --file-id 5285485487985271487

  # 指定大模型理解模板
  python vod_import_media_knowledge.py import \\
      --sub-app-id 1500046806 \\
      --file-id 5285485487985271487 \\
      --definition 100

  # 默认等待任务完成
  python vod_import_media_knowledge.py import \\
      --sub-app-id 1500046806 \\
      --file-id 5285485487985271487
  
  # 不等待，仅提交任务
  python vod_import_media_knowledge.py import \\
      --sub-app-id 1500046806 \\
      --file-id 5285485487985271487 \\
      --no-wait

  # 批量导入多个媒体
  python vod_import_media_knowledge.py batch \\
      --sub-app-id 1500046806 \\
      --file-ids 528548548798527148 528548548798527149 528548548798527150

  # 预览请求参数（不实际执行）
  python vod_import_media_knowledge.py import \\
      --sub-app-id 1500046806 \\
      --file-id 5285485487985271487 \\
      --dry-run

  # 列出可用模板
  python vod_import_media_knowledge.py templates
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # ---- import 子命令（单个导入）----
    import_parser = subparsers.add_parser('import', help='导入单个媒体到知识库')
    import_parser.add_argument('--sub-app-id', type=int,
                               default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                               help='点播应用 ID（必填，也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    import_parser.add_argument('--file-id', required=True,
                               help='媒体文件 ID（必填）')
    import_parser.add_argument('--definition', type=int, default=100,
                               help='大模型理解模板 ID（默认 100，包含音频级别的摘要和 ASR）')
    import_parser.add_argument('--region', default='ap-guangzhou',
                               help='地域，默认 ap-guangzhou')
    import_parser.add_argument('--no-wait', action='store_true',
                               help='仅提交任务，不等待结果')
    import_parser.add_argument('--max-wait', type=int, default=600,
                               help='最大等待时间(秒)，默认 600')
    import_parser.add_argument('--json', action='store_true',
                               help='JSON 格式输出完整响应')
    import_parser.add_argument('--dry-run', action='store_true',
                               help='预览请求参数，不实际执行')

    # ---- batch 子命令（批量导入）----
    batch_parser = subparsers.add_parser('batch', help='批量导入多个媒体到知识库')
    batch_parser.add_argument('--sub-app-id', type=int,
                              default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                              help='点播应用 ID（必填，也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    batch_parser.add_argument('--file-ids', nargs='+', required=True,
                              help='媒体文件 ID 列表（必填，空格分隔）')
    batch_parser.add_argument('--definition', type=int, default=100,
                              help='大模型理解模板 ID（默认 100，包含音频级别的摘要和 ASR）')
    batch_parser.add_argument('--region', default='ap-guangzhou',
                              help='地域，默认 ap-guangzhou')
    batch_parser.add_argument('--json', action='store_true',
                              help='JSON 格式输出完整结果')
    batch_parser.add_argument('--dry-run', action='store_true',
                              help='预览请求参数，不实际执行')

    # ---- templates 子命令 ----
    templates_parser = subparsers.add_parser('templates', help='列出可用的大模型理解模板')  # NOCA:unused-variable(variable reserved for future use)  # NOCA:line-too-long(content cannot be shortened)

    args = parser.parse_args()

    if args.command == 'import':
        import_media_knowledge(args)
    elif args.command == 'batch':
        batch_import(args)
    elif args.command == 'templates':
        list_templates(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
