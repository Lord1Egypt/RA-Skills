#!/usr/bin/env python3
"""
腾讯云 MPS 视频二次创作脚本

功能：
  调用 MPS VideoRemake 能力，对视频进行二次创作处理（换脸/换人/视频交错等）。
  通过 ExtendedParameter 的 vremake 参数控制创作模式。

  API 文档：https://cloud.tencent.com/document/product/862/124394
  接口：ProcessMedia → AiAnalysisTask.Definition=29（视频二次创作模板）

  ⚠️  视频去重（画中画/视频扩展/垂直填充/水平填充）请使用 mps_dedupe.py。

支持的创作模式（--mode）：
  AB               视频交错：AB 视频交错模式
  SwapFace         换脸：视频人脸替换（需提供 --src-faces 和 --dst-faces）
  SwapCharacter    换人：视频人物替换（需提供 --src-character 和 --dst-character）

用法：
  # 换脸模式（默认自动等待完成）
  python scripts/mps_vremake.py \\
      --url https://example.com/video.mp4 \\
      --mode SwapFace \\
      --src-faces https://example.com/src.png \\
      --dst-faces https://example.com/dst.png

  # 换人模式
  python scripts/mps_vremake.py \\
      --url https://example.com/video.mp4 \\
      --mode SwapCharacter \\
      --src-character https://example.com/src_person.png \\
      --dst-character https://example.com/dst_person.png

  # 视频交错（AB 模式）
  python scripts/mps_vremake.py \\
      --url https://example.com/video.mp4 \\
      --mode AB

  # 异步提交（不等待）
  python scripts/mps_vremake.py \\
      --url https://example.com/video.mp4 \\
      --mode SwapFace \\
      --src-faces https://example.com/src.png \\
      --dst-faces https://example.com/dst.png \\
      --no-wait

  # 查询已有任务结果
  python scripts/mps_get_video_task.py --task-id 1234567890-WorkflowTask-xxxxx

  # dry-run 预览（含 ExtendedParameter）
  python scripts/mps_vremake.py \\
      --url https://example.com/video.mp4 \\
      --mode SwapFace \\
      --src-faces https://example.com/src.png \\
      --dst-faces https://example.com/dst.png \\
      --dry-run
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
except Exception:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
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
DEFAULT_DEFINITION = 29    # 视频二次创作模板 ID（官方）
POLL_INTERVAL      = 15    # 轮询间隔（秒）
POLL_TIMEOUT       = 3600  # 最大等待时间（秒）

VALID_MODES = [
    "AB", "SwapFace", "SwapCharacter",
]

MODE_CN = {
    "AB":               "视频交错",
    "SwapFace":         "换脸",
    "SwapCharacter":    "换人",
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

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def build_extended_parameter(args) -> str:
    """
    构建 AiAnalysisTask.ExtendedParameter 的 JSON 字符串。

    结构示例：
      {"vremake": {"mode": "SwapFace", "swapFace": {"srcFaces": [...], "dstFaces": [...]}}}
    """
    mode = args.mode
    vremake: dict = {"mode": mode}

    if mode == "AB":
        ext_params: dict = {}
        if args.llm_video_prompt:
            ext_params["llmVideoPrompt"] = args.llm_video_prompt
        elif args.llm_prompt:
            ext_params["llmPrompt"] = args.llm_prompt
        if args.random_flip is not None:
            ext_params["randomFlip"] = args.random_flip
        if args.random_cut:
            ext_params["randomCut"] = True
        if args.random_speed:
            ext_params["randomSpeed"] = True
        if args.ext_mode is not None:
            ext_params["extMode"] = args.ext_mode
        if ext_params:
            vremake["AB"] = ext_params

    elif mode == "SwapFace":
        if not args.src_faces or not args.dst_faces:
            print("错误: SwapFace 模式需要提供 --src-faces 和 --dst-faces", file=sys.stderr)
            sys.exit(1)
        if len(args.src_faces) != len(args.dst_faces):
            print("错误: --src-faces 和 --dst-faces 数量必须一致", file=sys.stderr)
            sys.exit(1)
        vremake["swapFace"] = {
            "srcFaces": args.src_faces,
            "dstFaces": args.dst_faces,
        }

    elif mode == "SwapCharacter":
        if not args.src_character or not args.dst_character:
            print("错误: SwapCharacter 模式需要提供 --src-character 和 --dst-character", file=sys.stderr)
            sys.exit(1)
        vremake["swapCharacter"] = {
            "srcCharacter": args.src_character,
            "character":    args.dst_character,
        }

    # 支持 --custom-json 合并
    if args.custom_json:
        try:
            custom = json.loads(args.custom_json)
            # 若 custom 包含 vremake 字段，深度合并
            if "vremake" in custom:
                for k, v in custom["vremake"].items():
                    if k != "mode":
                        vremake[k] = v
            else:
                # 直接合并到 vremake
                vremake.update(custom)
        except json.JSONDecodeError as e:
            print(f"错误: --custom-json 格式错误: {e}", file=sys.stderr)
            sys.exit(1)

    return json.dumps({"vremake": vremake}, ensure_ascii=False)


# ─────────────────────────────────────────────
# 创建任务
# ─────────────────────────────────────────────

def create_task(client, args) -> str:
    """提交视频二次创作任务，返回 TaskId。"""
    req = models.ProcessMediaRequest()

    # 输入源
    input_info = models.MediaInputInfo()
    if args.url:
        input_info.Type = "URL"
        url_input = models.UrlInputInfo()
        url_input.Url = args.url
        input_info.UrlInputInfo = url_input
    elif args.cos_input_key:
        # 新版 COS 路径输入（--cos-input-bucket + --cos-input-region + --cos-input-key）
        input_info.Type = "COS"
        cos_input = models.CosInputInfo()
        bucket = args.cos_input_bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
        cos_region = args.cos_input_region or os.environ.get("TENCENTCLOUD_COS_REGION", args.region)
        if not bucket:
            print("错误: 使用 COS 输入时请指定 --cos-input-bucket 或设置 TENCENTCLOUD_COS_BUCKET 环境变量", file=sys.stderr)
            sys.exit(1)
        cos_input.Bucket = bucket
        cos_input.Region = cos_region
        # 确保 key 以 / 开头
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
    req.OutputDir = getattr(args, "output_cos_dir", None) or "/output/vremake/"

    # AiAnalysisTask
    ai_task = models.AiAnalysisTaskInput()
    ai_task.Definition = args.definition
    ai_task.ExtendedParameter = build_extended_parameter(args)
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
            print(f"\n✅ 二创完成（进度: {r['progress']}%）")
            if r.get("output_object_path"):
                out_path = r["output_object_path"]
                print(f"   输出路径: {out_path}")
                # 尝试生成预签名下载链接
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
                        except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
                            print(f"   ⚠️  生成预签名 URL 失败: {e}")
        else:
            print("\n⚠️  暂无结果（任务可能仍在处理中）")
        print(f"{sep}\n")

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        fname = f"vremake_{result['task_id'].replace('/', '_')}.json"
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
        description="腾讯云 MPS 视频二次创作（VideoRemake）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # 输入源（二选一）
    input_grp = parser.add_mutually_exclusive_group()
    input_grp.add_argument("--local-file", help="本地文件路径，自动上传到 COS 后处理（需配置 TENCENTCLOUD_COS_BUCKET）")
    input_grp.add_argument("--url",        help="视频 URL（HTTP/HTTPS）")

    # COS 路径输入（新版，与 mps_transcode.py 等保持一致）
    parser.add_argument("--cos-input-bucket", help="输入文件所在 COS Bucket 名称")
    parser.add_argument("--cos-input-region", help="输入文件所在 COS Region（如 ap-guangzhou）")
    parser.add_argument("--cos-input-key",    help="输入文件的 COS Key（如 /input/video.mp4）")

    # 创作模式
    parser.add_argument(
        "--mode", choices=VALID_MODES,
        help="创作模式（提交任务时必填）：" + " / ".join(f"{m}({MODE_CN[m]})" for m in VALID_MODES),
    )

    # 换脸/换人参数
    parser.add_argument("--src-faces",      nargs="+", metavar="URL", help="[SwapFace] 原视频中人脸 URL 列表")
    parser.add_argument("--dst-faces",      nargs="+", metavar="URL", help="[SwapFace] 目标人脸 URL 列表（与 --src-faces 一一对应）")
    parser.add_argument("--src-character",  metavar="URL", help="[SwapCharacter] 原视频人物 URL（正面全身图）")
    parser.add_argument("--dst-character",  metavar="URL", help="[SwapCharacter] 目标人物 URL（正面全身图）")

    # AB 模式参数
    parser.add_argument("--llm-prompt",       metavar="TEXT", help="大模型提示词（AB 模式）")
    parser.add_argument("--llm-video-prompt", metavar="TEXT", help="大模型提示词（生成背景视频，优先于 --llm-prompt）")
    parser.add_argument("--random-cut",       action="store_true", help="随机裁剪")
    parser.add_argument("--random-speed",     action="store_true", help="随机加速")
    parser.add_argument("--random-flip",      type=lambda x: x.lower() != "false",
                        metavar="true/false", help="随机镜像（默认 true）")
    parser.add_argument("--ext-mode",         type=int, choices=[1, 2, 3], help="扩展模式 1/2/3（AB）")
    parser.add_argument("--custom-json",      metavar="JSON", help="自定义 vremake 扩展参数 JSON（与 --mode 合并）")

    # 任务参数
    parser.add_argument("--definition", type=int, default=DEFAULT_DEFINITION,
                        help=f"AiAnalysisTask 模板 ID（默认 {DEFAULT_DEFINITION}，即视频二次创作模板）")
    parser.add_argument("--region", default=DEFAULT_REGION,
                        help=f"地域（默认 {DEFAULT_REGION}）")

    # 输出控制
    parser.add_argument("--output-bucket",  dest="output_bucket",  help="输出 COS Bucket 名称（默认取 TENCENTCLOUD_COS_BUCKET 环境变量）")  # NOCA:line-too-long(long SDK parameter or URL string)
    parser.add_argument("--output-region",  dest="output_region",  help="输出 COS Bucket 区域（默认取 TENCENTCLOUD_COS_REGION 环境变量）")  # NOCA:line-too-long(long SDK parameter or URL string)
    parser.add_argument("--output-cos-dir", dest="output_cos_dir", help="COS 输出目录（默认 /output/vremake/），以 / 开头和结尾")
    parser.add_argument("--no-wait",    action="store_true", help="异步模式：只提交任务，不等待结果")
    parser.add_argument("--json",       action="store_true", dest="json_output", help="JSON 格式输出")
    parser.add_argument("--output-dir", help="将结果 JSON 保存到指定本地目录")
    parser.add_argument("--dry-run",    action="store_true", help="只打印参数预览（含 ExtendedParameter），不调用 API")
    parser.add_argument("--download-dir", type=str, default=None,
                        help="任务完成后自动下载结果到指定目录（默认：不下载；指定路径后自动下载）")

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
    # --url 本地路径自动转换为本地上传模式
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
        if args.mode and (args.url or args.cos_input_key):
            ep = build_extended_parameter(args)
            print(f"\n  ExtendedParameter =\n  {ep}")
        return

    client = get_client(args.region)

    # ── 提交任务 ──
    has_input = bool(args.url) or bool(args.cos_input_key)
    if not has_input:
        parser.error("请提供 --url 或 --cos-input-key")
    if not args.mode:
        parser.error("提交任务时 --mode 为必填参数")

    # 确定输入源显示
    if args.url:
        src = f"URL={args.url}"
    else:
        bucket = args.cos_input_bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
        region = args.cos_input_region or os.environ.get("TENCENTCLOUD_COS_REGION", args.region)
        src = f"COS={bucket}/{region}{args.cos_input_key}"

    mode_cn = MODE_CN.get(args.mode, args.mode)
    print(f"🚀 提交视频二次创作任务")
    print(f"   输入  : {src}")
    print(f"   模式  : {args.mode}（{mode_cn}）")
    print(f"   模板  : {args.definition}  地域: {args.region}")

    try:
        task_id = create_task(client, args)
        print("✅ 视频二次创作任务提交成功！")
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
                    import os as _os
                    _os.makedirs(download_dir, exist_ok=True)
                    filename = _os.path.basename(out_path.lstrip("/"))
                    local_path = _os.path.join(download_dir, filename)
                    print(f"\n📥 下载输出视频到: {local_path}")
                    try:
                        from qcloud_cos import CosConfig as _CosConfig, CosS3Client as _CosClient
                        import os as _os2
                        _sid = _os2.environ.get("TENCENTCLOUD_SECRET_ID", "")
                        _skey = _os2.environ.get("TENCENTCLOUD_SECRET_KEY", "")
                        _cfg = _CosConfig(Region=region, SecretId=_sid, SecretKey=_skey)
                        _client = _CosClient(_cfg)
                        _client.download_file(Bucket=bucket, Key=out_path.lstrip("/"), DestFilePath=local_path)
                        size = _os.path.getsize(local_path)
                        print(f"   ✅ 下载成功 ({size / 1024 / 1024:.2f} MB): {local_path}")
                    except Exception as e:  # NOCA:broad-except(CLI script needs to catch all SDK exceptions for user-friendly error reporting)
                        print(f"   ❌ 下载失败: {e}")
        if result.get("status") == "FAIL":
            sys.exit(1)
    except TencentCloudSDKException as e:
        print(f"❌ 查询失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
