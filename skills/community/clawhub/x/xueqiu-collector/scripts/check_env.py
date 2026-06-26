"""
雪球采集 Skill 环境检测脚本（双路径版）
=====================================
同时检测系统路径和 WorkBuddy 用户路径，完整展示所有可用依赖。

使用方式：
  py scripts/check_env.py          # 完整检测
  py scripts/check_env.py --fix    # 检测 + 自动修复（pip 安装可选依赖）
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

# 强制 UTF-8 输出（解决 Windows GBK 编码问题）
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


# ════════════════════════════════════════
#  颜色输出（Windows 兼容）
# ════════════════════════════════════════

def _c(code, text):
    """带颜色的终端输出"""
    return f"\033[{code}m{text}\033[0m"

OK = lambda t: _c("32", f"✅ {t}")       # 绿色
WARN = lambda t: _c("33", f"⚠️  {t}")     # 黄色
FAIL = lambda t: _c("31", f"❌ {t}")       # 红色
INFO = lambda t: _c("36", f"ℹ️  {t}")      # 青色
DIM = lambda t: _c("2", t)                 # 灰色
HEAD = lambda t: _c("1;4", f"\n{'─'*50}\n{t}\n{'─'*50}")


# ════════════════════════════════════════
#  路径候选定义
# ════════════════════════════════════════

def get_npx_candidates():
    """npx 候选路径：全面扫描系统上所有 npx 安装"""
    seen = set()
    results = []

    # ① WorkBuddy 固定路径（Skill/工具链安装位置，最高优先级）
    wb_npx = r"C:\Users\123\nodejs\npx.cmd"
    if os.path.isfile(wb_npx):
        results.append(("WorkBuddy 工具链", wb_npx))
        seen.add(os.path.normpath(wb_npx).lower())

    # ② 用户目录 npm 全局安装
    local_npm = os.path.join(
        os.environ.get('LOCALAPPDATA', ''), 'nodejs', 'npx.cmd')
    if os.path.isfile(local_npm) and os.path.normpath(local_npm).lower() not in seen:
        results.append(("用户全局 (LOCALAPPDATA)", local_npm))
        seen.add(os.path.normpath(local_npm).lower())

    # ③ 系统 PATH（shutil.which）
    sys_which = shutil.which("npx")
    if sys_which and os.path.normpath(sys_which).lower() not in seen:
        results.append(("系统 PATH (shutil.which)", sys_which))
        seen.add(os.path.normpath(sys_which).lower())

    # ④ 原始 PATH 查找
    raw_which = shutil.which("npx", path=os.environ.get('PATH', ''))
    if raw_which and raw_which != sys_which and os.path.normpath(raw_which).lower() not in seen:
        results.append(("系统 (原始 PATH)", raw_which))
        seen.add(os.path.normpath(raw_which).lower())

    # ⑤ Program Files（系统安装的 Node.js）
    pf_npx = os.path.join(
        os.environ.get('APPDATA', ''), '..', 'nodejs', 'npx.cmd')
    pf_npx2 = r"C:\Program Files\nodejs\npx.CMD"
    for label, p in [("系统 (AppData..)", pf_npx), ("系统 (Program Files)", pf_npx2)]:
        if os.path.isfile(p) and os.path.normpath(p).lower() not in seen:
            results.append((label, p))
            seen.add(os.path.normpath(p).lower())

    # ⑥ 用户 Profile 目录下的 nodejs
    user_profile = os.environ.get('USERPROFILE', '')
    if user_profile:
        up_npx = os.path.join(user_profile, 'nodejs', 'npx.cmd')
        if os.path.isfile(up_npx) and os.path.normpath(up_npx).lower() not in seen:
            username = os.path.basename(user_profile)
            results.append((f"用户 ({username}\\nodejs)", up_npx))

    return results


def get_edge_profile_candidates():
    """Edge Profile 候选路径"""
    default_profile = Path(os.environ.get('LOCALAPPDATA', '')) / "Microsoft/Edge/User Data/Default"
    alt_profile = Path(rf"C:\Users\{os.environ.get('USERNAME', '123')}\AppData\Local\Microsoft\Edge\User Data\Default")
    return [
        ("默认 (LOCALAPPDATA)", default_profile),
        ("备用 (硬编码)", alt_profile),
    ]


def get_edge_browser_candidates():
    """Edge 浏览器候选路径"""
    return [
        ("x86 Program Files",
         Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")),
        ("x64 Program Files",
         Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe")),
    ]


# ════════════════════════════════════════
#  单路径检测工具函数
# ════════════════════════════════════════

def probe_npx(npx_path, label=""):
    """探测单个 npx 是否可用，返回 (ok, version_or_error)"""
    if not npx_path or not os.path.isfile(npx_path):
        return False, "文件不存在"
    try:
        result = subprocess.run(
            [npx_path, '--version'],
            capture_output=True, text=True, timeout=5
        )
        ver = (result.stdout or result.stderr).strip()
        if result.returncode == 0 and ver:
            return True, ver
        return False, ver[:60] if ver else "无输出"
    except Exception as e:
        return False, str(e)[:40]


def probe_playwright_cli(npx_path, label=""):
    """用指定 npx 探测 playwright-cli"""
    if not npx_path or not os.path.isfile(npx_path):
        return False, "npx 不可用"
    try:
        result = subprocess.run(
            [npx_path, "playwright-cli", "--version"],
            capture_output=True, text=True, timeout=15
        )
        out = (result.stdout or result.stderr).strip()
        if result.returncode == 0 and out:
            ver = out.split('\n')[0].strip()
            return True, ver
        return False, out[:80] if out else "无输出"
    except subprocess.TimeoutExpired:
        return False, "超时(15s)"
    except Exception as e:
        return False, str(e)[:40]


def probe_tesseract():
    """探测 tesseract CLI"""
    tess = shutil.which("tesseract")
    if not tess:
        return False, None, "未找到"
    try:
        r = subprocess.run(
            ["tesseract", "--version"],
            capture_output=True, text=True, timeout=5
        )
        if r.returncode == 0:
            line1 = r.stdout.strip().split('\n')[0] if r.stdout.strip() else ""
            return True, tess, line1
        return False, tess, r.stderr[:60] if r.stderr else "异常退出码"
    except Exception as e:
        return False, tess, str(e)[:40]


# ════════════════════════════════════════
#  双路径检测函数（核心）
# ════════════════════════════════════════

def check_python_version():
    """Python 版本 >= 3.10"""
    v = sys.version_info
    ok = v.major == 3 and v.minor >= 10
    label = OK(f"Python {v.major}.{v.minor}.{v.micro}") if ok else \
             FAIL(f"Python {v.major}.{v.minor}.{v.micro}（需要 >= 3.10）")
    print(label)
    fix = None if ok else "请升级 Python：https://www.python.org/downloads/"
    return ok, fix


def check_npx_multi():
    """npx — 多路径全检"""
    candidates = get_npx_candidates()
    any_ok = False
    best_path = None
    best_ver = ""

    for i, (label, path) in enumerate(candidates):
        if not path:
            continue
        ok, info = probe_npx(path)
        indent = "   "
        if ok:
            any_ok = True
            best_path = path
            best_ver = info
            marker = OK(f"[✓] {label}")
        else:
            marker = FAIL(f"[✗] {label}")
        print(f"{indent}{marker}")
        print(f"{indent}{DIM(f'     路径: {path}')}")
        print(f"{indent}{DIM(f'     结果: {info}')}")
        print()

    if any_ok:
        print(OK(f">>> 使用: npx ({best_ver})"))
        return True, None, best_path
    else:
        print(FAIL(">>> 所有路径均不可用"))
        return False, "安装 Node.js: https://nodejs.org/", None


def check_edge_profile_multi():
    """Edge Profile — 多路径全检"""
    candidates = get_edge_profile_candidates()
    for label, p in candidates:
        if p.is_dir() and (p / "Preferences").exists():
            print(OK(f"Edge Profile ({label})"))
            print(f"   {DIM(str(p))}")
            return True, None, str(p)

    print(WARN("Edge Profile 目录未找到"))
    for label, p in candidates:
        print(f"   {DIM(f'[{label}] {p}')} → 不存在")
    return False, "确认 Edge 已安装，或用 --edge-profile 参数指定", None


def check_edge_browser_multi():
    """Edge 浏览器 — 多路径全检"""
    candidates = get_edge_browser_candidates()
    for label, p in candidates:
        if p.exists():
            print(OK(f"Edge 浏览器 ({label})"))
            print(f"   {DIM(str(p))}")
            return True, None

    print(FAIL("Edge 浏览器未找到"))
    for label, p in candidates:
        print(f"   {DIM(f'[{label}] {p}')} → 不存在")
    return False, "请安装 Microsoft Edge: https://www.microsoft.com/edge"


def check_playwright_cli_multi(npx_paths_dict):
    """playwright-cli — 用多个 npx 全检"""
    # npx_paths_dict: {label: path} 来自 check_npx_multi 的结果
    any_ok = False

    # 收集所有有效的 npx 路径
    all_npx = []
    for label, path in get_npx_candidates():
        if path and os.path.isfile(path):
            all_npx.append((label, path))

    if not all_npx:
        print(FAIL("跳过：无可用的 npx"))
        return False, None

    for label, np in all_npx:
        ok, info = probe_playwright_cli(np, label)
        if ok:
            any_ok = True
            print(OK(f"  [{label}] playwright-cli ({info})"))
        else:
            print(FAIL(f"  [{label}] 失败 ({info})"))

    if any_ok:
        return True, None
    else:
        print("\n  >>> 所有 npx 路径均无法运行 playwright-cli")
        first_np = all_npx[0][1]
        cmd = f'{first_np} playwright --install msedge  &&  {first_np} playwright-cli'
        return False, f"安装命令:\n  {cmd}"


def check_winocr():
    """winocr（可选）"""
    try:
        import winocr
        print(OK("winocr（Windows 原生 OCR 引擎）"))
        return True, None
    except ImportError:
        pass
    print(WARN("winocr 未安装（OCR 将降级到 tesseract 或跳过）"))
    return False, "pip install winocr"


def check_pillow():
    """Pillow（可选）"""
    try:
        from PIL import Image
        print(OK(f"Pillow ({Image.__version__})"))
        return True, None
    except ImportError:
        pass
    print(WARN("Pillow 未安装（winocr 需要）"))
    return False, "pip install Pillow"


def check_tesseract_multi():
    """tesseract — 多路径"""
    ok, path, info = probe_tesseract()
    if ok:
        print(OK(f"tesseract ({info})"))
        print(f"   {DIM(str(path))}")
        return True, None
    print(WARN(f"tesseract 未找到（{info}）"))
    return False, (
        "Windows: choco install tesseract\n"
        "         或下载: https://github.com/UB-Mannheim/tesseract/wiki\n"
        "Linux:   sudo apt install tesseract-ocr tesseract-ocr-chi-sim"
    )


# ════════════════════════════════════════
#  主流程
# ════════════════════════════════════════

def main():
    auto_fix = "--fix" in sys.argv

    print(_c("1;36", "\n╔══════════════════════════════════════════╗"))
    print(_c("1;36", "║   🧊 雪球采集 Skill 环境检测（双路径版）  ║"))
    print(_c("1;36", "╚══════════════════════════════════════════╝"))

    results = []  # (name, passed, is_required, fix_cmd)

    # ── 必须依赖 ──
    print(HEAD("1. 必须依赖"))

    print("\n【Python】")
    ok, fix = check_python_version()
    results.append(("Python >= 3.10", ok, True, fix))

    print("\n【npx (Node.js)】— 扫描所有路径:")
    ok, fix, npx_path = check_npx_multi()
    results.append(("npx", ok, True, fix))

    print("\n【Edge Profile】")
    ok, fix, edge_profile = check_edge_profile_multi()
    results.append(("Edge Profile", ok, True, fix))

    print("\n【Edge 浏览器】")
    ok, fix = check_edge_browser_multi()
    results.append(("Edge 浏览器", ok, True, fix))

    print("\n【playwright-cli】— 用各 npx 分别测试:")
    ok, fix = check_playwright_cli_multi({})
    results.append(("playwright-cli", ok, True, fix))

    # ── 可选依赖 ──
    print(HEAD("2. 可选依赖（增强功能）"))

    print("\n【winocr】")
    ok_w, fix_w = check_winocr()
    results.append(("winocr (OCR)", ok_w, False, fix_w))

    print("\n【Pillow】")
    ok_p, fix_p = check_pillow()
    results.append(("Pillow (PIL)", ok_p, False, fix_p))

    print("\n【tesseract】")
    ok_t, fix_t = check_tesseract_multi()
    results.append(("tesseract (OCR)", ok_t, False, fix_t))

    # ═══ 汇总 ═══
    print(HEAD("检测结果汇总"))

    required = [r for r in results if r[2]]
    optional = [r for r in results if not r[2]]
    req_pass = sum(1 for r in required if r[1])
    opt_pass = sum(1 for r in optional if r[1])

    print(f"\n  必须依赖: {_c('32', str(req_pass))}/{len(required)} 通过")
    print(f"  可选依赖: {_c('32', str(opt_pass))}/{len(optional)} 通过")

    if req_pass == len(required):
        print(_c("32", "\n🎉 环境就绪！可以直接运行采集：\n"))
        print(f'  py scripts/collect.py --author "昵称" --url "https://xueqiu.com/u/XXXXXX"')
        if edge_profile:
            print(f'  py scripts/collect.py --author "昵称" --url "URL" --edge-profile "{edge_profile}"')
    else:
        print(FAIL("\n❌ 必须依赖未满足，无法运行采集！\n"))

    missing_req = [(n, f) for n, ok, _, f in results if not ok and (n, _, True, _) in [(r[0], r[1], r[2], r[3]) for r in required]]
    missing_opt = [(n, f) for n, ok, _, f in results if not ok and (n, _, False, _) in [(r[0], r[1], r[2], r[3]) for r in optional]]

    if missing_req:
        print(FAIL("【必须修复】以下依赖缺失："))
        for name, fix in missing_req:
            print(f"\n  🔸 {name}\n     {fix}")

    if missing_opt:
        print(WARN("\n【建议安装】以下功能将被降级或跳过："))
        for name, fix in missing_opt:
            print(f"\n  🔸 {name}\n     {fix}")

    # ── 自动修复 ──
    if auto_fix:
        pip_fixable = []
        if not ok_w:
            pip_fixable.append("winocr")
        if not ok_p:
            pip_fixable.append("Pillow")

        if pip_fixable:
            print(INFO("\n--fix 模式：自动安装 pip 包..."))
            for pkg in pip_fixable:
                print(f"\n  正在安装 {pkg} ...")
                try:
                    r = subprocess.run(
                        [sys.executable, "-m", "pip", "install", pkg],
                        capture_output=True, text=True, timeout=120
                    )
                    if r.returncode == 0:
                        print(OK(f"  {pkg} 安装成功 ✅"))
                    else:
                        err = (r.stderr or r.stdout)[-200:]
                        print(FAIL(f"  {pkg} 安装失败: {err}"))
                except Exception as e:
                    print(FAIL(f"  安装异常: {e}"))

    sys.exit(0 if req_pass == len(required) else 1)


if __name__ == "__main__":
    main()
