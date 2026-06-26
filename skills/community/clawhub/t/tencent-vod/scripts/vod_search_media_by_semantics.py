#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD 语义搜索媒体脚本
使用 SearchMediaBySemantics API 对已导入知识库的媒体进行自然语言语义搜索。

核心流程：
1. 用户输入自然语言描述（如"包含夕阳的海边视频"）
2. 调用 SearchMediaBySemantics API 进行语义匹配
3. 返回匹配的媒体片段列表（含 FileId、匹配得分、片段时间范围）

前置条件：
- 媒体文件需先通过 ImportMediaKnowledge（vod_import_media_knowledge.py）导入知识库
- 导入后，大模型会对视频进行内容理解（摘要、ASR 等），理解结果存入知识库
- 本脚本基于知识库中的理解结果进行语义检索

与 SearchMedia 的区别：
- SearchMedia（vod_search_media.py）：基于元数据的条件筛选（名称、标签、分类等）
- SearchMediaBySemantics（本脚本）：基于自然语言的语义搜索，理解视频内容后匹配

API 文档：https://cloud.tencent.com/document/api/266/126287
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


# 支持的文件类型
VALID_CATEGORIES = ["Video", "Audio", "Image"]

# 支持的搜索任务类型
VALID_TASK_TYPES = [
    "AiAnalysis.DescriptionTask",
    "SmartSubtitle.AsrFullTextTask",
]


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


def format_time_offset(seconds):
    """格式化时间偏移量为可读字符串"""
    if seconds is None:
        return "N/A"
    seconds = float(seconds)
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        m = int(seconds // 60)
        s = seconds % 60
        return f"{m}m{s:.1f}s"
    else:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        return f"{h}h{m}m{s:.0f}s"


def print_search_results(results, verbose=False):
    """格式化输出搜索结果"""
    if not results:
        print("\n未找到匹配的媒体片段。")
        print("提示：请确保目标媒体已通过 ImportMediaKnowledge 导入知识库。")
        return

    # 按 FileId 分组统计
    file_ids = set()
    for r in results:
        file_ids.add(r.get("FileId", "N/A"))

    print(f"\n📋 搜索结果：共 {len(results)} 个匹配片段，涉及 {len(file_ids)} 个媒体文件")
    print("=" * 70)

    for i, result in enumerate(results, 1):
        file_id = result.get("FileId", "N/A")
        score = result.get("Score", 0)
        start = result.get("StartTimeOffset")
        end = result.get("EndTimeOffset")

        # 得分条形图
        bar_len = 20
        filled = int(score * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)

        print(f"\n  [{i}] FileId: {file_id}")
        print(f"      得分:   {score:.5f} [{bar}]")

        if start is not None and end is not None:
            duration = float(end) - float(start)
            print(f"      片段:   {format_time_offset(start)} → {format_time_offset(end)} (时长: {format_time_offset(duration)})")  # NOCA:line-too-long(long SDK parameter or URL string)
        elif start is not None:
            print(f"      起始:   {format_time_offset(start)}")

    print()


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def search_by_semantics(args):
    """执行语义搜索"""

    # 构造请求参数
    payload = {}

    # 处理 SubAppId
    sub_app_id = args.sub_app_id
    client = None

    # 通过应用名称解析 SubAppId
    if args.app_name and not args.dry_run:
        if args.sub_app_id:
            print("错误：--app-name 和 --sub-app-id 不能同时指定")
            sys.exit(1)
        client = get_client(args.region)
        sub_app_id = resolve_sub_app_id(client, args.app_name)

    if sub_app_id:
        payload["SubAppId"] = sub_app_id

    # 必填：搜索文本
    payload["Text"] = args.text

    # 可选参数
    if args.limit is not None:
        payload["Limit"] = args.limit

    if args.categories:
        payload["Categories"] = args.categories

    if args.tags:
        payload["Tags"] = args.tags

    if args.persons:
        payload["Persons"] = args.persons

    if args.task_types:
        payload["TaskTypes"] = args.task_types

    # dry-run 模式
    if args.dry_run:
        if args.app_name:
            payload["_app_name"] = args.app_name
            payload["_note"] = "app_name 将在实际执行时解析为 SubAppId"
        print("[DRY RUN] 请求参数:")
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return None

    # 构造请求
    if client is None:
        client = get_client(args.region)

    req = models.SearchMediaBySemanticsRequest()
    req.from_json_string(json.dumps(payload, ensure_ascii=False))

    try:
        resp = client.SearchMediaBySemantics(req)
        result = json.loads(resp.to_json_string())

        search_results = result.get("SearchResults", [])
        request_id = result.get("RequestId", "N/A")

        # JSON 格式输出
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return result

        # 人类可读输出
        print(f"🔍 语义搜索完成!")
        print(f"  搜索内容: \"{args.text}\"")
        print(f"  匹配数量: {len(search_results)} 个片段")
        print(f"  RequestId: {request_id}")

        if sub_app_id:
            print(f"  SubAppId: {sub_app_id}")

        if args.categories:
            print(f"  文件类型: {', '.join(args.categories)}")
        if args.tags:
            print(f"  标签过滤: {', '.join(args.tags)}")
        if args.persons:
            print(f"  人物过滤: {', '.join(args.persons)}")
        if args.task_types:
            print(f"  任务类型: {', '.join(args.task_types)}")

        print_search_results(search_results, verbose=args.verbose)

        # 使用提示
        if search_results:
            sample_file_id = search_results[0].get("FileId", "xxx")
            print("💡 后续操作提示:")
            print(f"  查看媒体详情: python scripts/vod_describe_media.py --file-id {sample_file_id}" +
                  (f" --sub-app-id {sub_app_id}" if sub_app_id else ""))

        return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        error_msg = str(e)
        print(f"❌ 语义搜索失败: {error_msg}")

        # 常见错误提示
        if "InvalidParameterValue" in error_msg:
            print("\n可能的原因：")
            print("  - 搜索文本为空或格式不正确")
            print("  - SubAppId 不正确")
        elif "ResourceNotFound" in error_msg or "KnowledgeBase" in error_msg.lower():
            print("\n可能的原因：")
            print("  - 目标媒体尚未导入知识库")
            print("  - 请先使用 vod_import_media_knowledge.py 导入媒体到知识库")

        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='VOD 语义搜索媒体工具 —— 使用自然语言搜索已导入知识库的视频内容',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
前置条件:
  媒体文件需先通过 ImportMediaKnowledge 导入知识库：
    python scripts/vod_import_media_knowledge.py import \\
        --sub-app-id 1500046806 --file-id 5285485487985271487

  导入后，大模型会对视频进行内容理解（摘要、ASR 等），
  理解结果存入知识库后，即可使用本脚本进行语义搜索。

与 SearchMedia 的区别:
  SearchMedia（vod_search_media.py）     → 基于元数据条件筛选（名称、标签等）
  SearchMediaBySemantics（本脚本）       → 基于自然语言语义搜索（理解视频内容后匹配）

示例:
  # 基础语义搜索
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "包含夕阳的海边视频"

  # 通过应用名称 + 语义搜索
  python vod_search_media_by_semantics.py \\
      --app-name "测试应用" \\
      --text "有人在跑步的画面"

  # 限制返回数量
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "会议讨论内容" \\
      --limit 5

  # 只搜索视频文件
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "猫咪玩耍" \\
      --categories Video

  # 按标签过滤
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "精彩进球" \\
      --tags "体育" "足球"

  # 按人物过滤（搜索包含指定人物的片段）
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "演讲内容" \\
      --persons "张三"

  # 指定搜索任务类型
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "产品介绍" \\
      --task-types AiAnalysis.DescriptionTask

  # JSON 格式输出
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "包含夕阳的海边视频" \\
      --json

  # 预览请求参数（不实际执行）
  python vod_search_media_by_semantics.py \\
      --sub-app-id 1500046806 \\
      --text "包含夕阳的海边视频" \\
      --dry-run
        '''
    )

    # 应用选择（互斥）
    app_group = parser.add_argument_group('应用选择')
    app_group.add_argument('--sub-app-id', type=int,
                           default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                           help='点播子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置，与 --app-name 互斥）')
    app_group.add_argument('--app-name',
                           help='通过应用名称/描述模糊匹配子应用（与 --sub-app-id 互斥）')

    # 搜索参数
    search_group = parser.add_argument_group('搜索参数')
    search_group.add_argument('--text', '-t', required=True,
                              help='搜索内容，自然语言描述（必填），如 "包含夕阳的海边视频"')
    search_group.add_argument('--limit', '-n', type=int, default=20,
                              help='返回记录条数，默认 20，范围 [1, 100]')

    # 过滤条件
    filter_group = parser.add_argument_group('过滤条件')
    filter_group.add_argument('--categories', nargs='+',
                              choices=VALID_CATEGORIES,
                              help='文件类型过滤: Video / Audio / Image')
    filter_group.add_argument('--tags', nargs='+',
                              help='标签过滤（匹配任一标签，最多16个）')
    filter_group.add_argument('--persons', nargs='+',
                              help='人物过滤（匹配所有指定人物，最多16个）')
    filter_group.add_argument('--task-types', nargs='+',
                              choices=VALID_TASK_TYPES,
                              help='搜索任务类型: AiAnalysis.DescriptionTask / SmartSubtitle.AsrFullTextTask')

    # 输出控制
    output_group = parser.add_argument_group('输出控制')
    output_group.add_argument('--verbose', '-v', action='store_true',
                              help='显示详细信息')
    output_group.add_argument('--json', action='store_true',
                              help='JSON 格式输出完整响应')
    output_group.add_argument('--region', default='ap-guangzhou',
                              help='地域，默认 ap-guangzhou')
    output_group.add_argument('--dry-run', action='store_true',
                              help='预览请求参数，不实际执行')

    args = parser.parse_args()

    # 验证 app-name 和 sub-app-id 互斥
    if args.app_name and args.sub_app_id:
        print("错误：--app-name 和 --sub-app-id 不能同时指定")
        sys.exit(1)

    # 验证必须指定应用
    if not args.sub_app_id and not args.app_name:
        print("错误：必须指定 --sub-app-id 或 --app-name")
        sys.exit(1)

    # 验证 limit 范围
    if args.limit is not None and (args.limit < 1 or args.limit > 100):
        print("错误：--limit 取值范围为 [1, 100]")
        sys.exit(1)

    search_by_semantics(args)


if __name__ == '__main__':
    main()
