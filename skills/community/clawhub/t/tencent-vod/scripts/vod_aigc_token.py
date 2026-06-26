#!/usr/bin/env python3
"""
腾讯云 VOD AIGC API Token 管理工具

用途：管理 VOD AIGC 生文接口所需的 API Token（APIKey）。
Token 没有过期时间，创建后需等约 1 分钟同步到网关。
每个用户最多 50 个 Token。

子命令：
  create   创建新 Token
  delete   删除指定 Token
  list     查询 Token 列表
  usage    查询 AIGC 用量统计（Video/Image/Text）

用法示例：
  python scripts/vod_aigc_token.py create
  python scripts/vod_aigc_token.py list
  python scripts/vod_aigc_token.py delete --api-token <api_token>
  python scripts/vod_aigc_token.py usage --type Text --start 2026-03-01 --end 2026-03-19
  python scripts/vod_aigc_token.py usage --type Video --start 2026-03-01 --end 2026-03-19
"""

import argparse
import json
import os
import re
import sys

# 软依赖：vod_load_env 用于在凭证缺失时从 ~/.env 等 dotenv 文件兜底加载
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_auto_upgrade import check_sdk_version

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
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.vod.v20180717 import vod_client, models
except ImportError:
    print("❌ 缺少依赖，请先安装：pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)

DEFAULT_REGION = "ap-guangzhou"


def get_client(region: str = DEFAULT_REGION):
    """创建 VOD 客户端。若环境变量缺失则尝试从 dotenv 文件自动加载。"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        # 兜底：尝试从 ~/.env 等 dotenv 文件加载
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] 环境变量未设置，尝试从 dotenv 文件自动加载...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from vod_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print("❌ 未配置腾讯云密钥，请设置环境变量：", file=sys.stderr)
                print("   TENCENTCLOUD_SECRET_ID", file=sys.stderr)
                print("   TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
            sys.exit(1)
    cred = credential.Credential(secret_id, secret_key)
    return vod_client.VodClient(cred, region)


# ─────────────────────────────────────────────
# Token 管理接口
# ─────────────────────────────────────────────

def create_token(client, sub_app_id: int = None) -> dict:
    """
    创建 AIGC API Token。
    Token 无过期时间，创建后需等约 1 分钟同步到网关。
    """
    req = models.CreateAigcApiTokenRequest()
    if sub_app_id:
        req.SubAppId = sub_app_id
    resp = client.CreateAigcApiToken(req)
    return json.loads(resp.to_json_string())


def delete_token(client, api_token: str, sub_app_id: int = None) -> None:
    """
    删除 AIGC API Token。
    删除后需短暂时间（约 1 分钟）才能在网关失效。

    参数:
        api_token: 要删除的 API Token 字符串（非 TokenId）
        sub_app_id: VOD 子应用 ID（2023年12月后开通的用户必填）
    """
    req = models.DeleteAigcApiTokenRequest()
    req.ApiToken = api_token
    if sub_app_id:
        req.SubAppId = sub_app_id
    client.DeleteAigcApiToken(req)


def list_tokens(client, sub_app_id: int = None) -> dict:
    """查询 AIGC API Token 列表"""
    req = models.DescribeAigcApiTokensRequest()
    if sub_app_id:
        req.SubAppId = sub_app_id
    resp = client.DescribeAigcApiTokens(req)
    return json.loads(resp.to_json_string())


def describe_aigc_usage(
    client,
    start_time: str,
    end_time: str,
    aigc_type: str,
    sub_app_id: int = None,
) -> dict:
    """
    查询 AIGC 用量统计数据。
    aigc_type: Video | Image | Text
    start_time/end_time: ISO 格式，如 2026-03-01T00:00:00+08:00
    """
    req = models.DescribeAigcUsageDataRequest()
    req.StartTime = start_time
    req.EndTime   = end_time
    req.AigcType  = aigc_type
    if sub_app_id:
        req.SubAppId = sub_app_id
    resp = client.DescribeAigcUsageData(req)
    return json.loads(resp.to_json_string())


# ─────────────────────────────────────────────
# 输出格式化
# ─────────────────────────────────────────────

# 候选 dotenv 文件路径（与 vod_load_env._ENV_FILES 保持一致，仅扫描 dotenv 风格文件）
_ALL_ENV_FILES = [
    os.path.expanduser("~/.env"),
    os.path.join(os.getcwd(), ".env"),
]

_TOKEN_KEY = "TENCENTCLOUD_VOD_AIGC_TOKEN"
_DEFAULT_ENV_FILE = os.path.expanduser("~/.env")


def _update_token_in_file(filepath: str, token: str) -> bool:
    """
    在指定文件中更新或追加 TENCENTCLOUD_VOD_AIGC_TOKEN。
    如果文件中已有该行则替换，否则追加。
    返回 True 表示成功。
    """
    try:
        lines = []
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()

        new_lines = []
        found = False
        for line in lines:
            stripped = line.strip()
            # 匹配 KEY=... 或 export KEY=... 格式
            if re.match(rf"""^\s*(?:export\s+)?{_TOKEN_KEY}\s*=""", stripped):
                new_lines.append(f'export {_TOKEN_KEY}="{token}"\n')
                found = True
            else:
                new_lines.append(line)

        if not found:
            # 追加时确保文件末尾有换行
            if new_lines and not new_lines[-1].endswith("\n"):
                new_lines.append("\n")
            new_lines.append(f'export {_TOKEN_KEY}="{token}"\n')

        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        return True
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception as e:
        print(f"⚠️  写入 {filepath} 失败: {e}", file=sys.stderr)
        return False


def find_token_in_env_files() -> list:
    """
    扫描所有候选配置文件，返回包含 TENCENTCLOUD_VOD_AIGC_TOKEN 的文件路径列表。
    """
    found_files = []
    token_re = re.compile(rf"""^\s*(?:export\s+)?{_TOKEN_KEY}\s*=""")
    for filepath in _ALL_ENV_FILES:
        if not os.path.isfile(filepath):
            continue
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    if token_re.match(line):
                        found_files.append(filepath)
                        break
        except (OSError, IOError):
            pass
    return found_files


def save_token_to_env(token: str) -> list:
    """
    将 Token 写入环境变量配置文件。
    策略：
      1. 扫描所有候选文件，找到已包含 TENCENTCLOUD_VOD_AIGC_TOKEN 的文件，全部更新。
      2. 如果所有文件中都没有该变量，则仅写入 ~/.env。
    返回：成功写入的文件路径列表。
    """
    target_files = find_token_in_env_files()

    if not target_files:
        # 所有文件都没有配置，默认写入 ~/.env
        target_files = [_DEFAULT_ENV_FILE]

    written = []
    for filepath in target_files:
        if _update_token_in_file(filepath, token):
            written.append(filepath)

    return written


def print_token_created(data: dict, as_json: bool = False):
    """打印创建结果"""
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    sep = "=" * 60
    print(f"\n{sep}")
    print("✅ AIGC API Token 创建成功")
    print("─" * 60)
    # API 返回字段为 ApiToken（无 TokenId）
    token_id = data.get("TokenId", data.get("ApiTokenId", "-"))
    token    = data.get("ApiToken", data.get("Token", "-"))
    print(f"  Token ID : {token_id}")
    print(f"  Token    : {token}")
    print()
    # 自动写入环境变量配置文件
    if token and token != "-":
        written_files = save_token_to_env(token)
        if written_files:
            for f in written_files:
                print(f"💾 已自动写入 {f} (TENCENTCLOUD_VOD_AIGC_TOKEN)")
    print()
    print("⚠️  注意事项：")
    print("  1. Token 没有过期时间，请妥善保管")
    print("  2. 创建后需等约 1 分钟同步到网关，请勿立即使用")
    print("  3. 每个用户最多 50 个 Token")
    print(f"{sep}\n")


def print_token_list(data: dict, as_json: bool = False):
    """打印 Token 列表"""
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    sep = "=" * 60
    # API 返回 ApiTokens（字符串数组）或 AigcApiTokenSet（对象数组），兼容两种格式
    raw_tokens = data.get("ApiTokens") or data.get("AigcApiTokenSet") or []
    total  = len(raw_tokens)
    print(f"\n{sep}")
    print(f"AIGC API Token 列表（共 {total} 个）")
    print("─" * 60)
    if not raw_tokens:
        print("  暂无 Token，请先使用 create 子命令创建")
    else:
        for i, t in enumerate(raw_tokens, 1):
            if isinstance(t, str):
                # ApiTokens 格式：字符串数组
                masked = t[:8] + "..." + t[-4:] if len(t) > 12 else t
                print(f"  [{i}] Token : {masked}")
            else:
                # AigcApiTokenSet 格式：对象数组
                token_id    = t.get("TokenId", "-")
                token       = t.get("Token", "-")
                create_time = t.get("CreateTime", "-")
                print(f"  [{i}] Token ID   : {token_id}")
                print(f"      Token      : {token}")
                print(f"      创建时间   : {create_time}")
            print()
    print(f"{sep}\n")


def print_usage_data(data: dict, aigc_type: str, as_json: bool = False):
    """打印 AIGC 用量统计"""
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    sep = "=" * 60
    dataset = data.get("AigcUsageDataSet", [])
    print(f"\n{sep}")
    print(f"AIGC 用量统计（类型: {aigc_type}）")
    print("─" * 60)
    if not dataset:
        print("  暂无用量数据")
    else:
        total_count = 0
        total_usage = 0
        for spec_item in dataset:
            spec = spec_item.get("Specification", "-")
            rows = spec_item.get("DataSet", [])
            spec_count = sum(r.get("Count", 0) for r in rows)
            spec_usage = sum(r.get("Usage", 0) for r in rows)
            if spec_count == 0 and spec_usage == 0:
                continue
            print(f"  规格: {spec}")
            print(f"  {'日期':<30} {'任务数':>8} {'用量':>10}")
            print(f"  {'─'*30} {'─'*8} {'─'*10}")
            for row in rows:
                t   = row.get("Time", "-")[:10]  # 只取日期部分
                cnt = row.get("Count", 0)
                usg = row.get("Usage", 0)
                if cnt > 0 or usg > 0:
                    print(f"  {t:<30} {cnt:>8} {usg:>10}")
            print(f"  {'小计':<30} {spec_count:>8} {spec_usage:>10}")
            print()
            total_count += spec_count
            total_usage += spec_usage
        print("─" * 60)
        print(f"  {'合计':<30} {total_count:>8} {total_usage:>10}")
    print(f"{sep}\n")


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        description="腾讯云 VOD AIGC API Token 管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--region", default=DEFAULT_REGION,
                        help=f"地域（默认 {DEFAULT_REGION}）")
    parser.add_argument("--sub-app-id", type=int,
                        default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                        help="VOD 子应用 ID（2023年12月后开通的用户必须填写，也可通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="JSON 格式输出")
    parser.add_argument("--dry-run", action="store_true",
                        help="只打印参数预览，不调用 API")

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    _sub_app_id_kwargs = dict(
        type=int,
        default=None,
        help="VOD 子应用 ID（也可放在全局参数位置或通过环境变量 TENCENTCLOUD_VOD_SUB_APP_ID 设置）",
    )

    # ── create ──
    p_create = subparsers.add_parser("create", help="创建新的 AIGC API Token")
    p_create.add_argument("--sub-app-id", **_sub_app_id_kwargs)

    # ── delete ──
    p_delete = subparsers.add_parser("delete", help="删除指定 AIGC API Token")
    p_delete.add_argument("--api-token", required=True,
                          help="要删除的 API Token 字符串（通过 list 查询获取）")
    p_delete.add_argument("--sub-app-id", **_sub_app_id_kwargs)

    # ── list ──
    p_list = subparsers.add_parser("list", help="查询所有 AIGC API Token 列表")
    p_list.add_argument("--sub-app-id", **_sub_app_id_kwargs)

    # ── usage ──
    p_usage = subparsers.add_parser("usage", help="查询 AIGC 用量统计（Video/Image/Text）")
    p_usage.add_argument("--sub-app-id", **_sub_app_id_kwargs)
    p_usage.add_argument(
        "--type", "-t",
        dest="aigc_type",
        choices=["Video", "Image", "Text"],
        required=True,
        help="AIGC 类型：Video（视频）、Image（图片）、Text（文本）",
    )
    p_usage.add_argument(
        "--start",
        default=None,
        help="起始日期，格式 YYYY-MM-DD 或完整 ISO 格式（如 2026-03-01），默认为 30 天前",
    )
    p_usage.add_argument(
        "--end",
        default=None,
        help="结束日期，格式 YYYY-MM-DD 或完整 ISO 格式（如 2026-03-19），默认为今天",
    )

    return parser


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 合并 sub-app-id：子命令级别的优先，其次是全局，最后是环境变量
    sub_app_id = getattr(args, "sub_app_id", None) or int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None

    if args.dry_run:
        print("🔍 dry-run 参数预览:")
        print(f"  command    = {args.command}")
        print(f"  region     = {args.region}")
        if sub_app_id:
            print(f"  sub-app-id = {sub_app_id}")
        if args.command == "delete":
            print(f"  api-token  = {args.api_token}")
        if args.command == "usage":
            from datetime import datetime, timedelta
            today = datetime.now()
            default_start = (today - timedelta(days=30)).strftime("%Y-%m-%d")
            default_end = today.strftime("%Y-%m-%d")
            print(f"  type       = {args.aigc_type}")
            print(f"  start      = {args.start or default_start} (默认30天前)" if not args.start else f"  start      = {args.start}")  # NOCA:line-too-long(content cannot be shortened)
            print(f"  end        = {args.end or default_end} (默认今天)" if not args.end else f"  end        = {args.end}")
        return

    client = get_client(args.region)

    # --json 模式下进度信息输出到 stderr，避免污染 JSON stdout
    _out = sys.stderr if args.json_output else sys.stdout

    try:
        if args.command == "create":
            # 检测环境变量中是否已有 Token
            existing_token = os.environ.get("TENCENTCLOUD_VOD_AIGC_TOKEN", "").strip()
            if existing_token:
                masked = existing_token[:8] + "..." + existing_token[-4:] if len(existing_token) > 12 else existing_token[:4] + "..."  # NOCA:line-too-long(content cannot be shortened)
                print(f"⚠️  检测到环境变量中已存在 AIGC Token：{masked}", file=_out)
                # 扫描哪些文件中有配置
                files_with_token = find_token_in_env_files()
                if files_with_token:
                    print("   以下配置文件中存在 TENCENTCLOUD_VOD_AIGC_TOKEN，创建后将全部更新：", file=_out)
                    for f in files_with_token:
                        print(f"     • {f}", file=_out)
                else:
                    print(f"   创建新 Token 后将写入 {_DEFAULT_ENV_FILE}", file=_out)
                try:
                    answer = input("   是否继续创建新 Token？[y/N] ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    answer = "n"
                if answer not in ("y", "yes"):
                    print("⏭️  已取消，保留现有 Token。", file=_out)
                    sys.exit(0)
            print("🚀 创建 AIGC API Token...", file=_out)
            data = create_token(client, sub_app_id=sub_app_id)
            print_token_created(data, as_json=args.json_output)

        elif args.command == "delete":
            print(f"🗑️  删除 Token: {args.api_token}", file=_out)
            delete_token(client, api_token=args.api_token, sub_app_id=sub_app_id)
            print(f"✅ Token {args.api_token} 已删除（约 1 分钟后在网关失效）", file=_out)

        elif args.command == "list":
            print("🔍 查询 AIGC API Token 列表...", file=_out)
            data = list_tokens(client, sub_app_id=sub_app_id)
            print_token_list(data, as_json=args.json_output)

        elif args.command == "usage":
            # 日期格式兼容：如果只传了 YYYY-MM-DD，自动补全为 ISO 格式
            def to_iso(date_str: str, is_end: bool = False) -> str:
                if "T" not in date_str:
                    suffix = "T23:59:59+08:00" if is_end else "T00:00:00+08:00"
                    return date_str + suffix
                return date_str

            # 默认值：start=30天前，end=今天
            from datetime import datetime, timedelta
            today = datetime.now()
            default_start = (today - timedelta(days=30)).strftime("%Y-%m-%d")
            default_end = today.strftime("%Y-%m-%d")

            start_iso = to_iso(args.start or default_start, is_end=False)
            end_iso   = to_iso(args.end or default_end, is_end=True)
            print(f"🔍 查询 AIGC 用量统计 | 类型: {args.aigc_type} | {start_iso} ~ {end_iso}", file=_out)
            data = describe_aigc_usage(
                client,
                start_time=start_iso,
                end_time=end_iso,
                aigc_type=args.aigc_type,
                sub_app_id=sub_app_id,
            )
            print_usage_data(data, aigc_type=args.aigc_type, as_json=args.json_output)

    except TencentCloudSDKException as e:
        print(f"❌ API 调用失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
