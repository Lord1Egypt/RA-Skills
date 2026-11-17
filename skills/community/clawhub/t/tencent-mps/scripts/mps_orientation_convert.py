#!/usr/bin/env python3
"""
腾讯云 MPS 智能横竖屏方向转换脚本

功能：
  使用 MPS 智能分析功能，实现视频画面方向的双向转换：
    · 横屏 → 竖屏（算法 2 / 3 / 5 / 6）
    · 竖屏 → 横屏（算法 7）
  转换不是简单旋转：基础版通过识别感兴趣区域（ROI）智能裁剪；
  AIGC 版则基于原视频做 AI 补全生成缺失画面。

  ⚠️ 重要提示：
  - 本脚本仅支持处理离线文件，不支持直播流
  - 输入仅支持 URL 与腾讯云 COS，**不支持 AWS S3**
  - 输入编码标准：MPEG / H.264 / H.265；封装格式：.mp4/.avi/.mkv/.mov/.mpg
  - 输出统一为 H.264 编码、.mp4 格式
  - 扩展参数统一挂在 htv 键下，禁止自行增删字段
    （htv 为官方参数名，沿用官方约定，不代表仅支持横转竖）

  底层 API：ProcessMedia（离线文件）
  固定使用智能分析 28 号预设模板（AiAnalysisTask.Definition=28），不支持自定义模板

算法类别（通过 --algorithm-type 指定，必填）：
  【横 → 竖】
  2  多模型算法与定制优化（基础版，横转竖默认推荐）
  3  精确人脸检测；出现两个人脸时上下分屏并尽量居中（基础版）
  5  直接缩放居中放竖屏，背景用毛玻璃模糊图（基础版）
  6  AIGC 模式：横屏视频补全到 9:16 竖屏（高级版计费）
  【竖 → 横】
  7  AIGC 模式：竖屏视频补全到 16:9 横屏（高级版计费）

COS 存储约定：
  通过环境变量 TENCENTCLOUD_COS_BUCKET 指定 COS Bucket 名称。
  - 输入文件默认路径：{TENCENTCLOUD_COS_BUCKET}/input/
  - 输出文件默认路径：{TENCENTCLOUD_COS_BUCKET}/output/orientation/
  输出文件名以 htv- 开头（官方约定，可用 --output-pattern 自定义）

用法：
  # 横转竖（默认算法 2，比例 9:16）
  python3 mps_orientation_convert.py --cos-input-key /input/landscape.mp4 --algorithm-type 2

  # 人脸场景横转竖（双人脸上下分屏）
  python3 mps_orientation_convert.py --url https://example.com/interview.mp4 --algorithm-type 3

  # 缩放 + 毛玻璃背景
  python3 mps_orientation_convert.py --cos-input-key /input/clip.mp4 --algorithm-type 5 --blur-weight 50

  # AIGC 横转竖（补全到 9:16）
  python3 mps_orientation_convert.py --url https://example.com/land.mp4 --algorithm-type 6

  # AIGC 竖转横（补全到 16:9）
  python3 mps_orientation_convert.py --url https://example.com/port.mp4 --algorithm-type 7 --ratio 16:9

  # 自定义比例与平滑速度
  python3 mps_orientation_convert.py --cos-input-key /input/game.mp4 --algorithm-type 2 \
      --ratio 3:4 --smooth-weight 0.5

  # Dry Run（仅打印请求参数，不实际调用 API）
  python3 mps_orientation_convert.py --cos-input-key /input/v.mp4 --algorithm-type 2 --dry-run

环境变量：
  TENCENTCLOUD_SECRET_ID   - 腾讯云 SecretId
  TENCENTCLOUD_SECRET_KEY  - 腾讯云 SecretKey
  TENCENTCLOUD_COS_BUCKET  - COS Bucket 名称（如 mybucket-125xxx）
  TENCENTCLOUD_COS_REGION  - COS Bucket 区域（必需）
"""

import argparse
import json
import os
import sys

# 轮询模块（同目录）
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)
from mps_auto_upgrade import check_sdk_version
try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
try:
    from mps_poll_task import poll_video_task, auto_upload_local_file, auto_download_outputs
    _POLL_AVAILABLE = True
except ImportError:
    _POLL_AVAILABLE = False

check_sdk_version()
try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.mps.v20190612 import mps_client, models
except ImportError:
    print("错误：请先安装腾讯云 SDK：python3 -m pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# 智能横竖屏方向转换常量（固定值，禁止修改或扩展）
# =============================================================================

# 智能分析模板 ID（固定使用 28 号预设模板）
AI_ANALYSIS_DEFINITION = 28

# SmoothWeight 默认值（官方文档示例值）
DEFAULT_SMOOTH_WEIGHT = 0.75

# 默认画面比例（官方：解析失败时回退 9:16）
DEFAULT_RATIO = "9:16"

# 算法类别表（取值严格来自官方文档，禁止扩展）
# 注：version 为官方计费项名称（官方统称"智能横转竖"），其中算法 7 实际做竖转横
ALGORITHM_TYPES = {
    2: {
        "desc": "多模型算法与定制优化",
        "version": "智能横转竖-基础版",
        "direction": "横转竖",
        "support_face_config": False,
        "support_blur": False,
    },
    3: {
        "desc": "精确人脸检测；两个人脸时上下分屏并尽量居中",
        "version": "智能横转竖-基础版",
        "direction": "横转竖",
        "support_face_config": True,
        "support_blur": False,
    },
    5: {
        "desc": "直接缩放居中放竖屏，毛玻璃模糊图作背景",
        "version": "智能横转竖-基础版",
        "direction": "横转竖",
        "support_face_config": False,
        "support_blur": True,
    },
    6: {
        "desc": "AIGC 模式：横屏补全到 9:16 竖屏",
        "version": "智能横转竖-高级版",
        "direction": "横转竖",
        "support_face_config": False,
        "support_blur": False,
    },
    7: {
        "desc": "AIGC 模式：竖屏补全到 16:9 横屏",
        "version": "智能横转竖-高级版",
        "direction": "竖转横",
        "support_face_config": False,
        "support_blur": False,
    },
}

# 人脸检测精度可选值（官方文档）
FACE_ACCURACY_CHOICES = ["Balance", "Efficiency", "Precision"]

# 无人脸兜底策略可选值（官方文档）
NO_FACE_CHOICES = ["Scale", "ScaleWithoutBlur"]

# 双人脸兜底策略可选值（官方文档）
DOUBLE_FACE_CHOICES = ["Scale", "ScaleWithoutBlur", "SplitScreenVertical"]


def get_cos_bucket():
    """从环境变量获取 COS Bucket 名称。"""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """从环境变量获取 COS Bucket 区域。"""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def get_credentials():
    """从环境变量获取腾讯云凭证。若缺失则尝试从 dotenv 文件自动加载后重试。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        # 凭证可能写在 ~/.env 等 dotenv 文件中而未导出，先尝试加载再重试
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] 环境变量未设置，尝试从系统文件自动加载...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from mps_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print(
                    "\n错误：TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY 未设置。\n"
                    "请在 ~/.env、~/.bashrc、~/.profile 或 <SKILL_DIR>/.env 中添加这些变量。\n",
                    file=sys.stderr,
                )
            sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def create_mps_client(cred, region):
    """创建 MPS 客户端。"""
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    http_profile.reqMethod = "POST"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return mps_client.MpsClient(cred, region, client_profile)


def build_input_info(args):
    """
    构建输入信息。

    支持两种输入方式（官方：暂不支持 AWS S3）：
    1. URL 输入：--url
    2. COS 路径输入：--cos-input-key（配合 --cos-input-bucket/--cos-input-region 或环境变量）
    """
    if args.url:
        return {
            "Type": "URL",
            "UrlInputInfo": {
                "Url": args.url
            }
        }

    cos_input_bucket = getattr(args, 'cos_input_bucket', None)
    cos_input_region = getattr(args, 'cos_input_region', None)
    cos_input_key = getattr(args, 'cos_input_key', None)

    if cos_input_key:
        bucket = cos_input_bucket or get_cos_bucket()
        region = cos_input_region or get_cos_region()
        if not bucket:
            print("错误：COS 输入需要指定 Bucket。请通过 --cos-input-bucket 参数或 TENCENTCLOUD_COS_BUCKET 环境变量设置",
                  file=sys.stderr)
            sys.exit(1)
        return {
            "Type": "COS",
            "CosInputInfo": {
                "Bucket": bucket,
                "Region": region,
                "Object": cos_input_key if cos_input_key.startswith("/") else f"/{cos_input_key}"
            }
        }

    print("错误：请指定输入源：\n"
          "  - URL: --url <URL>\n"
          "  - COS路径: --cos-input-key <key>（配合环境变量或 --cos-input-bucket/--cos-input-region）",
          file=sys.stderr)
    sys.exit(1)


def build_output_storage(args):
    """
    构建输出存储信息。

    优先级：
    1. 命令行参数 --output-bucket / --output-region
    2. 环境变量 TENCENTCLOUD_COS_BUCKET / TENCENTCLOUD_COS_REGION

    注意：官方要求 InputInfo.Type 为 URL 时 OutputStorage 必填。
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


def build_face_detect_config(args):
    """
    构建 FaceDetectConfig（仅算法 3 使用）。

    仅在用户显式传入相关参数时才构建，避免下发空对象。
    """
    cfg = {}

    if args.face_score_thd is not None:
        cfg["FaceScoreThd"] = args.face_score_thd
    if args.face_accuracy:
        cfg["FaceAccuracy"] = args.face_accuracy

    fallback = {}
    if args.no_face_detect:
        fallback["NoFaceDetect"] = args.no_face_detect
    if args.double_face:
        fallback["DoubleFace"] = args.double_face
    if fallback:
        cfg["FallbackConfig"] = fallback

    return cfg or None


def build_extended_parameter(args):
    """
    构建 ExtendedParameter 参数（htv 键下）。

    ⚠️ 字段严格来自官方文档，禁止自行增删。
    """
    htv = {
        "AlgorithmType": args.algorithm_type,
        "SmoothWeight": args.smooth_weight,
        "Ratio": args.ratio,
    }

    if args.output_pattern:
        htv["OutputPattern"] = args.output_pattern

    if args.blur_weight is not None:
        htv["BlurWeight"] = args.blur_weight

    face_cfg = build_face_detect_config(args)
    if face_cfg:
        htv["FaceDetectConfig"] = face_cfg

    return {"htv": htv}


def build_ai_analysis_task(args):
    """
    构建智能分析任务参数（横竖屏方向转换）。

    固定使用 28 号预设模板，通过 ExtendedParameter 指定算法与配置。
    ExtendedParameter 必须为序列化后的 JSON 字符串。
    """
    extended_param = build_extended_parameter(args)
    return {
        "Definition": AI_ANALYSIS_DEFINITION,
        "ExtendedParameter": json.dumps(extended_param, ensure_ascii=False)
    }


def build_request_params(args):
    """构建完整的 ProcessMedia 请求参数。"""
    params = {}

    params["InputInfo"] = build_input_info(args)

    output_storage = build_output_storage(args)
    if output_storage:
        params["OutputStorage"] = output_storage

    # 输出目录：默认 /output/orientation/
    params["OutputDir"] = args.output_dir if args.output_dir else "/output/orientation/"

    params["AiAnalysisTask"] = build_ai_analysis_task(args)

    if args.session_id:
        params["SessionId"] = args.session_id

    if args.notify_url:
        params["TaskNotifyConfig"] = {
            "NotifyType": "URL",
            "NotifyUrl": args.notify_url,
        }

    return params


def get_config_summary(args):
    """生成算法配置摘要文本。"""
    items = []
    preset = ALGORITHM_TYPES.get(args.algorithm_type, {})

    items.append(f"🔄 方向: {preset.get('direction', '')}")
    items.append(f"🧮 算法类别: {args.algorithm_type}（{preset.get('desc', '')}）")
    items.append(f"📊 计费版本: {preset.get('version', '')}")
    items.append(f"📐 画面比例: {args.ratio}")
    items.append(f"🎚️ 平滑速度 SmoothWeight: {args.smooth_weight}（越小镜头移动越快）")

    if args.blur_weight is not None:
        items.append(f"🌫️ 模糊参数 BlurWeight: {args.blur_weight}（数值越大越模糊，过大影响速度）")
    if args.output_pattern:
        items.append(f"📝 输出文件名模式: {args.output_pattern}")

    face_cfg = build_face_detect_config(args)
    if face_cfg:
        items.append(f"👤 人脸检测配置: {json.dumps(face_cfg, ensure_ascii=False)}")

    return items


def process_media(args):
    """发起智能横竖屏方向转换任务。"""
    region = args.region or os.environ.get("TENCENTCLOUD_API_REGION", "")

    # 构建请求（dry-run 时无需凭证）
    params = build_request_params(args)

    if args.dry_run:
        print("=" * 60)
        print("【Dry Run 模式】仅打印请求参数，不实际调用 API")
        print("=" * 60)
        print(json.dumps(params, ensure_ascii=False, indent=2))
        return

    cred = get_credentials()
    client = create_mps_client(cred, region)

    if args.verbose:
        print("请求参数：")
        print(json.dumps(params, ensure_ascii=False, indent=2))
        print()

    try:
        req = models.ProcessMediaRequest()
        req.from_json_string(json.dumps(params))

        resp = client.ProcessMedia(req)
        result = json.loads(resp.to_json_string())

        task_id = result.get('TaskId', 'N/A')
        print("✅ 横竖屏方向转换任务提交成功！")
        print(f"   TaskId: {task_id}")
        print(f"\n## TaskId: {task_id}")
        print(f"   RequestId: {result.get('RequestId', 'N/A')}")

        config_items = get_config_summary(args)
        if config_items:
            print("   配置详情:")
            for item in config_items:
                print(f"     {item}")

        print()
        print("⚠️  注意：横竖屏方向转换任务处理时间较长，请耐心等待。")
        print("     输出目录下 htv- 开头的文件即为处理结果。")

        if args.verbose:
            print("\n完整响应：")
            print(json.dumps(result, ensure_ascii=False, indent=2))

        no_wait = getattr(args, 'no_wait', False)
        if not no_wait and _POLL_AVAILABLE and task_id != 'N/A':
            poll_interval = getattr(args, 'poll_interval', 10)
            max_wait = getattr(args, 'max_wait', 1800)
            task_result = poll_video_task(task_id, region=region, interval=poll_interval,
                                          max_wait=max_wait, verbose=args.verbose)
            download_dir = getattr(args, 'download_dir', None)
            if download_dir and task_result and _POLL_AVAILABLE:
                auto_download_outputs(task_result, download_dir=download_dir)
        else:
            print("\n提示：任务在后台处理中，可使用以下命令查询进度：")
            print(f"  python3 scripts/mps_get_video_task.py --task-id {task_id}")

        return result

    except TencentCloudSDKException as e:
        print(f"❌ 请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def _ratio_type(value):
    """校验画面比例格式（形如 9:16）。"""
    parts = value.split(":")
    if len(parts) != 2 or not all(p.strip().isdigit() and int(p) > 0 for p in parts):
        raise argparse.ArgumentTypeError(
            f"比例格式非法: {value!r}，应形如 9:16 / 16:9 / 3:4（正整数:正整数）"
        )
    return value


def _smooth_weight_type(value):
    """校验 SmoothWeight 取值范围（官方：0-1 之间的浮点数）。"""
    try:
        v = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"SmoothWeight 必须是浮点数，当前: {value!r}")
    if not 0.0 <= v <= 1.0:
        raise argparse.ArgumentTypeError(
            f"SmoothWeight 必须在 0-1 之间（官方约定），当前: {v}"
        )
    return v


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    parser = argparse.ArgumentParser(
        description="腾讯云 MPS 智能横竖屏方向转换 —— 横屏→竖屏 / 竖屏→横屏（ROI 裁剪 / AIGC 补全）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 横转竖（默认算法 2，比例 9:16）
  python3 mps_orientation_convert.py --cos-input-key /input/landscape.mp4 --algorithm-type 2

  # 人脸场景横转竖（双人脸上下分屏）
  python3 mps_orientation_convert.py --url https://example.com/interview.mp4 --algorithm-type 3

  # 人脸检测精细配置
  python3 mps_orientation_convert.py --cos-input-key /input/talk.mp4 --algorithm-type 3 \\
      --face-score-thd 60 --face-accuracy Precision --double-face SplitScreenVertical

  # 缩放 + 毛玻璃背景
  python3 mps_orientation_convert.py --cos-input-key /input/clip.mp4 --algorithm-type 5 --blur-weight 50

  # AIGC 横转竖（补全到 9:16，高级版计费）
  python3 mps_orientation_convert.py --url https://example.com/land.mp4 --algorithm-type 6

  # AIGC 竖转横（补全到 16:9，高级版计费）
  python3 mps_orientation_convert.py --url https://example.com/port.mp4 --algorithm-type 7

  # 自定义比例与平滑速度
  python3 mps_orientation_convert.py --cos-input-key /input/game.mp4 --algorithm-type 2 \\
      --ratio 3:4 --smooth-weight 0.5

  # 自定义输出文件名
  python3 mps_orientation_convert.py --cos-input-key /input/v.mp4 --algorithm-type 2 \\
      --output-pattern "htv-{sessionId}-{timestamp}"

  # Dry Run（仅打印请求参数）
  python3 mps_orientation_convert.py --cos-input-key /input/v.mp4 --algorithm-type 2 --dry-run

算法类别（--algorithm-type，必填）：
  【横 → 竖】
  2  多模型算法与定制优化（基础版，横转竖推荐默认）
  3  精确人脸检测，双人脸上下分屏居中（基础版）
  5  直接缩放居中放竖屏，毛玻璃模糊背景（基础版）
  6  AIGC 模式，横屏补全到 9:16 竖屏（高级版计费）
  【竖 → 横】
  7  AIGC 模式，竖屏补全到 16:9 横屏（高级版计费）

⚠️ 重要提示：
  - 本脚本支持**双向转换**：算法 2/3/5/6 做横转竖，算法 7 做竖转横
  - 使用算法 7 时建议同时指定 --ratio 16:9（否则默认 9:16 与竖转横意图不符）
  - 本脚本仅支持处理离线文件，不支持直播流
  - 输入仅支持 URL 与腾讯云 COS，**不支持 AWS S3**
  - 输入封装格式：.mp4/.avi/.mkv/.mov/.mpg；编码：MPEG/H.264/H.265
  - 输出统一为 H.264 编码 .mp4 格式，文件名以 htv- 开头（官方约定）
  - --face-score-thd/--face-accuracy/--no-face-detect/--double-face 仅算法 3 生效
  - --blur-weight 仅算法 5 生效
  - 算法 6/7 为 AIGC 高级版，计费高于基础版

环境变量：
  TENCENTCLOUD_SECRET_ID   腾讯云 SecretId
  TENCENTCLOUD_SECRET_KEY  腾讯云 SecretKey
  TENCENTCLOUD_COS_BUCKET  COS Bucket 名称
  TENCENTCLOUD_COS_REGION  COS Bucket 区域（必需）
        """
    )

    # ---- 输入源 ----
    input_group = parser.add_argument_group("输入源（三选一，不支持 AWS S3）")
    input_group.add_argument("--local-file", type=str,
                             help="本地文件路径，自动上传到 COS 后处理（需配置 TENCENTCLOUD_COS_BUCKET）")
    input_group.add_argument("--url", type=str, help="视频 URL 地址")
    input_group.add_argument("--cos-input-bucket", type=str, help="输入 COS Bucket 名称")
    input_group.add_argument("--cos-input-region", type=str,
                             help="输入 COS Bucket 区域（如 ap-guangzhou）")
    input_group.add_argument("--cos-input-key", type=str,
                             help="输入 COS 对象 Key（如 /input/video.mp4）")

    # ---- 算法配置（必填）----
    algo_group = parser.add_argument_group("算法配置（必填）")
    algo_group.add_argument(
        "--algorithm-type", type=int, required=True,
        choices=sorted(ALGORITHM_TYPES.keys()),
        metavar="TYPE",
        help=(
            "算法类别。横→竖：2=多模型定制优化 | 3=精确人脸检测 | "
            "5=缩放+毛玻璃背景 | 6=AIGC补全；"
            "竖→横：7=AIGC补全（建议同时指定 --ratio 16:9）"
        )
    )
    algo_group.add_argument("--ratio", type=_ratio_type, default=DEFAULT_RATIO,
                            help=(f"目标画面横竖比，形如 9:16 / 16:9 / 3:4（默认 {DEFAULT_RATIO}）。"
                                  "竖转横（算法 7）时应显式指定 16:9"))
    algo_group.add_argument("--smooth-weight", type=_smooth_weight_type,
                            default=DEFAULT_SMOOTH_WEIGHT,
                            help=f"平滑速度，0-1 浮点数，越小镜头移动越快（默认 {DEFAULT_SMOOTH_WEIGHT}）")
    algo_group.add_argument("--blur-weight", type=int, default=None,
                            help="模糊参数，数值越大越模糊（仅算法 5 生效；过大影响处理速度）")
    algo_group.add_argument("--output-pattern", type=str, default=None,
                            help='输出文件名模式，可用 {sessionId}/{timestamp}（默认 "htv-{sessionId}"）')

    # ---- 人脸检测配置（仅算法 3 生效）----
    face_group = parser.add_argument_group("人脸检测配置（仅 --algorithm-type 3 生效）")
    face_group.add_argument("--face-score-thd", type=int, default=None,
                            help="人脸识别阈值，仅评分超过该阈值才视为有效人脸")
    face_group.add_argument("--face-accuracy", type=str, default=None,
                            choices=FACE_ACCURACY_CHOICES,
                            help="人脸检测执行次数（默认 Balance）")
    face_group.add_argument("--no-face-detect", type=str, default=None,
                            choices=NO_FACE_CHOICES,
                            help="无人脸兜底策略（默认 ScaleWithoutBlur）")
    face_group.add_argument("--double-face", type=str, default=None,
                            choices=DOUBLE_FACE_CHOICES,
                            help="双人脸兜底策略（默认 SplitScreenVertical）")

    # ---- 输出 ----
    output_group = parser.add_argument_group("输出配置（可选）")
    output_group.add_argument("--output-bucket", type=str, help="输出 COS Bucket 名称")
    output_group.add_argument("--output-region", type=str, help="输出 COS Bucket 区域")
    output_group.add_argument("--output-dir", type=str,
                              help="输出目录（默认 /output/orientation/）")

    # ---- 其他 ----
    other_group = parser.add_argument_group("其他配置")
    other_group.add_argument("--region", type=str, help="MPS 服务区域（默认 ap-guangzhou）")
    other_group.add_argument("--session-id", type=str, default=None,
                             help="去重识别码，最长 50 字符；三天内相同识别码的请求会报错")
    other_group.add_argument("--notify-url", type=str, help="任务完成回调 URL")
    other_group.add_argument("--no-wait", action="store_true", help="仅提交任务，不等待结果")
    other_group.add_argument("--poll-interval", type=int, default=10,
                             help="轮询间隔（秒），默认 10")
    other_group.add_argument("--max-wait", type=int, default=1800,
                             help="最长等待时间（秒），默认 1800（30分钟）")
    other_group.add_argument("--verbose", "-v", action="store_true", help="输出详细信息")
    other_group.add_argument("--dry-run", action="store_true", help="仅打印参数，不调用 API")
    other_group.add_argument("--download-dir", type=str, default=None,
                             help="任务完成后自动下载结果到指定目录（默认：不下载）")

    args = parser.parse_args()

    # --url 传入本地路径时自动转为本地上传模式
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

    # ---- 校验 ----
    has_url = bool(args.url)
    has_cos_path = bool(getattr(args, 'cos_input_key', None))
    if not has_url and not has_cos_path:
        parser.error("请指定输入源：--url 或 --cos-input-key（配合 --cos-input-bucket/--cos-input-region 或环境变量）")

    preset = ALGORITHM_TYPES.get(args.algorithm_type, {})

    # 人脸检测参数仅算法 3 生效
    face_args = {
        "--face-score-thd": args.face_score_thd,
        "--face-accuracy": args.face_accuracy,
        "--no-face-detect": args.no_face_detect,
        "--double-face": args.double_face,
    }
    used_face_args = [k for k, v in face_args.items() if v is not None]
    if used_face_args and not preset.get("support_face_config"):
        parser.error(
            f"{', '.join(used_face_args)} 仅在 --algorithm-type 3（精确人脸检测）时生效，"
            f"当前算法类别为 {args.algorithm_type}"
        )

    # 模糊参数仅算法 5 生效
    if args.blur_weight is not None and not preset.get("support_blur"):
        parser.error(
            f"--blur-weight 仅在 --algorithm-type 5（缩放+毛玻璃背景）时生效，"
            f"当前算法类别为 {args.algorithm_type}"
        )

    # SessionId 长度限制（官方：最长 50 字符）
    if args.session_id and len(args.session_id) > 50:
        parser.error(f"--session-id 最长 50 个字符，当前 {len(args.session_id)} 个")

    # 竖转横（算法 7）若沿用默认竖屏比例，与转换意图矛盾，给出显式提示
    if args.algorithm_type == 7 and args.ratio == DEFAULT_RATIO:
        print(f"⚠️  提示：算法 7 为「竖转横」，但 --ratio 仍是默认竖屏比例 {DEFAULT_RATIO}。",
              file=sys.stderr)
        print("     若目标是横屏输出，请显式指定 --ratio 16:9。", file=sys.stderr)

    cos_bucket_env = get_cos_bucket()
    cos_region_env = get_cos_region()

    # ---- 打印执行信息 ----
    print("=" * 60)
    print(f"腾讯云 MPS 横竖屏方向转换 — {preset.get('direction', '')}（算法 {args.algorithm_type}）")
    print("=" * 60)
    if args.url:
        print(f"输入: URL - {args.url}")
    else:
        bucket_display = getattr(args, 'cos_input_bucket', None) or cos_bucket_env or "未设置"
        region_display = getattr(args, 'cos_input_region', None) or cos_region_env
        print(f"输入: COS - {bucket_display}:{args.cos_input_key} (region: {region_display})")

    out_bucket = args.output_bucket or cos_bucket_env or "未设置"
    out_region = args.output_region or cos_region_env
    out_dir = args.output_dir or "/output/orientation/"
    print(f"输出: COS - {out_bucket}:{out_dir} (region: {out_region})")

    if cos_bucket_env:
        print(f"COS Bucket (环境变量): {cos_bucket_env}")

    # URL 输入时 OutputStorage 必填（官方约定）
    if not args.dry_run and not args.output_bucket and not cos_bucket_env:
        print("❌ 未指定输出 Bucket，请通过 --output-bucket 参数或 TENCENTCLOUD_COS_BUCKET 环境变量配置后重试",
              file=sys.stderr)
        sys.exit(1)

    config_items = get_config_summary(args)
    if config_items:
        print("配置详情:")
        for item in config_items:
            print(f"  {item}")

    print()
    print("⚠️  提示：横竖屏方向转换任务处理时间较长，请耐心等待。")
    print("-" * 60)

    process_media(args)


if __name__ == "__main__":
    main()
