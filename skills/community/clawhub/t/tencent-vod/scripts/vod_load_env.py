#!/usr/bin/env python3
"""
vod_load_env.py — 腾讯云 VOD Skill 环境变量自动加载工具

实现说明：
  使用 python-dotenv 库的 load_dotenv 函数加载 dotenv 风格的配置文件。
  按以下顺序加载（已存在的环境变量不会被覆盖，先加载者优先）：
    1. 默认行为：通过 find_dotenv(usecwd=True) 从当前目录向上递归找最近的 .env 并加载
    2. ~/.env                （用户级 dotenv，最高优先级）
    3. ./.env                （当前工作目录 dotenv）

  目标变量：
    TENCENTCLOUD_SECRET_ID       （必须）
    TENCENTCLOUD_SECRET_KEY      （必须）
    TENCENTCLOUD_VOD_AIGC_TOKEN  （可选，AIGC LLM Chat 专用）
    TENCENTCLOUD_VOD_SUB_APP_ID  （可选，子应用 ID）

用法（在其他脚本中调用）：
    from vod_load_env import ensure_env_loaded
    ensure_env_loaded()
"""

import os
import sys

try:
    from dotenv import load_dotenv
    _DOTENV_AVAILABLE = True
except ImportError:
    _DOTENV_AVAILABLE = False

# 需要检测的目标变量
_TARGET_VARS = {
    "TENCENTCLOUD_SECRET_ID",
    "TENCENTCLOUD_SECRET_KEY",
    "TENCENTCLOUD_VOD_AIGC_TOKEN",
    "TENCENTCLOUD_VOD_SUB_APP_ID",
}

# 必须的变量（缺少时报错）
_REQUIRED_VARS = [
    "TENCENTCLOUD_SECRET_ID",
    "TENCENTCLOUD_SECRET_KEY",
]

# 可选的变量（仅在特定场景下需要）
_OPTIONAL_VARS = {
    "TENCENTCLOUD_VOD_AIGC_TOKEN": "AIGC LLM Chat（vod_aigc_chat.py）专用",
    "TENCENTCLOUD_VOD_SUB_APP_ID": "子应用操作时使用（可通过 --sub-app-id 参数覆盖）",
}

# 候选 dotenv 文件列表（按加载顺序，先加载者优先；load_dotenv 默认 override=False）
# 此外，load_env_files() 会先调用一次无参 load_dotenv()，
# 借助 find_dotenv(usecwd=True) 从当前工作目录向上递归查找最近的 .env 文件并加载。
_ENV_FILES = [
    os.path.expanduser("~/.env"),
    os.path.join(os.getcwd(), ".env"),
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

    # 先尝试 load_dotenv 的默认行为：从当前工作目录向上递归查找 .env 文件
    # 这一步覆盖了"用户在项目根目录放 .env，但脚本从子目录运行"等常见场景
    before_default = dict(os.environ)
    try:
        from dotenv import find_dotenv
        default_path = find_dotenv(usecwd=True)
    except (ImportError, Exception):
        default_path = ""

    if default_path and os.path.isfile(default_path):
        try:
            ok = load_dotenv(override=False)
            seen_paths.add(os.path.abspath(default_path))
            if verbose:
                print(
                    f"[load_env] 加载默认 .env: {default_path} "
                    f"({'成功' if ok else '无变化'})",
                    file=sys.stderr,
                )
            for key, value in os.environ.items():
                if key not in before_default:
                    newly_loaded[key] = value
                    if verbose:
                        display = value[:4] + "****" if len(value) > 4 else "****"
                        print(f"[load_env]   设置 {key}={display}", file=sys.stderr)
        except (OSError, IOError) as e:
            if verbose:
                print(f"[load_env] 读取默认 .env 失败: {e}", file=sys.stderr)
    else:
        if verbose:
            print(
                "[load_env] 未在当前目录或上级目录找到默认 .env",
                file=sys.stderr,
            )

    for filepath in _ENV_FILES:
        if not filepath:
            continue
        abs_path = os.path.abspath(filepath)
        if abs_path in seen_paths:
            if verbose:
                print(
                    f"[load_env] 跳过（已在默认查找中加载）: {filepath}",
                    file=sys.stderr,
                )
            continue
        seen_paths.add(abs_path)

        if not os.path.isfile(filepath):
            if verbose:
                print(f"[load_env] 跳过（不存在）: {filepath}", file=sys.stderr)
            continue

        # 记录加载前的快照，用于推断本次新加载了哪些 KEY
        before = dict(os.environ)

        try:
            ok = load_dotenv(dotenv_path=filepath, override=False)
        except (OSError, IOError) as e:
            if verbose:
                print(f"[load_env] 读取失败: {filepath} ({e})", file=sys.stderr)
            continue

        if verbose:
            print(
                f"[load_env] 加载文件: {filepath} ({'成功' if ok else '无变化'})",
                file=sys.stderr,
            )

        # 收集本次新加载的变量
        for key, value in os.environ.items():
            if key not in before:
                newly_loaded[key] = value
                if verbose:
                    display = value[:4] + "****" if len(value) > 4 else "****"
                    print(f"[load_env]   设置 {key}={display}", file=sys.stderr)

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
║                    腾讯云VOD环境变量未配置                          ║
╚══════════════════════════════════════════════════════════════════╝

以下环境变量缺失：
{missing_str}

密钥可以在腾讯云控制台获取：https://console.cloud.tencent.com/cam/capi
VOD 控制台：https://console.cloud.tencent.com/vod

【配置方式 1】写入 dotenv 文件（推荐，自动加载，无需 source）：
  脚本启动时会按顺序加载以下文件中的变量到当前进程：
{env_files_str}

  示例（以 ~/.env 为例）：
    TENCENTCLOUD_SECRET_ID=<您的 SecretId>
    TENCENTCLOUD_SECRET_KEY=<您的 SecretKey>
    # 可选
    TENCENTCLOUD_VOD_AIGC_TOKEN=<您的 AIGC Token>
    TENCENTCLOUD_VOD_SUB_APP_ID=<您的子应用 ID>

⚠️  安全提示：请通过安全渠道配置密钥，避免提交到代码仓库。

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
      required  — 必须存在的变量列表，默认检查 SECRET_ID / SECRET_KEY
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


# ─── 独立运行时：诊断模式 ───────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="加载 dotenv 文件并检查腾讯云 VOD 所需环境变量（诊断模式）"
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
        print("=== 腾讯云 VOD 环境变量状态 ===\n")
        print("【必须变量】")
        all_required_ok = True  # NOCA:invalid-name(naming follows SDK convention)
        for var in _REQUIRED_VARS:
            val = os.environ.get(var, "")
            status = _format_var_status(var, val)
            if not val:
                all_required_ok = False  # NOCA:invalid-name(naming follows SDK convention)
            print(f"  {var}: {status}")

        print("\n【可选变量】")
        for var, desc in _OPTIONAL_VARS.items():
            val = os.environ.get(var, "")
            if val:
                display = val[:4] + "****" if len(val) > 4 else "****"
                status = f"✅ 已设置 ({display})"
            else:
                status = f"⚪ 未设置（{desc}）"
            print(f"  {var}: {status}")

        print()
        if all_required_ok:
            print("✅ 必须变量全部已配置，可以正常使用 VOD Skill。")
            sys.exit(0)
        else:
            print("❌ 必须变量未完整配置，请按提示配置后重试。")
            sys.exit(1)

    if args.dry_run:
        print("=== 模拟执行（Dry-run）===\n")
        print("操作：使用 load_dotenv 加载腾讯云 VOD 环境变量")
        print(f"\npython-dotenv 状态: {'✅ 可用' if _DOTENV_AVAILABLE else '❌ 未安装'}")
        print("\n将要按顺序加载的 dotenv 文件：")
        for filepath in _ENV_FILES:
            exists = "✅ 存在" if os.path.isfile(filepath) else "⚪ 不存在"
            print(f"  - {filepath}  [{exists}]")

        print("\n将要查找的环境变量：")
        for var in _REQUIRED_VARS:
            val = os.environ.get(var, "")
            tag = "[必须]"
            print(f"  - {var}: {_format_var_status(var, val)}  {tag}")
        for var in _OPTIONAL_VARS:
            val = os.environ.get(var, "")
            tag = "[可选]"
            if val:
                display = val[:4] + "****" if len(val) > 4 else "****"
                print(f"  - {var}: ✅ 已设置 ({display})  {tag}")
            else:
                print(f"  - {var}: ⚪ 未设置  {tag}")

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
    print("【必须变量】")
    all_required_ok = True  # NOCA:invalid-name(naming follows SDK convention)
    for var in _REQUIRED_VARS:
        val = os.environ.get(var, "")
        status = _format_var_status(var, val)
        if not val:
            all_required_ok = False  # NOCA:invalid-name(naming follows SDK convention)
        print(f"  {var}: {status}")

    print("【可选变量】")
    for var, desc in _OPTIONAL_VARS.items():
        val = os.environ.get(var, "")
        if val:
            display = val[:4] + "****" if len(val) > 4 else "****"
            status = f"✅ 已设置 ({display})"
        else:
            status = f"⚪ 未设置（{desc}）"
        print(f"  {var}: {status}")

    if newly:
        target_hits = [k for k in newly if k in _TARGET_VARS]
        print(f"\n本次新加载了 {len(newly)} 个变量"
              f"（其中目标变量 {len(target_hits)} 个: {target_hits}）")
    else:
        print("\n未加载任何新变量（已全部设置或文件不存在）")

    if not all_required_ok:
        _print_setup_hint([v for v in _REQUIRED_VARS if not os.environ.get(v)])
        sys.exit(1)
    else:
        print("\n✅ 必须变量全部已配置，可以正常使用 VOD Skill。")
