#!/usr/bin/env python3
"""
tencent-mps-video-dubbing :: 一站式视频译制 (video dubbing)

基于腾讯云 MPS ProcessMedia 接口的 AiAnalysisTask (Definition=25)
+ ExtendedParameter 扩展参数，一次性完成：
    去字幕/ASR → 翻译 → 压制新字幕 → AI 高情感克隆配音

两种使用模式：
    1) CLI 模式：命令行参数直接传，**核心业务参数必须显式提供**（不允许静默使用默认值）
    2) 交互向导：不传任何输入源参数即进入，对每个配置项逐项询问（无预填默认，必须手动输入）

核心业务参数（无默认值，必须显式指定，缺失即 exit=2）：
    • --mode          （ocr / asr）
    • --src-lang      （源语言 code）
    • --dst-lang      （目标语言 code）
    • --burn-subtitle / --no-burn-subtitle  （二选一）
    • --subtitle-area preset|custom         （仅 OCR 模式必填；ASR 模式忽略）
    • --subtitle-bbox LTX,LTY,RBX,RBY       （仅 --subtitle-area=custom 必填，4 点像素坐标）

运维参数、ExtendedParameter 约束、费用确认规则与完整文档链接
详见 `python mps_video_dubbing.py --help`
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

# ---------------------------------------------------------------------------
# 复用 tencent-mps 工具模块（同目录导入）
# ---------------------------------------------------------------------------
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False

try:
    from mps_poll_task import (
        poll_video_task,
        auto_upload_local_file,
        auto_download_outputs,
    )
    _POLL_AVAILABLE = True
except ImportError:
    _POLL_AVAILABLE = False

try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
        TencentCloudSDKException,
    )
    from tencentcloud.mps.v20190612 import mps_client, models
except ImportError:
    print("错误：请先安装腾讯云 SDK：pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# 常量与默认值
# ─────────────────────────────────────────────────────────────────────────────
# 核心业务参数无默认值，必须由用户显式提供（mode / src-lang / dst-lang /
# burn-subtitle / subtitle-area），缺失即 exit=2，防止漏传导致译制结果不符合预期。
# 运维类常量（CLUSTER_ID / DEFINITION / OUTPUT_DIR / POLL_INTERVAL / MAX_WAIT）
# 仍作为默认值生效，与译制结果质量无关。
# =============================================================================
SUPPORTED_LANGUAGES = {
    "zh": "中文", "en": "英语", "ja": "日语", "ko": "韩语",
    "de": "德语", "fr": "法语", "ru": "俄语", "uk": "乌克兰语",
    "pt": "葡萄牙语", "it": "意大利语", "es": "西班牙语", "id": "印度尼西亚语",
    "nl": "荷兰语", "tr": "土耳其语", "fil": "菲律宾语", "ms": "马来语",
    "el": "希腊语", "fi": "芬兰语", "hr": "克罗地亚语", "sk": "斯洛伐克语",
    "pl": "波兰语", "sv": "瑞典语", "hi": "印地语", "bg": "保加利亚语",
    "ro": "罗马尼亚语", "ar": "阿拉伯语", "cs": "捷克语", "da": "丹麦语",
    "ta": "泰米尔语", "hun": "匈牙利语", "vi": "越南语",
}

# —— 按地区分组（仅用于交互展示，便于用户按场景快速定位）——
LANGUAGES_BY_REGION = [
    ("全球通用", ["en"]),
    ("东亚",   ["zh", "ja", "ko"]),
    ("东南亚", ["id", "ms", "fil", "vi", "ta"]),
    ("南亚",   ["hi"]),
    ("中东",   ["ar", "tr"]),
    ("西欧",   ["de", "fr", "it", "es", "pt", "nl"]),
    ("北欧",   ["sv", "da", "fi"]),
    ("中东欧", ["ru", "uk", "pl", "cs", "sk", "hun", "bg", "ro", "hr"]),
    ("南欧",   ["el"]),
]

# —— 运维常量（仍作为真正的默认值生效）——
# cluster_id=gpu_zhiyan：配音级译制（AiAnalysisTask Definition=25 / DeLogoTask）
# 统一使用 gpu_zhiyan 集群。
DEFAULT_CLUSTER_ID     = "gpu_zhiyan"
DEFAULT_DEFINITION     = 25
DEFAULT_OUTPUT_DIR     = "/output/video-dubbing/"
# 区域不设默认值；必须由 $TENCENTCLOUD_API_REGION / $TENCENTCLOUD_COS_REGION 提供，缺值即报错。
DEFAULT_POLL_INTERVAL  = 15
DEFAULT_MAX_WAIT       = 3600  # 译制任务较长，默认 1 小时

MODE_DESC = {
    "ocr": "OCR提取字幕 → 擦除原字幕 → 翻译 → 压制新字幕 → AI克隆配音 (适用硬字幕视频)",
    "asr": "ASR语音识别 → 翻译 → 压制新字幕 → AI克隆配音 (适用无硬字幕视频)",
}


# =============================================================================
# 客户端与环境
# =============================================================================
def create_client(region: str) -> "mps_client.MpsClient":
    """创建 MPS 客户端，密钥优先从环境变量读取。"""
    secret_id  = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        print("❌ 未找到 TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY 环境变量", file=sys.stderr)
        print("   请设置后重试：export TENCENTCLOUD_SECRET_ID=...", file=sys.stderr)
        sys.exit(1)

    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile()
    http_profile.endpoint = "mps.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(cred, region, client_profile)


# =============================================================================
# 核心：构建请求 + 提交
# =============================================================================
def build_extended_parameter(mode: str, src_lang: str, dst_lang: str,
                             burn_subtitle: bool,
                             subtitle_area: str = "preset",
                             bbox: Optional[tuple] = None) -> str:
    """
    构建 AiAnalysisTask.ExtendedParameter (转义 JSON 字符串)。

    字幕区域策略（仅 OCR 模式生效；ASR 模式 subtitle_area 被忽略）：
      • subtitle_area="preset"（或 mode="asr"）→ 产物不写 als_filter 键，后端使用默认区域（画面中部靠下）
      • subtitle_area="custom" → 写 als_filter.active_areas[{type:2, lt_x, lt_y, rb_x, rb_y}]
                                  注意：不写 preview_size（配音级译制不需要预览窗口大小）

    subtitle_param 恒含字段（经线上回归确认，缺一会被后端拒绝）：
      • use_draw: True/False（是否压制翻译字幕；语义面：压字幕为真、不压为假，恒写而非仅 False 时才写）
      • font_type: "auto"（字体自动选择，后端要求恒传）
    """
    delogo = {
        "cluster_id": DEFAULT_CLUSTER_ID,
        "CustomerAppId": f"audio_clone_{mode}",
        "subtitle_param": {
            "translate_src_language": src_lang,
            "translate_dst_language": dst_lang,
            "use_draw": bool(burn_subtitle),
            "font_type": "auto",
        },
    }

    # 仅 OCR + custom 才追加 als_filter；preset 或 ASR 都不写
    if mode == "ocr" and subtitle_area == "custom" and bbox is not None:
        lt_x, lt_y, rb_x, rb_y = bbox
        delogo["als_filter"] = {
            "active_areas": [{
                "type": 2,
                "lt_x": int(lt_x), "lt_y": int(lt_y),
                "rb_x": int(rb_x), "rb_y": int(rb_y),
            }]
        }
    return json.dumps({"delogo": delogo}, ensure_ascii=False)


def build_input_info(input_url: Optional[str],
                     cos_input_bucket: Optional[str],
                     cos_input_region: Optional[str],
                     cos_input_key: Optional[str]) -> dict:
    """
    构建 InputInfo。

    输入源优先级与规则：
      1. input_url 以 "cos://" 开头 → 自动解析为 CosInputInfo（Bucket/Region/Object）
         — 例：cos://<your-bucket>-<appid>/input/<filename>.mp4
      2. input_url 非空且非 cos:// → UrlInputInfo（公网 URL 拉取，含 http(s):// 与其他形式）
      3. input_url 为空 + 显式传了 cos_input_bucket/key → CosInputInfo
    """
    if input_url:
        if input_url.startswith("cos://"):
            # cos://<bucket>/<key...>
            rest = input_url[len("cos://"):]
            slash = rest.find("/")
            if slash <= 0:
                raise ValueError(f"非法的 cos:// URL：{input_url}（应为 cos://<bucket>/<key>）")
            bucket = rest[:slash]
            obj_key = rest[slash:]  # 含前导 /
            # region 必填：必须从入参或环境变量取到，缺值即报错
            region = (
                cos_input_region
                or os.environ.get("TENCENTCLOUD_COS_REGION")
            )
            if not region:
                raise ValueError(
                    "cos:// 输入需要 region：请显式传 --cos-input-region 或设置 "
                    "环境变量 TENCENTCLOUD_COS_REGION"
                )
            return {
                "Type": "COS",
                "CosInputInfo": {
                    "Bucket": bucket,
                    "Region": region,
                    "Object": obj_key,
                },
            }
        # 真正的 http(s) URL
        return {"Type": "URL", "UrlInputInfo": {"Url": input_url}}
    return {
        "Type": "COS",
        "CosInputInfo": {
            "Bucket": cos_input_bucket,
            "Region": cos_input_region,
            "Object": cos_input_key if cos_input_key.startswith("/") else "/" + cos_input_key,
        },
    }


def submit_video_dubbing(
    *,
    input_url: Optional[str],
    cos_input_bucket: Optional[str],
    cos_input_region: Optional[str],
    cos_input_key: Optional[str],
    mode: str,
    src_lang: str,
    dst_lang: str,
    burn_subtitle: bool,
    cos_bucket: str,
    cos_region: str,
    output_dir: str,
    session_id: Optional[str],
    region: str,
    subtitle_area: str = "preset",
    bbox: Optional[tuple] = None,
    dry_run: bool = False,
) -> dict:
    """构建并提交 ProcessMedia 请求，返回响应 dict。dry_run=True 仅打印不提交。"""
    input_info = build_input_info(input_url, cos_input_bucket, cos_input_region, cos_input_key)
    extended_parameter = build_extended_parameter(
        mode, src_lang, dst_lang, burn_subtitle,
        subtitle_area=subtitle_area, bbox=bbox,
    )

    params = {
        "InputInfo": input_info,
        "OutputStorage": {
            "Type": "COS",
            "CosOutputStorage": {"Bucket": cos_bucket, "Region": cos_region},
        },
        "OutputDir": output_dir,
        "AiAnalysisTask": {
            "Definition": DEFAULT_DEFINITION,
            "ExtendedParameter": extended_parameter,
        },
    }
    if session_id:
        params["SessionId"] = session_id

    print_config_summary(
        input_info=input_info, mode=mode, src_lang=src_lang, dst_lang=dst_lang,
        burn_subtitle=burn_subtitle, cos_bucket=cos_bucket, cos_region=cos_region,
        output_dir=output_dir, extended_parameter=extended_parameter, region=region,
        subtitle_area=subtitle_area, bbox=bbox,
    )

    if dry_run:
        print("\n🔍 [DRY-RUN] 已构建请求参数，不会提交。完整 ProcessMedia 请求：")
        print(json.dumps(params, ensure_ascii=False, indent=2))
        return {"DryRun": True, "Params": params}

    client = create_client(region)
    req = models.ProcessMediaRequest()
    req.from_json_string(json.dumps(params))

    print("\n📤 正在提交一站式视频译制任务...")
    resp = client.ProcessMedia(req)
    return json.loads(resp.to_json_string())


def print_config_summary(**kw) -> None:
    print()
    print("=" * 62)
    print("  🎬 一站式视频译制 — 本次任务配置")
    print("=" * 62)
    inp = kw["input_info"]
    if inp["Type"] == "URL":
        print(f"  📥 输入源  : URL → {inp['UrlInputInfo']['Url']}")
    else:
        c = inp["CosInputInfo"]
        print(f"  📥 输入源  : COS → cos://{c['Bucket']}{c['Object']} ({c['Region']})")
    print(f"  🔄 译制模式: {kw['mode']} ({MODE_DESC[kw['mode']]})")
    print(f"  🌏 源语言  : {SUPPORTED_LANGUAGES.get(kw['src_lang'], kw['src_lang'])} ({kw['src_lang']})")
    print(f"  🌐 目标语言: {SUPPORTED_LANGUAGES.get(kw['dst_lang'], kw['dst_lang'])} ({kw['dst_lang']})")
    print(f"  🔥 压制字幕: {'是' if kw['burn_subtitle'] else '否'}")
    # 仅 OCR 模式展示字幕区域；ASR 模式不展示
    if kw['mode'] == 'ocr':
        area = kw.get('subtitle_area', 'preset')
        if area == 'custom' and kw.get('bbox'):
            lt_x, lt_y, rb_x, rb_y = kw['bbox']
            w, h = rb_x - lt_x, rb_y - lt_y
            print(f"  🎯 字幕区域: 自定义 ({lt_x},{lt_y}) → ({rb_x},{rb_y})  = {w}×{h}px")
        else:
            print(f"  🎯 字幕区域: 预设（画面中部靠下，由后端默认处理）")
    _disp_dir = kw['output_dir'] if kw['output_dir'].startswith('/') else '/' + kw['output_dir']
    print(f"  📦 输出桶  : cos://{kw['cos_bucket']}{_disp_dir} ({kw['cos_region']})")
    print(f"  🌍 API 区域: {kw['region']}")
    print(f"  🧩 扩展参数: {kw['extended_parameter']}")
    print("=" * 62)


# =============================================================================
# 任务查询
# =============================================================================
def query_task(task_id: str, region: str) -> dict:
    """一次性查询任务详情 (不轮询)。"""
    client = create_client(region)
    req = models.DescribeTaskDetailRequest()
    req.from_json_string(json.dumps({"TaskId": task_id}))
    resp = client.DescribeTaskDetail(req)
    return json.loads(resp.to_json_string())


# =============================================================================
# 交互向导 —— 对每一项都提供默认值，回车即采用默认
# =============================================================================
def _prompt(label: str, default: Optional[str] = None,
            choices: Optional[list] = None) -> str:
    """通用输入，空则返回默认；choices 存在时严格校验。"""
    while True:
        hint = f" (默认 {default})" if default is not None else ""
        if choices:
            hint = f" [{'/'.join(choices)}]" + hint
        val = input(f"  {label}{hint}: ").strip()
        if not val:
            if default is None:
                print("    ⚠️  此项必填，请输入")
                continue
            return default
        if choices and val not in choices:
            print(f"    ⚠️  无效，请从 {choices} 中选择")
            continue
        return val


def _prompt_yn(label: str, default: Optional[bool] = None) -> bool:
    """
    y/n 交互。
    - default=None：必填，用户必须输入 y/n
    - default=True/False：有预填，回车即采用
    """
    if default is None:
        hint = "y/n"
    else:
        hint = "Y/n" if default else "y/N"
    while True:
        val = input(f"  {label} [{hint}]: ").strip().lower()
        if not val:
            if default is None:
                print("    ⚠️  此项必填，请输入 y 或 n")
                continue
            return default
        if val in ("y", "yes", "是", "1", "true"):
            return True
        if val in ("n", "no", "否", "0", "false"):
            return False
        print("    ⚠️  无效输入，请输入 y 或 n")


def _prompt_bbox() -> tuple:
    """
    交互式输入矩形 4 个整数像素坐标：lt_x, lt_y, rb_x, rb_y。
    要求 lt_x < rb_x 且 lt_y < rb_y，且全部为非负整数。
    """
    def _ask_int(label: str) -> int:
        while True:
            val = input(f"      {label}: ").strip()
            if not val:
                print("        ⚠️  此项必填")
                continue
            try:
                n = int(val)
                if n < 0:
                    print("        ⚠️  必须为非负整数")
                    continue
                return n
            except ValueError:
                print("        ⚠️  请输入整数")

    while True:
        lt_x = _ask_int("左上角 X (lt_x)")
        lt_y = _ask_int("左上角 Y (lt_y)")
        rb_x = _ask_int("右下角 X (rb_x)")
        rb_y = _ask_int("右下角 Y (rb_y)")
        if rb_x <= lt_x or rb_y <= lt_y:
            print(f"        ❌ 坐标非法：需满足 lt_x<rb_x 且 lt_y<rb_y，"
                  f"当前 ({lt_x},{lt_y})→({rb_x},{rb_y})，请重新输入")
            continue
        w, h = rb_x - lt_x, rb_y - lt_y
        print(f"      ✅ 字幕区域：({lt_x},{lt_y}) → ({rb_x},{rb_y})  尺寸 {w}×{h}px")
        return (lt_x, lt_y, rb_x, rb_y)


def _parse_bbox_str(s: str) -> tuple:
    """
    解析 CLI 参数 --subtitle-bbox "lt_x,lt_y,rb_x,rb_y" 为四元组。
    非法时抛 argparse.ArgumentTypeError。
    """
    parts = [p.strip() for p in s.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(
            f"--subtitle-bbox 需要 4 个逗号分隔的整数（lt_x,lt_y,rb_x,rb_y），收到：{s!r}"
        )
    try:
        lt_x, lt_y, rb_x, rb_y = [int(p) for p in parts]
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"--subtitle-bbox 必须全为整数，收到：{s!r}"
        )
    if min(lt_x, lt_y, rb_x, rb_y) < 0:
        raise argparse.ArgumentTypeError("--subtitle-bbox 坐标不能为负")
    if rb_x <= lt_x or rb_y <= lt_y:
        raise argparse.ArgumentTypeError(
            f"--subtitle-bbox 需满足 lt_x<rb_x 且 lt_y<rb_y，收到：({lt_x},{lt_y})→({rb_x},{rb_y})"
        )
    return (lt_x, lt_y, rb_x, rb_y)


def run_wizard(args: argparse.Namespace) -> dict:
    """交互式询问所有扩展配置，返回一个完整的配置字典。"""
    print()
    print("🧙 进入一站式视频译制向导")
    print("   核心业务项（输入源/模式/源语言/目标语言/压制字幕）必填，无默认值；")
    print("   OCR 模式会额外询问『字幕区域』（预设/自定义坐标）；")
    print("   COS 输出桶/地域/下载目录等运维项回车可用默认值。\n")

    # 1. 输入源
    print("步骤 1/9 📥 选择输入源（必选，无默认值）：")
    print("   [1] 本地文件（自动上传到 COS）")
    print("   [2] 公网 URL")
    print("   [3] COS 对象路径")
    src = _prompt("请选择", choices=["1", "2", "3"])

    local_file = input_url = cos_in_bucket = cos_in_region = cos_in_key = None
    if src == "1":
        local_file = _prompt("    本地文件绝对路径")
    elif src == "2":
        input_url = _prompt("    视频 URL")
    else:
        # COS 输入需要明确桶和地域（可从环境变量获取，或用户输入）
        default_bucket = os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
        default_region = os.environ.get("TENCENTCLOUD_COS_REGION", "")
        cos_in_bucket = _prompt("    COS 输入桶", default=default_bucket or None)
        cos_in_region = _prompt("    COS 输入地域", default=default_region or None)
        cos_in_key = _prompt("    COS 对象 key (如 input/video.mp4)")

    # 2. 模式
    print("\n步骤 2/9 🔄 选择译制模式（必选，无默认值）：")
    print(f"   ocr — {MODE_DESC['ocr']}")
    print(f"   asr — {MODE_DESC['asr']}")
    mode = _prompt("请选择", choices=["ocr", "asr"])

    # 3. 源语言
    print("\n步骤 3/9 🌏 源语言（必选，无默认值）：")
    print_language_hint(title="   👇 请从下列【简写 code】中选择一项作为源语言")
    src_lang = _prompt("源语言（如 zh）")
    if src_lang not in SUPPORTED_LANGUAGES:
        print(f"\n    ❌ 不支持的语种 '{src_lang}'，请从下列简写中选择：", file=sys.stderr)
        print_language_hint(title="   🌍 可用语言简写（请重新运行向导并输入其中之一）")
        sys.exit(1)

    # 4. 目标语言
    print(f"\n步骤 4/9 🌐 目标语言（必选，无默认值；不能等于源语言 '{src_lang}'）：")
    print(f"   💡 提示：输入下方任一【简写 code】，已选源语言为 [{src_lang}] {SUPPORTED_LANGUAGES[src_lang]}")
    # 目标语言仅展示紧凑表（避免重复刷屏），地区分组已在步骤 3 展示过
    print("  " + "─" * 68)
    print(_format_languages_compact())
    print("  " + "─" * 68)
    dst_lang = _prompt("目标语言（如 en）")
    if dst_lang not in SUPPORTED_LANGUAGES:
        print(f"\n    ❌ 不支持的语种 '{dst_lang}'，请从下列简写中选择：", file=sys.stderr)
        print_language_hint(title="   🌍 可用语言简写（请重新运行向导并输入其中之一）")
        sys.exit(1)
    if src_lang == dst_lang:
        print(f"\n    ❌ 源语言和目标语言不能相同（均为 '{src_lang}'），请重新运行向导", file=sys.stderr)
        sys.exit(1)

    # 5. 压制字幕
    print("\n步骤 5/9 🔥 是否将翻译后的字幕压制到视频画面（必选，无默认值）：")
    burn = _prompt_yn("压制字幕")

    # 5.5 / 6. OCR 模式专属：字幕区域
    subtitle_area = "preset"
    bbox = None
    if mode == "ocr":
        print("\n步骤 6/9 🎯 OCR 字幕区域（必选，无默认值）：")
        print("   硬字幕在画面上的位置将直接影响识别与擦除的准确性。")
        print("   [1] 预设：画面中部靠下（推荐，适合 90% 常规硬字幕视频；产物不写 als_filter）")
        print("   [2] 自定义：精确指定像素矩形坐标（适合顶部字幕 / 竖屏 / 双语对照等非常规场景）")
        area_choice = _prompt("请选择", choices=["1", "2"])
        if area_choice == "2":
            subtitle_area = "custom"
            print("   请依次输入矩形 4 个【整数像素坐标】（示例：lt_x=53, lt_y=741, rb_x=953, rb_y=922）：")
            bbox = _prompt_bbox()
        else:
            subtitle_area = "preset"
    else:
        print("\n步骤 6/9 🎯 字幕区域：ASR 模式无需指定，跳过")

    # 7. 输出桶
    print("\n步骤 7/9 📦 输出 COS 桶/地域（任务生成的译制成品存储位置）：")
    default_bucket = os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
    default_region = os.environ.get("TENCENTCLOUD_COS_REGION", "")
    cos_bucket = _prompt("    输出桶", default=default_bucket or None)
    cos_region = _prompt("    输出地域", default=default_region or None)
    output_dir = _prompt("    输出目录", default=DEFAULT_OUTPUT_DIR)

    # 8. 下载
    print("\n步骤 8/9 📥 任务完成后是否下载成品到本地：")
    download_dir = None
    if _prompt_yn("下载到本地", default=False):
        download_dir = _prompt("    下载目录", default="./output/")

    # 9. 费用确认
    print("\n步骤 9/9 💰 费用确认：")
    print("=" * 62)
    print("  一站式视频译制计费提示")
    print("=" * 62)
    print("  本次任务将调用腾讯云 MPS 一站式视频译制，按以下项计费：")
    if mode == "ocr":
        print("    • 去字幕")
        print("    • OCR 提取字幕 + 翻译 + 压制字幕")
        print("    • AI 配音（高情感克隆音色）")
    else:
        print("    • ASR 生成字幕 + 翻译 + 压制字幕")
        print("    • AI 配音（高情感克隆音色）")
    print("  计费详情见：https://cloud.tencent.com/document/product/862/124504")
    print("=" * 62)
    confirm = input("\n  请输入 YES（大写）确认提交任务，其他任意输入将中止: ").strip()
    if confirm != "YES":
        print("\n🛑 已取消，未提交任务")
        sys.exit(0)

    return {
        "local_file": local_file,
        "input_url": input_url,
        "cos_input_bucket": cos_in_bucket,
        "cos_input_region": cos_in_region,
        "cos_input_key": cos_in_key,
        "mode": mode,
        "src_lang": src_lang,
        "dst_lang": dst_lang,
        "burn_subtitle": burn,
        "subtitle_area": subtitle_area,
        "bbox": bbox,
        "cos_bucket": cos_bucket,
        "cos_region": cos_region,
        "output_dir": output_dir,
        "download_dir": download_dir,
        "confirm_charges": True,
    }


# =============================================================================
# 工具辅助
# =============================================================================
def _format_languages_compact() -> str:
    """紧凑对照表：每行 4 个 '[code] 名称'，便于在向导/错误提示中复用。"""
    items = [f"[{code:<3}] {name}" for code, name in SUPPORTED_LANGUAGES.items()]
    per_row = 4
    col_w   = 16  # 每列宽度（可容纳 [fil] 5 字 + 中文名 3~5 字 + 间隔）
    lines = []
    for i in range(0, len(items), per_row):
        row = items[i:i + per_row]
        lines.append("  " + "".join(f"{cell:<{col_w}}" for cell in row).rstrip())
    return "\n".join(lines)


def _format_languages_grouped() -> str:
    """按地区分组展示，强调'输入简写即可'。"""
    lines = []
    for region, codes in LANGUAGES_BY_REGION:
        parts = [f"{SUPPORTED_LANGUAGES[c]} {c}" for c in codes]
        lines.append(f"  {region:<5}│ " + "、".join(parts))
    return "\n".join(lines)


def print_language_hint(title: str = "🌍 支持的语言（请输入下方【简写 code】，如 zh / en / ja）") -> None:
    """
    打印"语言输入提示"——在任何需要用户填写 src-lang / dst-lang 的时机调用。
    输出包含：标题 → 紧凑对照表（所有 31 种语言的简写）→ 地区分组速查 → 使用提示。
    """
    print(f"\n{title}")
    print("  " + "─" * 68)
    print(_format_languages_compact())
    print("  " + "─" * 68)
    print("  📍 按地区速查：")
    print(_format_languages_grouped())
    print("  " + "─" * 68)
    print("  💡 规则：① 输入小写 code（示例：zh / en / fil / hun）  "
          "② 源语言 ≠ 目标语言")


def list_languages() -> None:
    """--list-languages 命令：对外完整展示所有支持的语种简写。"""
    print("\n🌍 腾讯云 MPS 视频译制支持的语言（共 "
          f"{len(SUPPORTED_LANGUAGES)} 种，全部双向支持翻译）")
    print("   --src-lang / --dst-lang 无默认值，必须显式指定\n"
          "   详见 references/mps_video_dubbing.md「支持语种」章节")
    print_language_hint(title="📋 完整简写对照表")
    # 标注"参考值"（即 references 文档示例里最常用的 zh→en）
    print(f"\n  📌 参考示例：--src-lang zh  --dst-lang en"
          f"   （{SUPPORTED_LANGUAGES['zh']} → {SUPPORTED_LANGUAGES['en']}）")


def has_any_input_arg(args: argparse.Namespace) -> bool:
    return bool(args.input_url or args.cos_input_key or args.local_file)


# =============================================================================
# CLI
# =============================================================================
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mps_video_dubbing.py",
        description="一站式视频译制 — 腾讯云 MPS ProcessMedia (Definition=25)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用模式
────────────────────────────────────────────────────────────
① 交互向导：不传输入源参数即进入（或显式 --interactive）
     python mps_video_dubbing.py

② CLI 模式：必须显式传入输入源 + 核心业务参数
     python mps_video_dubbing.py \\
         -i https://xxx.com/a.mp4 \\
         --mode ocr --src-lang zh --dst-lang en --burn-subtitle \\
         --subtitle-area preset \\
         --confirm-charges

   OCR + 自定义字幕区域坐标（示例 lt_x=53, lt_y=741, rb_x=953, rb_y=922）：
     python mps_video_dubbing.py \\
         -i https://xxx.com/a.mp4 \\
         --mode ocr --src-lang zh --dst-lang en --burn-subtitle \\
         --subtitle-area custom --subtitle-bbox 53,741,953,922 \\
         --confirm-charges

【核心业务参数必传（无默认值）】
────────────────────────────────────────────────────────────
   --mode                           必传：ocr 或 asr
   --src-lang                       必传：源语言 code
   --dst-lang                       必传：目标语言 code
   --burn-subtitle / --no-burn-subtitle  必传：二选一显式指定
   --subtitle-area                  OCR 模式必传：preset 或 custom
   --subtitle-bbox                  --subtitle-area=custom 时必传
   缺任一项 CLI 将直接报错退出，不会静默使用默认值。

【运维参数 — 区域/桶相关全部必填，无默认兜底】
────────────────────────────────────────────────────────────
   --cos-bucket     必填：从 $TENCENTCLOUD_COS_BUCKET 读取，未设置则报错
   --cos-region     必填：从 $TENCENTCLOUD_COS_REGION 读取，未设置则报错
   --output-dir     默认 /output/video-dubbing/
   --region         必填：从 $TENCENTCLOUD_API_REGION 读取，未设置则报错
   --poll-interval  默认 15 秒
   --max-wait       默认 3600 秒

费用确认（强约束）
────────────────────────────────────────────────────────────
  CLI 模式必须显式传 --confirm-charges，否则进入 dry-run 不提交
  交互模式必须键入 YES 才提交

查询与下载
────────────────────────────────────────────────────────────
   --query-task <TaskId>    查询任务结果
   --download-dir <目录>    任务完成后自动下载成品

环境变量（均为必需）
────────────────────────────────────────────────────────────
   TENCENTCLOUD_SECRET_ID / TENCENTCLOUD_SECRET_KEY  (必需，腾讯云 API 凭证)
   TENCENTCLOUD_COS_BUCKET / TENCENTCLOUD_COS_REGION (必需，COS 输入/输出桶与地域)
   TENCENTCLOUD_API_REGION                           (必需，MPS API 调用地域)

文档：https://cloud.tencent.com/document/product/862/124504
""",
    )

    # 输入源
    g_in = parser.add_argument_group("输入源（三选一，不传则进入交互向导）")
    g_in.add_argument("-i", "--input-url", help="视频公网 URL")
    g_in.add_argument("--local-file", help="本地文件路径（自动上传到 COS）")
    g_in.add_argument("--cos-input-bucket", help="COS 输入桶（仅 --cos-input-key 路径下生效，未传则沿用 --cos-bucket）")
    g_in.add_argument("--cos-input-region", help="COS 输入地域（仅 --cos-input-key 路径下生效，未传则沿用 --cos-region）")
    g_in.add_argument("--cos-input-key", help="COS 输入 key（如 input/video.mp4）")

    # 译制配置（核心业务参数全部必填，无默认值）
    g_cfg = parser.add_argument_group(
        "译制配置（核心业务参数必填，无默认值）"
    )
    g_cfg.add_argument("--mode", choices=["ocr", "asr"], default=None,
                       help="【必填】译制模式：ocr（OCR 提字幕+擦除+翻译+压制+克隆配音，适用硬字幕视频）"
                            "或 asr（语音识别+翻译+压制+克隆配音，适用无硬字幕视频）")
    g_cfg.add_argument("--src-lang", default=None,
                       help="【必填】源语言 code（如 zh/en/ja/ko/de/fr 等），用 --list-languages 查看全部")
    g_cfg.add_argument("--dst-lang", default=None,
                       help="【必填】目标语言 code")

    # 压制字幕：互斥必填组，必须显式二选一
    g_burn = g_cfg.add_mutually_exclusive_group(required=False)
    # 注意：required=False 是为了给交互向导路径留出空档；
    # CLI 路径会在 cli_to_config 中做二次校验，若既未传 --burn 也未传 --no-burn 则报错退出。
    g_burn.add_argument("--burn-subtitle", action="store_const", const=True,
                        dest="burn_subtitle",
                        help="【必填】压制翻译字幕到画面（与 --no-burn-subtitle 二选一必传）")
    g_burn.add_argument("--no-burn-subtitle", action="store_const", const=False,
                        dest="burn_subtitle",
                        help="【必填】不压制翻译字幕到画面（与 --burn-subtitle 二选一必传）")

    # OCR 字幕区域（仅 OCR 模式生效；ASR 模式忽略）
    g_area = parser.add_argument_group(
        "OCR 字幕区域（仅 --mode ocr 时生效；ASR 模式忽略）"
    )
    g_area.add_argument("--subtitle-area", choices=["preset", "custom"], default=None,
                        help="【OCR 必填】字幕区域模式：preset=后端预设（画面中部靠下，产物不写 als_filter）；"
                             "custom=自定义矩形坐标（需配合 --subtitle-bbox）")
    g_area.add_argument("--subtitle-bbox", type=_parse_bbox_str, default=None,
                        metavar="LTX,LTY,RBX,RBY",
                        help="【--subtitle-area=custom 必填】矩形 4 点整数像素坐标，"
                             "如 53,741,953,922（即 lt_x=53, lt_y=741, rb_x=953, rb_y=922）；"
                             "不需要预览窗口宽高")

    # 输出
    g_out = parser.add_argument_group("输出 COS（必填，从环境变量读取）")
    g_out.add_argument("--cos-bucket", help="输出桶（必填，未传则从 $TENCENTCLOUD_COS_BUCKET 读取，未设置则报错）")
    g_out.add_argument("--cos-region", help="输出地域（必填，未传则从 $TENCENTCLOUD_COS_REGION 读取，未设置则报错）")
    g_out.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR,
                       help=f"输出目录，默认 {DEFAULT_OUTPUT_DIR}")

    # 任务控制
    g_tk = parser.add_argument_group("任务控制")
    g_tk.add_argument("--no-wait", action="store_true", help="仅提交不等待（默认自动轮询）")
    g_tk.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
                      help=f"轮询间隔秒，默认 {DEFAULT_POLL_INTERVAL}")
    g_tk.add_argument("--max-wait", type=int, default=DEFAULT_MAX_WAIT,
                      help=f"最长等待秒，默认 {DEFAULT_MAX_WAIT}")
    g_tk.add_argument("--download-dir", help="完成后下载成品到本地目录")
    g_tk.add_argument("--session-id", help="任务去重识别码（同一 ID 在 3 天内重复提交会报错；适用于幂等重试场景）")

    # 其他
    g_misc = parser.add_argument_group("其他")
    g_misc.add_argument("--region",
                        default=os.environ.get("TENCENTCLOUD_API_REGION"),
                        help="MPS API 区域（必填，未传则从 $TENCENTCLOUD_API_REGION 读取，未设置则报错）")
    g_misc.add_argument("--interactive", action="store_true", help="强制进入交互向导")
    g_misc.add_argument("--confirm-charges", action="store_true",
                        help="【CLI 模式必需】确认已阅读并同意产生费用")
    g_misc.add_argument("--dry-run", action="store_true", help="只打印请求参数，不实际调用 API")
    g_misc.add_argument("--verbose", "-v", action="store_true", help="输出详细信息")

    # 工具
    parser.add_argument("--query-task", help="查询任务结果，传入 TaskId")
    parser.add_argument("--list-languages", action="store_true", help="列出支持的语种")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # 自动加载 /root/.env 之类
    if _LOAD_ENV_AVAILABLE:
        try:
            _ensure_env_loaded(verbose=args.verbose if hasattr(args, "verbose") else False)
        except SystemExit:
            raise
        except Exception as e:
            if args.verbose:
                print(f"⚠️  自动加载 env 失败：{e}", file=sys.stderr)

    # 工具命令
    if args.list_languages:
        list_languages()
        return

    if args.query_task:
        result = query_task(args.query_task, args.region)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 决定走哪条路径
    enter_wizard = args.interactive or not has_any_input_arg(args)

    # CLI 模式强校验：核心业务参数必传，一次性列出所有缺失项
    if not enter_wizard:
        missing = []
        if args.mode is None:
            missing.append("--mode  (ocr|asr)")
        if args.src_lang is None:
            missing.append("--src-lang  (源语言 code，如 zh/en/ja，完整列表见 --list-languages)")
        if args.dst_lang is None:
            missing.append("--dst-lang  (目标语言 code)")
        if args.burn_subtitle is None:
            missing.append("--burn-subtitle 或 --no-burn-subtitle  (二选一，显式指定是否压制字幕)")
        # OCR 模式额外要求 --subtitle-area
        if args.mode == "ocr" and args.subtitle_area is None:
            missing.append("--subtitle-area  (preset|custom，OCR 模式必填；"
                           "preset=画面中部靠下，custom 需配合 --subtitle-bbox)")
        if missing:
            print("\n❌ CLI 模式缺少核心业务参数（无默认值，必须显式指定）：", file=sys.stderr)
            for item in missing:
                print(f"   • {item}", file=sys.stderr)
            print("\n   示例：", file=sys.stderr)
            print("     python mps_video_dubbing.py -i <url> \\", file=sys.stderr)
            print("         --mode ocr --src-lang zh --dst-lang en --burn-subtitle \\", file=sys.stderr)
            print("         --confirm-charges", file=sys.stderr)
            print("\n   或不带参数运行，进入交互向导：python mps_video_dubbing.py\n", file=sys.stderr)
            sys.exit(2)
        # 源目标语言不能相同（与向导一致的保护）
        if args.src_lang == args.dst_lang:
            print(f"\n❌ 源语言和目标语言不能相同（均为 '{args.src_lang}'）", file=sys.stderr)
            sys.exit(2)
        # OCR + custom 必须同时提供 --subtitle-bbox
        if args.mode == "ocr" and args.subtitle_area == "custom" and args.subtitle_bbox is None:
            print("\n❌ --subtitle-area=custom 需要同时提供 --subtitle-bbox LTX,LTY,RBX,RBY", file=sys.stderr)
            print("   示例：--subtitle-area custom --subtitle-bbox 53,741,953,922", file=sys.stderr)
            sys.exit(2)
        # ASR 模式传了字幕区域参数 → 警告并忽略
        if args.mode == "asr" and (args.subtitle_area or args.subtitle_bbox):
            print("⚠️  ASR 模式不需要字幕区域参数，--subtitle-area / --subtitle-bbox 将被忽略",
                  file=sys.stderr)

    try:
        if enter_wizard:
            cfg = run_wizard(args)
        else:
            cfg = cli_to_config(args)

        # 本地文件 → 自动上传
        if cfg.get("local_file"):
            if not _POLL_AVAILABLE:
                print("❌ mps_poll_task 模块不可用，无法自动上传本地文件", file=sys.stderr)
                sys.exit(1)
            print(f"\n📤 本地文件 → COS 自动上传: {cfg['local_file']}")
            upload_result = auto_upload_local_file(cfg["local_file"])
            if not upload_result:
                print("❌ 本地文件上传失败，任务终止", file=sys.stderr)
                sys.exit(1)
            cfg["cos_input_bucket"] = upload_result["Bucket"]
            cfg["cos_input_region"] = upload_result["Region"]
            cfg["cos_input_key"]    = upload_result["Key"]
            cfg["input_url"] = None
            if not cfg.get("cos_bucket"):
                cfg["cos_bucket"] = upload_result["Bucket"]
            if not cfg.get("cos_region"):
                cfg["cos_region"] = upload_result["Region"]

        # 输出桶/地域兜底（缺值即报错退出）
        if not cfg.get("cos_bucket"):
            cfg["cos_bucket"] = os.environ.get("TENCENTCLOUD_COS_BUCKET", "")
        if not cfg.get("cos_region"):
            cfg["cos_region"] = os.environ.get("TENCENTCLOUD_COS_REGION", "")
        if not cfg["cos_bucket"]:
            print("❌ 输出桶缺失：请设置环境变量 TENCENTCLOUD_COS_BUCKET，或显式传 --cos-bucket",
                  file=sys.stderr)
            sys.exit(1)
        if not cfg["cos_region"]:
            print("❌ 输出地域缺失：请设置环境变量 TENCENTCLOUD_COS_REGION，或显式传 --cos-region",
                  file=sys.stderr)
            sys.exit(1)
        if not args.region:
            print("❌ MPS API 区域缺失：请设置环境变量 TENCENTCLOUD_API_REGION，或显式传 --region",
                  file=sys.stderr)
            sys.exit(1)

        # COS 输入桶兜底（若未填，沿用输出桶）
        if cfg.get("cos_input_key") and not cfg.get("cos_input_bucket"):
            cfg["cos_input_bucket"] = cfg["cos_bucket"]
        if cfg.get("cos_input_key") and not cfg.get("cos_input_region"):
            cfg["cos_input_region"] = cfg["cos_region"]

        # 当输入源为 COS 路径时，桶和地域必须有值
        if cfg.get("cos_input_key"):
            if not cfg.get("cos_input_bucket"):
                print("❌ COS 输入桶缺失：使用 --cos-input-key 时必须指定桶名。\n"
                      "   请通过 --cos-input-bucket 显式传入，或设置环境变量 TENCENTCLOUD_COS_BUCKET",
                      file=sys.stderr)
                sys.exit(1)
            if not cfg.get("cos_input_region"):
                print("❌ COS 输入地域缺失：使用 --cos-input-key 时必须指定地域。\n"
                      "   请通过 --cos-input-region 显式传入，或设置环境变量 TENCENTCLOUD_COS_REGION",
                      file=sys.stderr)
                sys.exit(1)

        # 校验语言
        if cfg["src_lang"] not in SUPPORTED_LANGUAGES:
            print(f"\n❌ 不支持的源语言 '{cfg['src_lang']}'，请从下列简写中选择：", file=sys.stderr)
            print_language_hint(title="   🌍 可用语言简写（请使用 --src-lang 重新指定）")
            sys.exit(1)
        if cfg["dst_lang"] not in SUPPORTED_LANGUAGES:
            print(f"\n❌ 不支持的目标语言 '{cfg['dst_lang']}'，请从下列简写中选择：", file=sys.stderr)
            print_language_hint(title="   🌍 可用语言简写（请使用 --dst-lang 重新指定）")
            sys.exit(1)

        # 费用确认（CLI 路径）
        dry_run = args.dry_run
        if not cfg.get("confirm_charges") and not dry_run:
            print()
            print("=" * 62)
            print("  ⚠️  未检测到 --confirm-charges，自动切换到 DRY-RUN 模式")
            print("=" * 62)
            print("  一站式译制任务将产生费用：")
            if cfg["mode"] == "ocr":
                print("    • 去字幕 + OCR + 翻译 + 压制字幕 + AI克隆配音")
            else:
                print("    • ASR 识别 + 翻译 + 压制字幕 + AI克隆配音")
            print("  计费详情：https://cloud.tencent.com/document/product/862/124504")
            print("  确认要提交，请在命令中加上 --confirm-charges")
            print("=" * 62)
            dry_run = True

        # 提交
        result = submit_video_dubbing(
            input_url=cfg.get("input_url"),
            cos_input_bucket=cfg.get("cos_input_bucket"),
            cos_input_region=cfg.get("cos_input_region"),
            cos_input_key=cfg.get("cos_input_key"),
            mode=cfg["mode"],
            src_lang=cfg["src_lang"],
            dst_lang=cfg["dst_lang"],
            burn_subtitle=cfg["burn_subtitle"],
            subtitle_area=cfg.get("subtitle_area", "preset"),
            bbox=cfg.get("bbox"),
            cos_bucket=cfg["cos_bucket"],
            cos_region=cfg["cos_region"],
            output_dir=cfg["output_dir"],
            session_id=cfg.get("session_id"),
            region=args.region,
            dry_run=dry_run,
        )

        if dry_run:
            return

        response = result.get("Response", result)
        task_id = response.get("TaskId", "")
        if not task_id:
            print("\n❌ 任务提交失败！原始响应：")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(1)

        print()
        print("=" * 62)
        print("  ✅ 一站式视频译制任务已提交！")
        print(f"  🆔 TaskId: {task_id}")
        print("=" * 62)

        # 轮询
        if not args.no_wait and _POLL_AVAILABLE:
            print("\n⏳ 开始轮询任务状态...")
            task_result = poll_video_task(
                task_id, region=args.region,
                interval=args.poll_interval, max_wait=args.max_wait,
                verbose=args.verbose,
            )
            if cfg.get("download_dir") or args.download_dir:
                download_dir = cfg.get("download_dir") or args.download_dir
                print(f"\n📥 下载结果到：{download_dir}")
                auto_download_outputs(task_result, download_dir=download_dir)
        else:
            print(f"\n查询任务状态：python {sys.argv[0]} --query-task {task_id}")

    except TencentCloudSDKException as e:
        print(f"\n❌ 腾讯云 SDK 错误：{e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 用户中止")
        sys.exit(130)


def cli_to_config(args: argparse.Namespace) -> dict:
    """把 argparse namespace 转换为统一 cfg dict（CLI 路径，不弹任何 prompt）。"""
    return {
        "local_file":        args.local_file,
        "input_url":         args.input_url,
        "cos_input_bucket":  args.cos_input_bucket,
        "cos_input_region":  args.cos_input_region,
        "cos_input_key":     args.cos_input_key,
        "mode":              args.mode,
        "src_lang":          args.src_lang,
        "dst_lang":          args.dst_lang,
        "burn_subtitle":     args.burn_subtitle,
        "subtitle_area":     (args.subtitle_area if args.mode == "ocr" else "preset"),
        "bbox":              (args.subtitle_bbox if args.mode == "ocr" and args.subtitle_area == "custom" else None),
        "cos_bucket":        args.cos_bucket,
        "cos_region":        args.cos_region,
        "output_dir":        args.output_dir,
        "download_dir":      args.download_dir,
        "session_id":        args.session_id,
        "confirm_charges":   args.confirm_charges,
    }


if __name__ == "__main__":
    main()
