#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD URL 拉取上传脚本
支持从 URL 拉取媒体文件上传到云点播
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


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def pull_upload(args):
    """URL 拉取上传"""
    client = get_client(args.region)

    # 通过应用名称解析 SubAppId
    if args.app_name:
        if args.sub_app_id:
            print("错误：--app-name 和 --sub-app-id 不能同时指定")
            sys.exit(1)
        args.sub_app_id = resolve_sub_app_id(client, args.app_name)

    req = models.PullUploadRequest()
    req.MediaUrl = args.url

    if args.media_name:
        req.MediaName = args.media_name
    if args.media_type:
        req.MediaType = args.media_type
    if args.cover_url:
        req.CoverUrl = args.cover_url
    if args.procedure:
        req.Procedure = args.procedure
    if args.expire_time:
        req.ExpireTime = args.expire_time
    if args.storage_region:
        req.StorageRegion = args.storage_region
    if args.class_id is not None:
        req.ClassId = args.class_id
    if args.tasks_priority is not None:
        req.TasksPriority = args.tasks_priority
    if args.session_context:
        req.SessionContext = args.session_context
    if args.session_id:
        req.SessionId = args.session_id
    if args.ext_info:
        req.ExtInfo = args.ext_info
    if args.source_context:
        req.SourceContext = args.source_context
    if args.media_storage_path:
        req.MediaStoragePath = args.media_storage_path
    if args.sub_app_id:
        req.SubAppId = args.sub_app_id

    if args.dry_run:
        print("[DRY RUN] 请求参数:")
        print(json.dumps(json.loads(req.to_json_string()), indent=2, ensure_ascii=False))
        return

    try:
        resp = client.PullUpload(req)
        result = json.loads(resp.to_json_string())

        print(f"拉取上传任务已提交!")
        print(f"TaskId: {result.get('TaskId', 'N/A')}")
        print(f"FileId: {result.get('FileId', 'N/A')}")

        # 如果需要等待任务完成
        if not args.no_wait and result.get('TaskId'):
            wait_result = wait_for_task(client, result['TaskId'], args.sub_app_id, args.max_wait)
            if wait_result is None:
                print(f"\n⏱️ 等待超时（{args.max_wait}秒），任务仍在执行中")
                print(f"📋 可稍后手动查询: python scripts/vod_describe_task.py --task-id {result['TaskId']}")

        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))

        return result
    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)  # NOCA:line-too-long(content cannot be shortened)
        print(f"拉取上传失败: {e}")
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

            status = result.get('Status', 'PROCESSING')
            print(f"  当前状态: {status}")

            if status == 'FINISH':
                print("任务完成!")
                pull_task = result.get('PullUploadTask') or {}
                if pull_task:
                    file_id = pull_task.get('FileId', 'N/A')
                    print(f"  FileId: {file_id}")
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
        description='VOD URL 拉取上传工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 基础拉取上传
  python vod_pull_upload.py --url "https://example.com/video.mp4"

  # 指定媒体名称和封面
  python vod_pull_upload.py --url "https://example.com/video.mp4" --media-name "我的视频" --cover-url "https://example.com/cover.jpg"

  # 拉取后自动执行任务流
  python vod_pull_upload.py --url "https://example.com/video.mp4" --procedure "SimpleAes"

  # 指定存储园区和分类
  python vod_pull_upload.py --url "https://example.com/video.mp4" --storage-region "ap-chongqing" --class-id 100

  # 设置过期时间
  python vod_pull_upload.py --url "https://example.com/video.mp4" --expire-time "2025-12-31T23:59:59Z"

  # 等待任务完成
  python vod_pull_upload.py --url "https://example.com/video.mp4"  # 默认等待完成
  
  # 不等待，仅提交任务
  python vod_pull_upload.py --url "https://example.com/video.mp4" --no-wait

  # 预览请求参数（不实际执行）
  python vod_pull_upload.py --url "https://example.com/video.mp4" --dry-run
        '''
    )

    parser.add_argument('--url', required=True, help='媒体 URL（必填）')
    parser.add_argument('--media-name', help='媒体名称')
    parser.add_argument('--media-type', help='媒体类型 (mp4, mp3, jpg等)')
    parser.add_argument('--cover-url', help='封面 URL')
    parser.add_argument('--procedure', help='任务流名称，上传完成后自动执行')
    parser.add_argument('--expire-time', help='媒体文件过期时间，ISO 8601 格式，如 2025-12-31T23:59:59Z')
    parser.add_argument('--storage-region', help='指定存储园区，如 ap-chongqing')
    parser.add_argument('--class-id', type=int, help='分类 ID，默认 0（其他分类）')
    parser.add_argument('--tasks-priority', type=int, help='任务优先级，范围 -10 到 10，默认 0')
    parser.add_argument('--session-context', help='会话上下文，透传用户请求信息，最长 1000 字符')
    parser.add_argument('--session-id', help='去重识别码，三天内相同 ID 的请求会返回错误，最长 50 字符')
    parser.add_argument('--ext-info', help='保留字段，特殊用途时使用')
    parser.add_argument('--source-context', help='来源上下文，透传用户请求信息，最长 250 字符')
    parser.add_argument('--media-storage-path', help='媒体存储路径，以 / 开头，仅 FileID+Path 模式子应用可用')
    parser.add_argument('--sub-app-id', type=int,
                        default=int(os.environ.get('TENCENTCLOUD_VOD_SUB_APP_ID', 0)) or None,
                        help='子应用 ID（也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）')
    parser.add_argument('--app-name', help='通过应用名称/描述模糊匹配子应用（与 --sub-app-id 互斥）')
    parser.add_argument('--region', default='ap-guangzhou', help='地域，默认 ap-guangzhou')
    parser.add_argument('--no-wait', action='store_true', help='仅提交任务，不等待结果')
    parser.add_argument('--max-wait', type=int, default=600, help='最大等待时间(秒)，默认 600')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出完整响应')
    parser.add_argument('--dry-run', action='store_true', help='预览请求参数，不实际执行')

    args = parser.parse_args()
    pull_upload(args)


if __name__ == '__main__':
    main()
