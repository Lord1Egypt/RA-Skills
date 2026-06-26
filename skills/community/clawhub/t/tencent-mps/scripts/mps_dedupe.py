#!/usr/bin/env python3
"""
腾讯云 MPS 视频去重脚本

功能：
  调用 MPS VideoRemake 能力，通过修改视频画面规避平台重复内容检测。
  底层使用 AiAnalysisTask.Definition=29（视频去重预设模板）。

  API 文档：https://cloud.tencent.com/document/product/862/124394

支持的去重模式（--mode，默认 PicInPic）：
  PicInPic         画中画：将原视频缩小嵌入新背景
  BackgroundExtend 视频扩展：在场景切换处插入扩展画面
  VerticalExtend   垂直填充：在视频上下方向添加填充内容
  HorizontalExtend 水平填充：在视频左右方向添加填充内容

用法：
  # 最简用法（默认 PicInPic 模式，自动等待完成）
  python scripts/mps_dedupe.py --url https://example.com/video.mp4

  # 指定去重模式
  python scripts/mps_dedupe.py --url https://example.com/video.mp4 \\
      --mode VerticalExtend

  # COS 输入（推荐）
  python scripts/mps_dedupe.py --cos-input-key /input/video.mp4

  # 异步提交（不等待）
  python scripts/mps_dedupe.py --url https://example.com/video.mp4 --no-wait

  # dry-run 预览（含 ExtendedParameter）
  python scripts/mps_dedupe.py --url https://example.com/video.mp4 --dry-run
"""

import sys
from mps_auto_upgrade import check_sdk_version
import os
import json
import time
import argparse

_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _script_dir)

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
try:
    import mps_load_env as _le
    _le.load_env_files()
except Exception:
    pass

check_sdk_version()
try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.mps.v20190612 import mps_client, models
except ImportError:
    print("错误: 未安装腾讯云 SDK，请运行: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)

try:
    from mps_poll_task import auto_upload_local_file
    _POLL_AVAILABLE = True
except ImportError:
    _POLL_AVAILABLE = False

try:
    from qcloud_cos import CosConfig, CosS3Client
    _COS_SDK_AVAILABLE = True
except ImportError:
    _COS_SDK_AVAILABLE = False

# ─────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────
DEFAULT_REGION     = os.environ.get("TENCENTCLOUD_API_REGION", "")
DEFAULT_DEFINITION = 29    # 视频去重预设模板 ID
DEFAULT_MODE       = "PicInPic"
POLL_INTERVAL      = 15    # 轮询间隔（秒）
POLL_TIMEOUT       = 3600  # 最大等待时间（秒）

VALID_MODES = [
    "PicInPic", "BackgroundExtend", "VerticalExtend", "HorizontalExtend",
]

MODE_CN = {
    "PicInPic":         "画中画",
    "BackgroundExtend": "视频扩展",
    "VerticalExtend":   "垂直填充",
    "HorizontalExtend": "水平填充",
}

# ─────────────────────────────────────────────
# SDK 客户端
# ─────────────────────────────────────────────

def get_client(region: str = DEFAULT_REGION):
    secret_id  = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        print("错误: 请设置 TENCENTCLOUD_SECRET_ID 和 TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
        sys.exit(1)
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(credential.Credential(secret_id, secret_key), region, client_profile)

# ─────────────────────────────────────────────
# COS 输出辅助函数
# ─────────────────────────────────────────────

def get_cos_bucket():
    """从环境变量获取 COS Bucket 名称。"""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """从环境变量获取 COS Bucket 区域。"""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def build_output_storage(args):
    """
    构建输出存储信息。

    优先级：
    1. 命令行参数 --output-bucket / --output-region
    2. 环境变量 TENCENTCLOUD_COS_BUCKET / TENCENTCLOUD_COS_REGION
    """
    bucket = args.output_bucket or get_cos_bucket()
    region = args.output_region or get_cos_region()

    if bucket and region:
        return {
            "Type": "COS",
            "CosOutputStorage": {
                "Bucket": bucket,
                "Region": region
            }
        }
    return None


# ─────────────────────────────────────────────
# 构建 ExtendedParameter
# ─────────────────────────────────────────────

def build_extended_parameter(mode: str) -> str:
    """
    构建 AiAnalysisTask.ExtendedParameter 的 JSON 字符串。
    参考：https://cloud.tencent.com/document/product/862/124394
    """
    return json.dumps({"vremake": {"mode": mode}}, ensure_ascii=False)

# ─────────────────────────────────────────────
# 创建任务
# ─────────────────────────────────────────────

def create_task(client, args) -> str:
    """提交视频去重任务，返回 TaskId。"""
    req = models.ProcessMediaRequest()

    # 输入源
    input_info = models.MediaInputInfo()
    if args.url:
        input_info.Type = "URL"
        url_input = models.UrlInputInfo()
        url_input.Url = args.url
        input_info.UrlInputInfo = url_input
    elif args.cos_input_key:
        input_info.Type = "COS"
        cos_input = models.CosInputInfo()
        bucket = args.cos_input_bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
        cos_region = args.cos_input_region or os.environ.get("TENCENTCLOUD_COS_REGION", args.region)
        if not bucket:
            print("错误: 使用 COS 输入时请指定 --cos-input-bucket 或设置 TENCENTCLOUD_COS_BUCKET 环境变量", file=sys.stderr)
            sys.exit(1)
        cos_input.Bucket = bucket
        cos_input.Region = cos_region
        cos_input.Object = args.cos_input_key if args.cos_input_key.startswith("/") else f"/{args.cos_input_key}"
        input_info.CosInputInfo = cos_input
    else:
        print("错误: 请提供 --url 或 --cos-input-key", file=sys.stderr)
        sys.exit(1)

    req.InputInfo = input_info

    # 输出存储
    output_storage = build_output_storage(args)
    if output_storage:
        out_storage_obj = models.TaskOutputStorage()
        out_storage_obj.Type = output_storage["Type"]
        cos_out = models.CosOutputStorage()
        cos_out.Bucket = output_storage["CosOutputStorage"]["Bucket"]
        cos_out.Region = output_storage["CosOutputStorage"]["Region"]
        out_storage_obj.CosOutputStorage = cos_out
        req.OutputStorage = out_storage_obj
    req.OutputDir = getattr(args, "output_cos_dir", None) or "/output/dedupe/"

    # AiAnalysisTask
    ai_task = models.AiAnalysisTaskInput()
    ai_task.Definition = args.definition
    ai_task.ExtendedParameter = build_extended_parameter(args.mode)
    req.AiAnalysisTask = ai_task

    resp = client.ProcessMedia(req)
    return resp.TaskId

# ─────────────────────────────────────────────
# 查询任务
# ─────────────────────────────────────────────

def query_task(client, task_id: str) -> dict:
    req = models.DescribeTaskDetailRequest()
    req.TaskId = task_id
    resp = client.DescribeTaskDetail(req)
    return json.loads(resp.to_json_string())

def poll_task(client, task_id: str, timeout: int = POLL_TIMEOUT) -> dict:
    start = time.time()
    print(f"⏳ 等待任务完成: {task_id}")
    while True:
        result = query_task(client, task_id)
        status = result.get("Status", "")
        if status in ("FINISH", "FAIL"):
            elapsed = int(time.time() - start)
            icon = "✅" if status == "FINISH" else "❌"
            print(f"{icon} 任务{status}，耗时 {elapsed}s")
            return result
        if time.time() - start > timeout:
            print(f"⚠️  超时（{timeout}s），任务仍在处理", file=sys.stderr)
            return result
        elapsed = int(time.time() - start)
        print(f"   [{elapsed}s] 状态: {status}，继续等待...")
        time.sleep(POLL_INTERVAL)

# ─────────────────────────────────────────────
# 结果解析
# ─────────────────────────────────────────────

def extract_result(task_detail: dict) -> dict:
    """从 WorkflowTask.AiAnalysisResultSet 中提取 VideoRemake 结果"""
    wf = task_detail.get("WorkflowTask", {}) or {}
    out = {
        "task_id":     wf.get("TaskId", task_detail.get("TaskId", "")),
        "status":      wf.get("Status", task_detail.get("Status", "")),
        "create_time": task_detail.get("CreateTime", ""),
        "finish_time": task_detail.get("FinishTime", ""),
        "remake":      None,
        "error":       None,
    }
    for item in wf.get("AiAnalysisResultSet", []):
        if item.get("Type") == "VRemake":
            vr = item.get("VideoRemakeTask", {}) or {}
            if vr.get("ErrCode", 0) != 0:
                out["error"] = {"code": vr["ErrCode"], "message": vr.get("Message", "")}
            else:
                task_out = vr.get("Output", {}) or {}
                out["remake"] = {
                    "output_object_path": task_out.get("Path", ""),
                    "output_storage":     task_out.get("OutputStorage", {}),
                    "progress":           vr.get("Progress", 0),
                    "begin_time":         vr.get("BeginProcessTime", ""),
                    "finish_time":        vr.get("FinishTime", ""),
                }
            break
    return out

def print_result(result: dict, as_json: bool = False, output_dir: str = None):
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        sep = "=" * 60
        print(f"\n{sep}")
        print(f"任务 ID : {result['task_id']}")
        print(f"状态    : {result['status']}")
        print(f"完成时间: {result.get('finish_time', '-')}")
        if result.get("error"):
            err = result["error"]
            print(f"\n❌ 错误: [{err['code']}] {err['message']}")
        elif result.get("remake"):
            r = result["remake"]
            print(f"\n✅ 去重完成（进度: {r['progress']}%）")
            if r.get("output_object_path"):
                out_path = r["output_object_path"]
                print(f"   输出路径: {out_path}")
                out_storage = r.get("output_storage") or {}
                out_type = out_storage.get("Type", "")
                if out_type == "COS" and _COS_SDK_AVAILABLE:
                    cos_out = out_storage.get("CosOutputStorage", {}) or {}
                    bucket = cos_out.get("Bucket", "")
                    region = cos_out.get("Region", "")
                    if bucket and region:
                        try:
                            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
                            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
                            cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
                            cos_client = CosS3Client(cos_config)
                            signed_url = cos_client.get_presigned_url(
                                Bucket=bucket,
                                Key=out_path.lstrip("/"),
                                Method="GET",
                                Expired=3600
                            )
                            print(f"   🔗 下载链接（预签名，1小时有效）: {signed_url}")
                        except Exception as e:
                            print(f"   ⚠️  生成预签名 URL 失败: {e}")
        else:
            print("\n⚠️  暂无结果（任务可能仍在处理中）")
        print(f"{sep}\n")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        fname = f"dedupe_{result['task_id'].replace('/', '_')}.json"
        fpath = os.path.join(output_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"结果已保存: {fpath}")

# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    parser = argparse.ArgumentParser(
        description="腾讯云 MPS 视频去重（VideoRemake）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # 输入源（二选一）
    input_grp = parser.add_mutually_exclusive_group()
    input_grp.add_argument("--local-file", help="本地文件路径，自动上传到 COS 后处理（需配置 TENCENTCLOUD_COS_BUCKET）")
    input_grp.add_argument("--url",        help="视频 URL（HTTP/HTTPS）")

    # COS 路径输入
    parser.add_argument("--cos-input-bucket", help="输入文件所在 COS Bucket 名称")
    parser.add_argument("--cos-input-region", help="输入文件所在 COS Region（如 ap-guangzhou）")
    parser.add_argument("--cos-input-key",    help="输入文件的 COS Key（如 /input/video.mp4）")

    # 去重模式（默认 PicInPic）
    parser.add_argument(
        "--mode", choices=VALID_MODES, default=DEFAULT_MODE,
        help=f"去重模式（默认 {DEFAULT_MODE}）：" + " / ".join(f"{m}({MODE_CN[m]})" for m in VALID_MODES),
    )

    # 任务参数
    parser.add_argument("--definition", type=int, default=DEFAULT_DEFINITION,
                        help=f"AiAnalysisTask 模板 ID（默认 {DEFAULT_DEFINITION}）")
    parser.add_argument("--region", default=DEFAULT_REGION,
                        help=f"地域（默认 {DEFAULT_REGION}）")

    # 输出控制
    parser.add_argument("--output-bucket",  dest="output_bucket",  help="输出 COS Bucket 名称（默认取 TENCENTCLOUD_COS_BUCKET 环境变量）")
    parser.add_argument("--output-region",  dest="output_region",  help="输出 COS Bucket 区域（默认取 TENCENTCLOUD_COS_REGION 环境变量）")
    parser.add_argument("--output-cos-dir", dest="output_cos_dir", help="COS 输出目录（默认 /output/dedupe/），以 / 开头和结尾")
    parser.add_argument("--no-wait",    action="store_true", help="异步模式：只提交任务，不等待结果")
    parser.add_argument("--json",       action="store_true", dest="json_output", help="JSON 格式输出")
    parser.add_argument("--output-dir", help="将结果 JSON 保存到指定本地目录")
    parser.add_argument("--dry-run",    action="store_true", help="只打印参数预览（含 ExtendedParameter），不调用 API")
    parser.add_argument("--download-dir", type=str, default=None,
                        help="任务完成后自动下载结果到指定目录（默认：不下载）")

    args = parser.parse_args()

    # 自动加载环境变量（入口处立即执行）
    if _LOAD_ENV_AVAILABLE:
        try:
            _ensure_env_loaded(verbose=getattr(args, "verbose", False))
        except SystemExit:
            raise
        except Exception as e:
            if getattr(args, "verbose", False):
                print(f"⚠️  自动加载 env 失败：{e}", file=sys.stderr)

    # --url 本地路径自动转换
    if getattr(args, 'url', None) and not getattr(args, 'local_file', None):
        _val = args.url
        if not _val.startswith('http://') and not _val.startswith('https://'):
            print(f"提示：'{_val}' 未指定来源，默认按本地文件处理", file=sys.stderr)
            args.local_file = _val
            args.url = None

    # --local-file 与 COS 输入参数互斥
    if getattr(args, 'local_file', None):
        cos_conflicts = [x for x in [
            getattr(args, 'cos_input_bucket', None), getattr(args, 'cos_input_key', None)
        ] if x]
        if cos_conflicts:
            parser.error("--local-file 不能与 --cos-input-bucket / --cos-input-key 同时使用")

    # 本地文件自动上传
    if getattr(args, 'local_file', None):
        if not _POLL_AVAILABLE:
            print("错误：--local-file 需要 mps_poll_task 模块支持", file=sys.stderr)
            sys.exit(1)
        upload_result = auto_upload_local_file(args.local_file)
        if not upload_result:
            sys.exit(1)
        args.cos_input_key = upload_result["Key"]
        args.cos_input_bucket = upload_result["Bucket"]
        args.cos_input_region = upload_result["Region"]

    # ── dry-run ──
    if args.dry_run:
        print("🔍 dry-run 参数预览:")
        if args.url:
            src = f"URL={args.url}"
        elif args.cos_input_key:
            bucket = args.cos_input_bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
            region = args.cos_input_region or os.environ.get("TENCENTCLOUD_COS_REGION", args.region)
            src = f"COS={bucket}/{region}{args.cos_input_key}"
        else:
            src = "未指定"
        print(f"  输入       = {src}")
        print(f"  mode       = {args.mode}（{MODE_CN.get(args.mode, '?')}）")
        print(f"  definition = {args.definition}")
        print(f"  region     = {args.region}")
        print(f"  no-wait    = {args.no_wait}")
        if args.url or args.cos_input_key:
            ep = build_extended_parameter(args.mode)
            print(f"\n  ExtendedParameter =\n  {ep}")
        return

    client = get_client(args.region)

    # ── 提交任务 ──
    has_input = bool(args.url) or bool(args.cos_input_key)
    if not has_input:
        parser.error("请提供 --url 或 --cos-input-key")

    if args.url:
        src = f"URL={args.url}"
    else:
        bucket = args.cos_input_bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
        region = args.cos_input_region or os.environ.get("TENCENTCLOUD_COS_REGION", args.region)
        src = f"COS={bucket}/{region}{args.cos_input_key}"

    mode_cn = MODE_CN.get(args.mode, args.mode)
    print(f"🚀 提交视频去重任务")
    print(f"   输入  : {src}")
    print(f"   模式  : {args.mode}（{mode_cn}）")
    print(f"   模板  : {args.definition}  地域: {args.region}")

    try:
        task_id = create_task(client, args)
        print("✅ 视频去重任务提交成功！")
        print(f"   TaskId: {task_id}")
        print(f"\n## TaskId: {task_id}")
    except TencentCloudSDKException as e:
        print(f"❌ 提交失败: {e}", file=sys.stderr)
        sys.exit(1)

    # ── 异步模式（--no-wait） ──
    if args.no_wait:
        result = {
            "task_id": task_id,
            "status":  "PROCESSING",
            "message": "任务已提交，使用 mps_get_video_task.py --task-id 查询结果",
        }
        print_result(result, as_json=args.json_output, output_dir=args.output_dir)
        return

    # ── 等待完成（默认） ──
    try:
        detail = poll_task(client, task_id)
        result = extract_result(detail)
        print_result(result, as_json=args.json_output, output_dir=args.output_dir)

        # --download-dir：下载输出视频到本地目录
        download_dir = getattr(args, 'download_dir', None)
        if download_dir and result.get("remake") and not result.get("error"):
            remake = result["remake"]
            out_path = remake.get("output_object_path", "")
            out_storage = remake.get("output_storage") or {}
            out_type = out_storage.get("Type", "")
            if out_type == "COS" and out_path:
                cos_out = out_storage.get("CosOutputStorage", {}) or {}
                bucket = cos_out.get("Bucket", "")
                region = cos_out.get("Region", "")
                if bucket and region:
                    os.makedirs(download_dir, exist_ok=True)
                    filename = os.path.basename(out_path.lstrip("/"))
                    local_path = os.path.join(download_dir, filename)
                    print(f"\n📥 下载输出视频到: {local_path}")
                    try:
                        secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
                        secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
                        cos_config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
                        cos_client = CosS3Client(cos_config)
                        cos_client.download_file(Bucket=bucket, Key=out_path.lstrip("/"), DestFilePath=local_path)
                        size = os.path.getsize(local_path)
                        print(f"   ✅ 下载成功 ({size / 1024 / 1024:.2f} MB): {local_path}")
                    except Exception as e:
                        print(f"   ❌ 下载失败: {e}")
        if result.get("status") == "FAIL":
            sys.exit(1)
    except TencentCloudSDKException as e:
        print(f"❌ 查询失败: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
