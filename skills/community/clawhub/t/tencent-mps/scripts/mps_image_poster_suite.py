#!/usr/bin/env python3
"""
腾讯云 MPS AI 套图生成脚本

功能：
  基于商品主图，调用 MPS ProcessImage 接口的 AiPosterSuiteConfig，按指定主题列表
  批量产出多张广告海报 panel。支持 auto / modify 两种模式：
    - auto：服务自动从商品图提取信息（品牌、卖点、配色等）并生成整套 panel
    - modify：直接基于 ExtPrompt 中提供的变量集合生成，不做自动提取
  通过 DescribeImageTaskDetail 轮询等待结果，返回变量回显 + panel 图片列表。

  支持的 Definition（平台）：
    50=淘宝/天猫  51=亚马逊(Amazon)  52=京东  53=拼多多  54=Temu  55=TikTok

  标准主题（6 类，所有平台共享名称）：
    hero（主图）/ selling（卖点图）/ scene（场景图）
    detail（细节图）/ angles（多角度图）/ atmosphere（氛围图）

COS 存储约定：
  通过环境变量 TENCENTCLOUD_COS_BUCKET 指定输出 COS Bucket 名称。
  - 输出文件默认目录：/output/poster_suite/

用法：
  # Auto 模式（最少必填）
  python3 scripts/mps_image_poster_suite.py \\
      --product-url "https://example.com/product.jpg" \\
      --definition 50 \\
      --recipe hero:2 --recipe detail:2

  # Auto 模式 + 用户文案变量 + 自定义变量
  python3 scripts/mps_image_poster_suite.py \\
      --product-url "https://example.com/product.jpg" \\
      --definition 50 \\
      --recipe hero:2 --recipe detail:2 \\
      --panel-ratio 3:4 --panel-resolution 2K \\
      --ext-prompt BrandName AURASKIN \\
      --ext-prompt Headline "持续焕活" \\
      --user-prompt "瓶身 32cm，强调按压泵与磨砂质感"

  # Modify 模式（基于上一次 auto 结果迭代，必须回填所有 9 个标准变量）
  python3 scripts/mps_image_poster_suite.py \\
      --product-cos-key "/input/product.jpg" \\
      --definition 50 \\
      --recipe hero:2 --recipe detail:2 \\
      --mode modify \\
      --ext-prompt BrandName AURASKIN \\
      --ext-prompt Headline "敏感肌也能用的高效精华" \\
      --ext-prompt SellingPointsText "保湿 / 紧致 / 抗氧化" \\
      --ext-prompt ProductCategory "美妆-护肤" \\
      --ext-prompt ProductVisualIdentity "matte glass dropper bottle, amber" \\
      --ext-prompt TextureDescription "silky cream" \\
      --ext-prompt ColorPalette "#F5C2C7,#A8DADC,#F1FAEE" \\
      --ext-prompt TargetAudience "都市白领女性 22-35 岁" \\
      --ext-prompt SceneContext "晨间梳妆台" \\
      --user-prompt "Headline 字号再加大一档"

  # 只提交任务，不等待结果（返回 TaskId）
  python3 scripts/mps_image_poster_suite.py \\
      --product-url "https://example.com/product.jpg" \\
      --definition 50 --recipe hero:2 --recipe detail:2 --no-wait

环境变量：
  TENCENTCLOUD_SECRET_ID    - 腾讯云 SecretId（必须）
  TENCENTCLOUD_SECRET_KEY   - 腾讯云 SecretKey（必须）
  TENCENTCLOUD_API_REGION   - MPS API 接入地域（必需）
  TENCENTCLOUD_COS_BUCKET   - 输出 COS Bucket（可被 --output-bucket 覆盖）
                              同时作为 --product-cos-key / --image-cos-key 的默认 Bucket
  TENCENTCLOUD_COS_REGION   - 输出 COS Region（可被 --output-region 覆盖）
                              同时作为 --product-cos-key / --image-cos-key 的默认 Region
"""

import argparse
import json
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)
from mps_auto_upgrade import check_sdk_version

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False

try:
    from mps_poll_task import poll_image_task
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
# 默认参数
# =============================================================================
DEFAULT_OUTPUT_DIR = "/output/poster_suite/"
DEFAULT_POLL_INTERVAL = 10       # 套图生成较慢
DEFAULT_TIMEOUT = 1800            # 30 分钟（多 panel 生成）
DEFAULT_MODE = "auto"
DEFAULT_LANGUAGE = "zh-CN"
DEFAULT_PANEL_RATIO = "1:1"
DEFAULT_PANEL_RESOLUTION = "1K"
DEFAULT_MODEL = "WAND-suite-1.0-flash"

# Definition → 平台映射
PLATFORM_MAP = {
    50: "淘宝/天猫",
    51: "亚马逊(Amazon)",
    52: "京东",
    53: "拼多多",
    54: "Temu",
    55: "TikTok",
}

# 标准主题（6 类，所有平台共享名称）
THEME_OPTIONS = ["hero", "selling", "scene", "detail", "angles", "atmosphere"]

# 标准变量 Role（9 个，文档 §4）
STANDARD_VAR_ROLES = [
    "BrandName", "Headline", "SellingPointsText", "ProductCategory",
    "ProductVisualIdentity", "TextureDescription", "ColorPalette",
    "TargetAudience", "SceneContext",
]

PANEL_RATIOS = ["1:1", "3:2", "2:3", "3:4", "4:3", "9:16", "16:9"]
PANEL_RESOLUTIONS = ["720", "1K", "2K", "4K"]
LANGUAGES = ["zh-CN", "en-US"]
MODES = ["auto", "modify"]

MAX_ADDON_IMAGES = 3              # 附加商品视角图最多 3 张
RECIPE_NUM_RANGE = (1, 4)         # 单主题数量取值范围
RECIPE_TOTAL_RANGE = (4, 12)      # 全部 panel 总数取值范围


# =============================================================================
# 工具函数（与 mps_image_bg_fusion.py 保持一致的设计风格）
# =============================================================================

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


def get_cos_bucket():
    """从环境变量获取输出 COS Bucket 名称。"""
    return os.environ.get("TENCENTCLOUD_COS_BUCKET", "")


def get_cos_region():
    """从环境变量获取输出 COS Region。"""
    return os.environ.get("TENCENTCLOUD_COS_REGION", "")


def create_mps_client(cred, region):
    """创建 MPS 客户端。"""
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    http_profile.reqMethod = "POST"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return mps_client.MpsClient(cred, region, client_profile)


def build_url_input(url):
    """构造 URL 类型输入源。"""
    return {
        "Type": "URL",
        "UrlInputInfo": {"Url": url},
    }


def build_cos_input(cos_key, cos_bucket=None, cos_region=None):
    """构造 COS 类型输入源。"""
    bucket = cos_bucket or get_cos_bucket()
    region = cos_region or get_cos_region()
    if not bucket:
        print(
            "错误：COS 输入需要指定 Bucket，请通过对应 --*-cos-bucket 参数或 TENCENTCLOUD_COS_BUCKET 环境变量设置",
            file=sys.stderr,
        )
        sys.exit(1)
    return {
        "Type": "COS",
        "CosInputInfo": {
            "Bucket": bucket,
            "Region": region,
            "Object": cos_key if cos_key.startswith("/") else f"/{cos_key}",
        },
    }


def build_media_input(url=None, cos_key=None, cos_bucket=None, cos_region=None, label="图片"):
    """
    根据 url 或 cos_key 构造媒体输入源（二选一）。
    优先使用 url；若 url 为空则使用 cos_key。
    """
    if url:
        return build_url_input(url)
    if cos_key:
        return build_cos_input(cos_key, cos_bucket, cos_region)
    print(f"错误：请指定{label}输入源（--*-url 或 --*-cos-key）", file=sys.stderr)
    sys.exit(1)


def parse_recipe(recipe_args):
    """
    解析 --recipe 参数列表，格式为 "Theme:Num"（如 "hero:2"）。
    返回 [{"Theme": "hero", "Num": 2}, ...]
    """
    parsed = []
    total = 0
    for item in recipe_args:
        if ":" not in item:
            print(f"错误：--recipe 格式应为 'Theme:Num'（如 hero:2），收到: {item}", file=sys.stderr)
            sys.exit(1)
        theme, num_str = item.rsplit(":", 1)
        theme = theme.strip()
        num_str = num_str.strip()
        if theme not in THEME_OPTIONS:
            print(
                f"错误：Theme '{theme}' 不在标准主题列表 {THEME_OPTIONS} 中",
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            num = int(num_str)
        except ValueError:
            print(f"错误：--recipe Num 必须是整数，收到: {num_str}", file=sys.stderr)
            sys.exit(1)
        if not (RECIPE_NUM_RANGE[0] <= num <= RECIPE_NUM_RANGE[1]):
            print(
                f"错误：单主题 Num 取值范围 {RECIPE_NUM_RANGE[0]}-{RECIPE_NUM_RANGE[1]}，"
                f"Theme={theme} Num={num}",
                file=sys.stderr,
            )
            sys.exit(1)
        parsed.append({"Theme": theme, "Num": num})
        total += num

    if not parsed:
        print("错误：至少需要一个 --recipe 条目", file=sys.stderr)
        sys.exit(1)

    if not (RECIPE_TOTAL_RANGE[0] <= total <= RECIPE_TOTAL_RANGE[1]):
        print(
            f"错误：全部 panel 总数取值范围 {RECIPE_TOTAL_RANGE[0]}-{RECIPE_TOTAL_RANGE[1]}，"
            f"当前总数 {total}",
            file=sys.stderr,
        )
        sys.exit(1)

    return parsed, total


def build_request_payload(args):
    """组装 ProcessImage 请求体。"""
    # 解析 Recipe
    recipe_list, total_panels = parse_recipe(args.recipe)

    # 构造商品主图输入（必填）
    product_input = build_media_input(
        url=args.product_url,
        cos_key=args.product_cos_key,
        cos_bucket=args.product_cos_bucket,
        cos_region=args.product_cos_region,
        label="商品主图",
    )

    # 输出 Bucket/Region
    output_bucket = args.output_bucket or get_cos_bucket()
    output_region = args.output_region or get_cos_region()
    if not output_bucket:
        print(
            "错误：缺少输出 Bucket，请传入 --output-bucket 或设置 TENCENTCLOUD_COS_BUCKET",
            file=sys.stderr,
        )
        sys.exit(1)

    # AddOnParameter
    addon_parameter = {}

    # ImageSet：附加商品视角图（最多 3 张）
    image_set = []
    for url in args.image_url or []:
        image_set.append({"Image": build_url_input(url)})
    for key in args.image_cos_key or []:
        image_set.append({
            "Image": build_cos_input(key, args.image_cos_bucket, args.image_cos_region)
        })
    if len(image_set) > MAX_ADDON_IMAGES:
        print(
            f"错误：附加商品视角图最多 {MAX_ADDON_IMAGES} 张，当前 {len(image_set)} 张",
            file=sys.stderr,
        )
        sys.exit(1)
    if image_set:
        addon_parameter["ImageSet"] = image_set

    # ExtPrompt：用户文案变量 + 自由文
    ext_prompts = []
    user_prompt_count = 0
    for role, prompt in args.ext_prompt or []:
        ext_prompts.append({"Role": role, "Prompt": prompt})
        if role == "UserPrompt":
            user_prompt_count += 1
    if args.user_prompt:
        user_prompt_count += 1
        ext_prompts.append({"Role": "UserPrompt", "Prompt": args.user_prompt})

    # 整请求至多 1 条 UserPrompt
    if user_prompt_count > 1:
        print(
            f"错误：UserPrompt 整请求至多 1 条，当前 {user_prompt_count} 条"
            "（--ext-prompt UserPrompt 与 --user-prompt 不可同时使用）",
            file=sys.stderr,
        )
        sys.exit(1)

    # modify 模式：必须回填 auto 获得的所有标准变量（9 个）
    # 业务规则：modify 不做自动提取，必须把上一次 auto 响应 [0].Output.Content 中
    # 解析出的所有变量原样塞回 ExtPrompt（可修改字段值），不可只传子集。
    if args.mode == "modify":
        provided_roles = {role for role, _ in (args.ext_prompt or [])}
        missing_roles = [r for r in STANDARD_VAR_ROLES if r not in provided_roles]
        if missing_roles:
            print(
                f"错误：modify 模式必须回填 auto 获得的所有标准变量（{len(STANDARD_VAR_ROLES)} 个），"
                f"不可只传子集。缺失 Role: {missing_roles}\n"
                f"标准变量 Role 全集: {STANDARD_VAR_ROLES}\n"
                "请先执行 auto 模式，从响应 [0].Output.Content 解析变量回显后"
                "全部塞回 ExtPrompt（可修改某些字段值）",
                file=sys.stderr,
            )
            sys.exit(1)

    if ext_prompts:
        addon_parameter["ExtPrompt"] = ext_prompts

    # 构造 AiPosterSuiteConfig
    poster_suite_config = {
        "Mode": args.mode,
        "Definition": args.definition,
        "Recipe": recipe_list,
        "Language": args.language,
        "PanelRatio": args.panel_ratio,
        "PanelResolution": args.panel_resolution,
        "Model": args.model,
    }

    # CustomVariables：仅 auto 模式可用
    if args.custom_variable:
        if args.mode != "auto":
            print(
                "错误：--custom-variable 仅 auto 模式可用，modify 模式不支持",
                file=sys.stderr,
            )
            sys.exit(1)
        # 校验 Type 唯一性
        seen_types = set()
        for var_type, desc in args.custom_variable:
            if var_type == "UserPrompt":
                print(
                    "错误：CustomVariables 的 Type 不可与 UserPrompt 同名",
                    file=sys.stderr,
                )
                sys.exit(1)
            if var_type in seen_types:
                print(
                    f"错误：CustomVariables 的 Type 不可重复，重复 Type: {var_type}",
                    file=sys.stderr,
                )
                sys.exit(1)
            seen_types.add(var_type)
            poster_suite_config.setdefault("CustomVariables", []).append(
                {"Type": var_type, "Description": desc}
            )

    payload = {
        "InputInfo": product_input,
        "OutputStorage": {
            "Type": "COS",
            "CosOutputStorage": {
                "Bucket": output_bucket,
                "Region": output_region,
            },
        },
        "OutputDir": args.output_dir,
        "ImageTask": {
            "AiPosterSuiteConfig": poster_suite_config,
        },
        "AddOnParameter": addon_parameter,
    }

    if args.resource_id:
        payload["ResourceId"] = args.resource_id

    return payload, total_panels


def submit_process_image(client, payload):
    """调用 ProcessImage 提交套图生成任务。"""
    req = models.ProcessImageRequest()
    req.from_json_string(json.dumps(payload, ensure_ascii=False))
    resp = client.ProcessImage(req)
    result = json.loads(resp.to_json_string())
    # 兼容 SDK 返回格式
    if "Response" in result:
        result = result["Response"]
    return result


# =============================================================================
# 参数解析
# =============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="腾讯云 MPS AI 套图生成（ProcessImage AiPosterSuiteConfig）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # 输入参数
    input_group = parser.add_argument_group("输入参数")
    # 商品主图（URL 或 COS，二选一，必填）
    product_group = input_group.add_mutually_exclusive_group(required=True)
    product_group.add_argument(
        "--product-url",
        help="商品主图 URL（与 --product-cos-key 二选一）",
    )
    product_group.add_argument(
        "--product-cos-key",
        help="商品主图 COS 对象 Key（如 /input/product.jpg），与 --product-url 二选一",
    )
    input_group.add_argument(
        "--product-cos-bucket",
        help="商品主图 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--product-cos-region",
        help="商品主图 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )
    # 附加商品视角图（最多 3 张）
    input_group.add_argument(
        "--image-url", action="append", metavar="URL",
        help=f"附加商品视角图 URL，可重复传入多次（最多 {MAX_ADDON_IMAGES} 张）",
    )
    input_group.add_argument(
        "--image-cos-key", action="append", metavar="KEY",
        help=f"附加商品视角图 COS 对象 Key，可重复传入多次（最多 {MAX_ADDON_IMAGES} 张）",
    )
    input_group.add_argument(
        "--image-cos-bucket",
        help="附加商品视角图 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    input_group.add_argument(
        "--image-cos-region",
        help="附加商品视角图 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )

    # 套图配置参数
    suite_group = parser.add_argument_group("套图配置参数")
    suite_group.add_argument(
        "--definition", type=int, required=True, choices=sorted(PLATFORM_MAP.keys()),
        help=f"模板包 ID（必填）："
             + " / ".join(f"{k}={v}" for k, v in sorted(PLATFORM_MAP.items())),
    )
    suite_group.add_argument(
        "--recipe", action="append", required=True, metavar="THEME:NUM",
        help=f"主题与数量，格式 'Theme:Num'（如 hero:2）。可重复；"
             f"Theme ∈ {THEME_OPTIONS}；单主题 Num {RECIPE_NUM_RANGE[0]}-{RECIPE_NUM_RANGE[1]}；"
             f"总数 {RECIPE_TOTAL_RANGE[0]}-{RECIPE_TOTAL_RANGE[1]}",
    )
    suite_group.add_argument(
        "--mode", choices=MODES, default=DEFAULT_MODE,
        help=f"执行模式（默认 {DEFAULT_MODE}）：auto 自动提取变量 / modify 基于 ExtPrompt 生成",
    )
    suite_group.add_argument(
        "--language", choices=LANGUAGES, default=DEFAULT_LANGUAGE,
        help=f"文案语言（默认 {DEFAULT_LANGUAGE}）",
    )
    suite_group.add_argument(
        "--panel-ratio", choices=PANEL_RATIOS, default=DEFAULT_PANEL_RATIO,
        help=f"Panel 宽高比（默认 {DEFAULT_PANEL_RATIO}）",
    )
    suite_group.add_argument(
        "--panel-resolution", choices=PANEL_RESOLUTIONS, default=DEFAULT_PANEL_RESOLUTION,
        help=f"Panel 分辨率（默认 {DEFAULT_PANEL_RESOLUTION}）",
    )
    suite_group.add_argument(
        "--model", default=DEFAULT_MODEL,
        help=f"模型（默认 {DEFAULT_MODEL}）",
    )

    # ExtPrompt（用户文案变量）
    ext_group = parser.add_argument_group("ExtPrompt（用户文案变量）")
    ext_group.add_argument(
        "--ext-prompt", nargs=2, action="append", metavar=("ROLE", "PROMPT"),
        help=f"用户文案变量条目，格式 'Role Prompt'（如 --ext-prompt BrandName AURASKIN）。"
             f"可重复；标准 Role: {STANDARD_VAR_ROLES}；"
             f"modify 模式必须回填所有 {len(STANDARD_VAR_ROLES)} 个标准变量（不可只传子集）",
    )
    ext_group.add_argument(
        "--user-prompt", metavar="TEXT",
        help="自由文条目（Role=UserPrompt），整请求至多 1 条；"
             "用于补充硬性事实/数字/限制等内容",
    )

    # 自定义变量（仅 auto 模式）
    custom_group = parser.add_argument_group("自定义变量（仅 auto 模式）")
    custom_group.add_argument(
        "--custom-variable", nargs=2, action="append", metavar=("TYPE", "DESC"),
        help="自定义变量条目，格式 'Type Description'（如 --custom-variable MaterialKeyword '材质关键词'）。"
             "可重复；Type 用 PascalCase，不可与 UserPrompt 同名，不可重名",
    )

    # 输出参数
    output_group = parser.add_argument_group("输出参数")
    output_group.add_argument(
        "--output-bucket",
        help="输出 COS Bucket（默认读取 TENCENTCLOUD_COS_BUCKET）",
    )
    output_group.add_argument(
        "--output-region",
        help="输出 COS Region（默认读取 TENCENTCLOUD_COS_REGION）",
    )
    output_group.add_argument(
        "--output-dir", default=DEFAULT_OUTPUT_DIR,
        help=f"输出目录（默认 {DEFAULT_OUTPUT_DIR}）",
    )

    # 任务控制
    task_group = parser.add_argument_group("任务控制")
    task_group.add_argument(
        "--no-wait", action="store_true",
        help="只提交任务，不等待结果（返回 TaskId 后退出）",
    )
    task_group.add_argument(
        "--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL,
        help=f"轮询间隔秒数（默认 {DEFAULT_POLL_INTERVAL}）",
    )
    task_group.add_argument(
        "--timeout", type=int, default=DEFAULT_TIMEOUT,
        help=f"最长等待时间秒数（默认 {DEFAULT_TIMEOUT}）",
    )
    task_group.add_argument(
        "--dry-run", action="store_true",
        help="模拟执行，打印请求 payload 不实际调用 API",
    )

    # 认证与地域
    auth_group = parser.add_argument_group("认证与地域")
    auth_group.add_argument(
        "--region",
        default=os.environ.get("TENCENTCLOUD_API_REGION", ""),
        help="MPS API 接入地域（默认读取 TENCENTCLOUD_API_REGION，否则 ap-guangzhou）",
    )
    auth_group.add_argument(
        "--secret-id",
        help="腾讯云 SecretId（不传则读取环境变量 TENCENTCLOUD_SECRET_ID）",
    )
    auth_group.add_argument(
        "--secret-key",
        help="腾讯云 SecretKey（不传则读取环境变量 TENCENTCLOUD_SECRET_KEY）",
    )
    auth_group.add_argument(
        "--resource-id",
        help="可选的资源 ID（业务侧专属资源）",
    )

    return parser.parse_args()


# =============================================================================
# 主流程
# =============================================================================

# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    # 时序修复：先加载 .env，让 argparse default=os.environ.get(...) 能读到用户配置
    if _LOAD_ENV_AVAILABLE:
        try:
            _ensure_env_loaded(verbose=False)
        except Exception:
            pass
    args = parse_args()

    # 解析 payload
    try:
        payload, total_panels = build_request_payload(args)
    except SystemExit:
        raise
    except Exception as e:
        print(f"错误：构造请求失败 - {e}", file=sys.stderr)
        sys.exit(1)

    platform_name = PLATFORM_MAP.get(args.definition, str(args.definition))

    # dry-run 模式：只打印 payload
    if args.dry_run:
        print("=== Dry-run 模式：模拟执行 ===\n")
        print(f"模式: {args.mode}")
        print(f"平台: {args.definition} ({platform_name})")
        print(f"Panel 总数: {total_panels}")
        print(f"模型: {args.model}")
        if args.product_url:
            print(f"商品主图: {args.product_url}")
        else:
            bucket = args.product_cos_bucket or get_cos_bucket()
            print(f"商品主图: COS - {bucket}:{args.product_cos_key}")
        print()
        print("请求 payload:")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print("\n不会实际调用 API。移除 --dry-run 参数后执行实际操作。")
        return

    cred = get_credentials()
    region = args.region
    client = create_mps_client(cred, region)

    print(f"🚀 提交套图生成任务...")
    print(f"   模式: {args.mode}")
    print(f"   平台: {args.definition} ({platform_name})")
    print(f"   Panel 总数: {total_panels}")
    print(f"   模型: {args.model}")
    # 打印商品主图来源
    if args.product_url:
        print(f"   商品主图: {args.product_url}")
    else:
        bucket = args.product_cos_bucket or get_cos_bucket()
        print(f"   商品主图: COS - {bucket}:{args.product_cos_key}")
    # 打印附加商品视角图
    addon_count = len(args.image_url or []) + len(args.image_cos_key or [])
    if addon_count > 0:
        print(f"   附加商品视角图: {addon_count} 张")
    # 打印 ExtPrompt
    if args.ext_prompt:
        for role, prompt in args.ext_prompt:
            print(f"   ExtPrompt[{role}]: {prompt}")
    if args.user_prompt:
        print(f"   ExtPrompt[UserPrompt]: {args.user_prompt}")
    # 打印 CustomVariables
    if args.custom_variable:
        for var_type, desc in args.custom_variable:
            print(f"   CustomVariable[{var_type}]: {desc}")

    try:
        submit_result = submit_process_image(client, payload)
    except TencentCloudSDKException as e:
        print(f"错误：提交任务失败 - {e}", file=sys.stderr)
        sys.exit(1)

    task_id = submit_result.get("TaskId", "N/A")
    print(f"✅ 套图生成任务提交成功！")
    print(f"   TaskId: {task_id}")
    print(f"   RequestId: {submit_result.get('RequestId', 'N/A')}")
    print(f"\n## TaskId: {task_id}")

    if args.no_wait:
        print(json.dumps({"TaskId": task_id, "RequestId": submit_result.get("RequestId")},
                         ensure_ascii=False, indent=2))
        return

    # 轮询等待结果
    if not _POLL_AVAILABLE:
        print("⚠️  轮询模块不可用，请手动查询：", file=sys.stderr)
        print(f"   python3 scripts/mps_get_image_task.py --task-id {task_id}", file=sys.stderr)
        print(json.dumps({"TaskId": task_id}, ensure_ascii=False, indent=2))
        return

    task_result = poll_image_task(
        task_id=task_id,
        region=region,
        interval=args.poll_interval,
        max_wait=args.timeout,
        verbose=False,
    )

    if task_result is None:
        print(f"\n⚠️  轮询超时，任务可能仍在处理中。", file=sys.stderr)
        print(f"   可手动查询：python3 scripts/mps_get_image_task.py --task-id {task_id}", file=sys.stderr)
        sys.exit(1)

    # 输出最终结果
    err_msg = task_result.get("ErrMsg") or ""
    if err_msg:
        print(f"\n❌ 套图生成任务失败：ErrCode={task_result.get('ErrCode')}，ErrMsg={err_msg}",
              file=sys.stderr)
        sys.exit(1)

    # 解析结果集：[0] 变量回显（JSON 字符串），[1..N] panel 图片
    result_set = task_result.get("ImageProcessTaskResultSet") or []
    variable_echo = None
    panels = []

    for idx, item in enumerate(result_set):
        output = item.get("Output") or {}
        path = output.get("Path", "")
        content = output.get("Content", "")
        storage = (output.get("OutputStorage") or {}).get("CosOutputStorage") or {}
        bucket = storage.get("Bucket", "")
        region_out = storage.get("Region", "")

        if idx == 0 and content and not path:
            # 变量回显条目：解析 JSON 字符串
            try:
                variable_echo = json.loads(content)
                print(f"\n📝 变量回显（可用于 modify 模式迭代）：")
                print(json.dumps(variable_echo, ensure_ascii=False, indent=2))
            except (json.JSONDecodeError, ValueError):
                # 解析失败则跳过，当作普通结果处理
                variable_echo = content
            continue

        # panel 图片条目
        panel = {
            "theme_label": content or f"panel_{idx}",
            "bucket": bucket,
            "region": region_out,
            "path": path,
            "cos_uri": f"cos://{bucket}{path}" if bucket and path else None,
            "url": f"https://{bucket}.cos.{region_out}.myqcloud.com{path}" if bucket and path else None,
        }
        panels.append(panel)
        # 打印每个 panel 的下载链接
        label = content or f"panel_{idx}"
        if panel["url"]:
            print(f"   [{label}] 下载链接: [{label}]({panel['url']})")
        elif panel["cos_uri"]:
            print(f"   [{label}] COS 路径: {panel['cos_uri']}")

    final_result = {
        "TaskId": task_id,
        "Status": task_result.get("Status"),
        "CreateTime": task_result.get("CreateTime"),
        "FinishTime": task_result.get("FinishTime"),
        "VariableEcho": variable_echo,
        "Panels": panels,
    }

    print("\n=== 最终结果 ===")
    print(json.dumps(final_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已中断", file=sys.stderr)
        sys.exit(1)
