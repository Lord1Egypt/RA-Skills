#!/usr/bin/env python3
"""
mps_load_env.py — 腾讯云 MPS Skill 环境变量自动加载工具

实现说明：
  使用 python-dotenv 库的 load_dotenv 函数加载 dotenv 风格的配置文件。
  按以下顺序加载（已存在的环境变量不会被覆盖，先加载者优先）：
    1. 默认行为：通过 find_dotenv(usecwd=True) 从当前目录向上递归找最近的 .env 并加载
    2. ~/.env                （用户级 dotenv）
    3. ~/.bashrc             （shell 启动文件，兼容 export VAR=... 写法）
    4. ~/.profile            （登录 shell 启动文件）
    5. <SKILL_DIR>/.env      （脚本所在 skill 目录的 dotenv）

  目标变量（全部为必需）：
    TENCENTCLOUD_SECRET_ID       （必需）
    TENCENTCLOUD_SECRET_KEY      （必需）
    TENCENTCLOUD_COS_BUCKET      （必需，输入/输出 COS 桶）
    TENCENTCLOUD_COS_REGION      （必需，COS 桶所在地域）
    TENCENTCLOUD_API_REGION      （必需，MPS API 调用地域）

  可选变量：
    TENCENTCLOUD_MPS_ENDPOINT    （可选，MPS API 接入点；默认 mps.tencentcloudapi.com，
                                  国际站设为 mps.intl.tencentcloudapi.com）

用法（在其他脚本中调用）：
    from mps_load_env import ensure_env_loaded
    ensure_env_loaded()

诊断模式（独立运行）：
    python mps_load_env.py                   # 实际加载并打印结果
    python mps_load_env.py --check-only      # 仅检查当前进程环境变量状态
    python mps_load_env.py --dry-run         # 模拟执行（不实际加载）
    python mps_load_env.py --verbose         # 显示详细加载日志
"""

import os
import sys

try:
    from dotenv import load_dotenv
    _DOTENV_AVAILABLE = True
except ImportError:
    _DOTENV_AVAILABLE = False

# 必需的变量（缺少时报错）
_REQUIRED_VARS = [
    "TENCENTCLOUD_SECRET_ID",
    "TENCENTCLOUD_SECRET_KEY",
    "TENCENTCLOUD_COS_BUCKET",
    "TENCENTCLOUD_COS_REGION",
    "TENCENTCLOUD_API_REGION",
]

# 可选变量（未设置时使用默认值，不报错）
_OPTIONAL_VARS = [
    "TENCENTCLOUD_MPS_ENDPOINT",
]

# 候选 dotenv 文件列表（按加载顺序，先加载者优先；load_dotenv 默认 override=False）
# 此外，load_env_files() 会先调用一次无参 load_dotenv()，
# 借助 find_dotenv(usecwd=True) 从当前工作目录向上递归查找最近的 .env 文件并加载。
_ENV_FILES = [
    os.path.expanduser("~/.env"),
    os.path.expanduser("~/.bashrc"),
    os.path.expanduser("~/.profile"),
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
]

def load_env_files(verbose: bool = False) -> dict:
    """
    使用 load_dotenv 依次加载候选文件中的环境变量到 os.environ。
    已存在的环境变量不会被覆盖（override=False）。

    返回：本次新加载的变量字典 {key: value}（含目标变量与文件中其它变量）
    """
    if not _DOTENV_AVAILABLE:
        if verbose:
            print(
                "[load_env] python-dotenv 未安装，无法加载 .env 文件。"
                "请运行: pip install -r scripts/requirements.txt",
                file=sys.stderr,
            )
        return {}

    newly_loaded = {}
    seen_paths = set()

    def _load_and_collect(path_label, dotenv_path=None):
        """加载一个 dotenv 文件并收集新增变量。"""
        before = dict(os.environ)
        try:
            ok = load_dotenv(dotenv_path=dotenv_path, override=False) if dotenv_path else load_dotenv(override=False)
        except (OSError, IOError) as e:
            if verbose:
                print(f"[load_env] 读取失败: {path_label} ({e})", file=sys.stderr)
            return
        if verbose:
            print(f"[load_env] 加载文件: {path_label} ({'成功' if ok else '无变化'})", file=sys.stderr)
        for key, value in os.environ.items():
            if key not in before:
                newly_loaded[key] = value
                if verbose:
                    display = value[:4] + "****" if len(value) > 4 else "****"
                    print(f"[load_env]   设置 {key}={display}", file=sys.stderr)

    # 先尝试 find_dotenv 的默认行为：从当前工作目录向上递归查找 .env 文件
    try:
        from dotenv import find_dotenv
        default_path = find_dotenv(usecwd=True)
    except (ImportError, Exception):
        default_path = ""

    if default_path and os.path.isfile(default_path):
        _load_and_collect(f"默认 .env: {default_path}")
        seen_paths.add(os.path.abspath(default_path))
    elif verbose:
        print("[load_env] 未在当前目录或上级目录找到默认 .env", file=sys.stderr)

    for filepath in _ENV_FILES:
        if not filepath:
            continue
        abs_path = os.path.abspath(filepath)
        if abs_path in seen_paths:
            if verbose:
                print(f"[load_env] 跳过（已加载）: {filepath}", file=sys.stderr)
            continue
        seen_paths.add(abs_path)

        if not os.path.isfile(filepath):
            if verbose:
                print(f"[load_env] 跳过（不存在）: {filepath}", file=sys.stderr)
            continue

        _load_and_collect(filepath, dotenv_path=filepath)

    return newly_loaded


def check_required_vars(required: list = None) -> list:
    """
    检查必需的环境变量是否已设置。
    返回缺失的变量名列表（空列表表示全部已设置）。
    """
    if required is None:
        required = _REQUIRED_VARS
    return [k for k in required if not os.environ.get(k)]


def _print_setup_hint(missing_vars: list) -> None:
    """当环境变量加载失败时，向用户打印详细的配置引导提示。"""
    env_files_str = "\n".join(f"    • {f}" for f in _ENV_FILES)
    missing_str = "\n".join(f"    {k}=<your_value>" for k in missing_vars)
    hint = f"""
╔══════════════════════════════════════════════════════════════════╗
║              腾讯云 MPS 环境变量未配置                           ║
╚══════════════════════════════════════════════════════════════════╝

以下环境变量缺失：
{missing_str}

开通 MPS 服务：https://console.cloud.tencent.com/mps
密钥获取：     https://console.cloud.tencent.com/cam/capi
COS 桶管理：   https://console.cloud.tencent.com/mps/workflows/buckets

【配置方式 1】写入 dotenv 文件（推荐，自动加载，无需 source）：
  脚本启动时会按顺序加载以下文件中的变量到当前进程：
{env_files_str}
  此外，find_dotenv(usecwd=True) 会从当前目录向上递归查找最近的 .env 文件。

  示例（以 ~/.env 为例）：
    TENCENTCLOUD_SECRET_ID=<您的 SecretId>
    TENCENTCLOUD_SECRET_KEY=<您的 SecretKey>
    TENCENTCLOUD_COS_BUCKET=<您的 Bucket 名称>
    TENCENTCLOUD_COS_REGION=<Bucket 所在地域，如 ap-guangzhou>
    TENCENTCLOUD_API_REGION=<MPS API 调用地域，如 ap-guangzhou>

【配置方式 2】传统 shell 环境变量（需要重新启动 shell 或 source）：
    export TENCENTCLOUD_SECRET_ID=<您的 SecretId>
    export TENCENTCLOUD_SECRET_KEY=<您的 SecretKey>

⚠️  安全提示：请通过安全渠道配置密钥，避免提交到代码仓库。
   如需安装 python-dotenv：pip install -r scripts/requirements.txt

配置完成后，请重新发起对话即可。
"""
    print(hint, file=sys.stderr)


def ensure_env_loaded(
    required: list = None,
    verbose: bool = False,
) -> bool:
    """
    确保必需的环境变量已加载。

    执行流程：
      1. 检查必需变量是否已在 os.environ 中
      2. 如果有缺失，调用 load_dotenv 加载候选文件
      3. 再次检查，返回是否全部就绪
    参数：
      required  — 必须存在的变量列表，默认 _REQUIRED_VARS（5 项：SECRET_ID/KEY + COS_BUCKET/REGION + API_REGION）
      verbose   — 是否打印加载日志到 stderr

    返回：True 表示所有必需变量均已就绪，False 表示仍有缺失
    """
    if required is None:
        required = _REQUIRED_VARS

    missing_before = check_required_vars(required)
    if not missing_before:
        return True

    if verbose:
        print(
            f"[load_env] 检测到缺失变量: {missing_before}，开始加载 dotenv 文件...",
            file=sys.stderr,
        )

    load_env_files(verbose=verbose)

    missing_after = check_required_vars(required)
    if missing_after:
        return False

    if verbose:
        print("[load_env] 所有必需变量已加载完成。", file=sys.stderr)
    return True


def _format_var_status(var: str, val: str) -> str:
    """格式化单个变量的展示状态。"""
    if val:
        display = val[:4] + "****" if len(val) > 4 else "****"
        return f"✅ 已设置 ({display})"
    return "❌ 未设置"


def _format_optional_var_status(var: str, val: str) -> str:
    """格式化可选变量的展示状态（非敏感，明文展示，未设置时提示默认行为）。"""
    if val:
        return f"✅ 已设置 ({val})"
    if var == "TENCENTCLOUD_MPS_ENDPOINT":
        return "⚪ 未设置（默认国内站 mps.tencentcloudapi.com）"
    return "⚪ 未设置（使用默认值）"


# ─── 独立运行时：诊断模式 ───────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="加载 dotenv 文件并检查腾讯云 MPS 所需环境变量（诊断模式）"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="显示详细加载日志"
    )
    parser.add_argument(
        "--check-only", action="store_true", help="仅检查当前环境变量状态，不加载"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="模拟执行，显示将要执行的操作但不实际加载"
    )
    args = parser.parse_args()

    if args.check_only:
        print("=== 腾讯云 MPS 环境变量状态 ===\n")
        print("【必需变量】")
        all_ok = True
        for var in _REQUIRED_VARS:
            val = os.environ.get(var, "")
            status = _format_var_status(var, val)
            if not val:
                all_ok = False
            print(f"  {var}: {status}")

        print()
        print("【可选变量】")
        for var in _OPTIONAL_VARS:
            val = os.environ.get(var, "")
            print(f"  {var}: {_format_optional_var_status(var, val)}")

        print()
        if all_ok:
            print("✅ 必需变量全部已配置，可以正常使用 MPS Skill。")
            sys.exit(0)
        else:
            print("❌ 必需变量未完整配置，请按提示配置后重试。")
            sys.exit(1)

    if args.dry_run:
        print("=== 模拟执行（Dry-run）===\n")
        print("操作：使用 load_dotenv 加载腾讯云 MPS 环境变量")
        print(f"\npython-dotenv 状态: {'✅ 可用' if _DOTENV_AVAILABLE else '❌ 未安装'}")
        print("\n将要按顺序加载的 dotenv 文件：")
        print("  - 0) find_dotenv(usecwd=True) 自动从当前目录向上递归查找最近的 .env")
        for filepath in _ENV_FILES:
            exists = "✅ 存在" if os.path.isfile(filepath) else "⚪ 不存在"
            print(f"  - {filepath}  [{exists}]")

        print("\n将要查找的环境变量：")
        for var in _REQUIRED_VARS:
            val = os.environ.get(var, "")
            print(f"  - {var}: {_format_var_status(var, val)}  [必需]")
        for var in _OPTIONAL_VARS:
            val = os.environ.get(var, "")
            print(f"  - {var}: {_format_optional_var_status(var, val)}  [可选]")

        print("\n不会实际加载环境变量。移除 --dry-run 参数后执行实际操作。")
        sys.exit(0)

    print("=== 加载 dotenv 文件 ===", flush=True)
    if not _DOTENV_AVAILABLE:
        print(
            "❌ python-dotenv 未安装。请运行: pip install -r scripts/requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    newly = load_env_files(verbose=True)
    sys.stderr.flush()

    print("\n=== 加载结果 ===")
    print("【必需变量】")
    all_ok = True
    for var in _REQUIRED_VARS:
        val = os.environ.get(var, "")
        status = _format_var_status(var, val)
        if not val:
            all_ok = False
        print(f"  {var}: {status}")

    print()
    print("【可选变量】")
    for var in _OPTIONAL_VARS:
        val = os.environ.get(var, "")
        print(f"  {var}: {_format_optional_var_status(var, val)}")

    if newly:
        target_hits = [k for k in newly if k in set(_REQUIRED_VARS)]
        print(f"\n本次新加载了 {len(newly)} 个变量"
              f"（其中目标变量 {len(target_hits)} 个: {target_hits}）")
    else:
        print("\n未加载任何新变量（已全部设置或文件不存在）")

    if not all_ok:
        _print_setup_hint([v for v in _REQUIRED_VARS if not os.environ.get(v)])
        sys.exit(1)
    else:
        print("\n✅ 必需变量全部已配置，可以正常使用 MPS Skill。")
