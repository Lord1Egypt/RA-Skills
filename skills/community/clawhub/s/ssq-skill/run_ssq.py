#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双色球算法选号防被骗 · 跨平台统一启动器（普通用户唯一需要记住的命令）

只需 Python3（仅用标准库，无需 pip 安装任何包）。

最常用（记这一条就够了）:
  python run_ssq.py                 # 完整流水线：下载当期数据 → 预测 → 22项自检 → 报告

其它用法（进阶，普通用户一般用不到）:
  python run_ssq.py --skip-download # 离线模式：用内置数据，不联网
  python run_ssq.py --healthcheck   # 仅跑 22 项自检护栏（退出码0=全绿）
  python run_ssq.py --explore       # 跑方法发现+证伪引擎（9种选号思路样本外回测）
  python run_ssq.py --randomness    # 跑开奖序列随机性检验电池（10项卡方）
  python run_ssq.py --help          # 查看这份友好说明

重要立场：本工具产出的是娱乐性参考组合 + 诚实分析报告，不保证结果。
数学上任何选号思路都不优于随机，长期玩必亏——请量力而行、理性娱乐。

任何传给底层引擎的其它参数可用 --passthrough "..." 透传。
"""
import os
import sys
import glob
import subprocess
import json
from datetime import datetime

# 本启动器所在目录 = scripts/（顶层，仅放入口+说明）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 所有内部模块与离线数据都收在 lib/ 子目录，避免顶层文件过多
LIB_DIR = os.path.join(SCRIPT_DIR, "lib")
if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

PY = sys.executable or "python3"

# 缓存清单：记录上次为哪个目标期生成了已验证报告，同期复访直接秒出
CACHE_FILE = os.path.join(LIB_DIR, "ssq_cache_manifest.json")


def _friendly_banner(extra_args):
    """启动横幅：一句话说清要做什么，普通用户不慌。"""
    mode = "完整流水线（下载数据→预测→22项自检→报告）"
    if "--skip-download" in extra_args:
        mode = "离线模式（用内置离线数据，不联网）"
    elif "--healthcheck" in extra_args:
        mode = "系统自检（22 项护栏，退出码 0 = 全绿）"
    elif "--explore" in extra_args:
        mode = "方法发现与证伪（9 种选号思路样本外回测）"
    elif "--randomness" in extra_args:
        mode = "开奖随机性检验（10 项卡方电池）"
    print("=" * 64)
    print("双色球算法选号防被骗 · 启动")
    print("  立场：娱乐性参考组合 + 诚实分析报告，不保证结果。")
    print("  正在运行：python run_ssq.py  →  " + mode)
    print("=" * 64)


def _run(target, extra_args):
    """在 lib/ 目录内运行目标脚本，流式输出。"""
    target_path = os.path.join(LIB_DIR, target)
    cmd = [PY, target_path] + extra_args
    # 关键: 把 cwd 设到 lib/, 这样 ssq_*.py 的相对数据/脚本引用全部成立
    rc = subprocess.run(cmd, cwd=LIB_DIR).returncode
    if rc == 0:
        print("=" * 64)
        print("退出码: %d  （全部完成 ✅）" % rc)
        print("=" * 64)
    else:
        print("=" * 64)
        print("退出码: %d  （存在异常 ⚠️）" % rc)
        print("  这通常不是你操作的问题，而是网络/数据/环境的临时状况。")
        print("  本工具已尽量自动回退（如改用离线数据），报告仍会尽量生成。")
        print("  若反复出现，请查看 references/faq.md 的「运行报错」章节排查。")
        print("=" * 64)
    return rc


def _detect_real_desktop():
    """SYSTEM 排程语境下 ~ 指向 systemprofile 虚拟桌面, 报告会落到用户看不到的位置。
    动态扫描系统用户目录定位真实交互用户桌面, 不写死用户名(换机也能正确投递)。"""
    users_root = os.path.expandvars(r"%SystemDrive%\Users")
    if not os.path.isdir(users_root):
        return None
    skip = ("public", "default", "default user", "defaultuser0", "all users",
            "systemprofile", "network service", "local service")
    try:
        for name in os.listdir(users_root):
            nl = name.lower()
            if nl in skip or nl.startswith("systemprofile"):
                continue
            d = os.path.join(users_root, name, "Desktop")
            if os.path.isdir(d):
                return d
    except Exception:
        pass
    return None


def _resolve_desktop():
    """解析真实用户桌面目录(中英文系统兼容, 兜底到用户主目录)。
    SYSTEM 语境动态定位真实交互用户桌面, 不再写死本机用户名。"""
    real = _detect_real_desktop()
    for c in (real,
              os.path.expanduser("~/Desktop"),
              os.path.expanduser("~/桌面"),
              os.path.expanduser("~/Documents"),
              os.path.expanduser("~")):
        if c and os.path.isdir(c):
            return c
    return None


def _ensure_report_delivery():
    """生成报告后：保证增强版(优先)报告一定落到用户桌面 + 打印清晰绝对路径。"""
    import shutil
    pats = ("双色球*V15_增强版.html", "双色球*预测报告_V1_全面修复.html")
    cands = []
    for pat in pats:
        cands += glob.glob(os.path.join(LIB_DIR, pat))
    cands = sorted(set(cands), key=os.path.getmtime, reverse=True)
    enhanced = next((p for p in cands if "V15_增强版" in os.path.basename(p)), None)
    base = next((p for p in cands if "V15_增强版" not in os.path.basename(p)), None)

    # 增强版缺失 -> 补跑 ssq_enhance.py (幂等), 再重新定位
    if not enhanced and base:
        print("  ⚠ 未检测到增强版报告, 尝试补跑 ssq_enhance.py ...")
        try:
            subprocess.run([PY, os.path.join(LIB_DIR, "ssq_enhance.py")], cwd=LIB_DIR,
                           capture_output=True, text=True, timeout=180,
                           encoding='utf-8', errors='replace')
        except Exception as e:
            print(f"  ⚠ 补跑增强失败(非致命): {e}")
        cands = []
        for pat in pats:
            cands += glob.glob(os.path.join(LIB_DIR, pat))
        cands = sorted(set(cands), key=os.path.getmtime, reverse=True)
        enhanced = next((p for p in cands if "V15_增强版" in os.path.basename(p)), None)
        base = next((p for p in cands if "V15_增强版" not in os.path.basename(p)), None)

    if not cands:
        print("  ⚠ 未找到任何预测报告, 无法交付报告文件（请查看上方日志或 references/faq.md）")
        return

    desktop = _resolve_desktop()
    enhanced_desktop = base_desktop = None
    chosen_abs = None
    if desktop:
        for src, holder in ((enhanced, "enhanced_desktop"), (base, "base_desktop")):
            if not src:
                continue
            try:
                dest = os.path.join(desktop, os.path.basename(src))
                shutil.copy2(src, dest)
                absdest = os.path.abspath(dest)
                if holder == "enhanced_desktop":
                    enhanced_desktop = absdest
                    chosen_abs = absdest
                else:
                    base_desktop = absdest
                    if not chosen_abs:
                        chosen_abs = absdest
                try:
                    fixed = os.path.join(desktop, "双色球分析报告_最新.html")
                    shutil.copy2(src, fixed)
                except Exception:
                    pass
            except Exception as e:
                print(f"  ⚠ 复制 {os.path.basename(src)} 到桌面失败: {e}")
    else:
        print("  ⚠ 未找到桌面目录, 跳过桌面复制(报告仍在 scripts/lib/ 目录)")

    # 把最终报告绝对路径写入确定性文件（调用模型直接读它即可 present_files）
    try:
        with open(os.path.join(LIB_DIR, "REPORT_PATH.txt"), "w", encoding="utf-8") as f:
            f.write(chosen_abs or os.path.abspath(enhanced or base or ""))
    except Exception:
        pass

    print("=" * 64)
    print("REPORT_DESKTOP_PATH: " + (enhanced_desktop or base_desktop or ""))
    print("REPORT_ABS_PATH: " + os.path.abspath(enhanced or base))
    if desktop:
        print("REPORT_LATEST_PATH: " + os.path.join(desktop, "双色球分析报告_最新.html"))
    if base_desktop and base_desktop != enhanced_desktop:
        print("REPORT_BASE_DESKTOP_PATH: " + base_desktop)
    print("REPORT_PATH_FILE: " + os.path.join(LIB_DIR, "REPORT_PATH.txt"))
    print("=" * 64)


def _current_target_period():
    """计算当前目标期号(下一未开奖期)。用于缓存键: 同期内预测确定性不变。"""
    try:
        if LIB_DIR not in sys.path:
            sys.path.insert(0, LIB_DIR)
        from ssq_period import next_period as npf
        with open(os.path.join(LIB_DIR, "ssq_history.json"), "r", encoding="utf-8") as f:
            data = json.load(f)
        draws = data.get("draws", []) if isinstance(data, dict) else data
        if not draws:
            return None
        latest = draws[-1]
        return str(npf(int(latest["period"]), latest.get("date", "")))
    except Exception:
        return None


def _cache_sig():
    """报告/数据相关文件签名: 任一变化即令缓存失效, 杜绝"代码/数据修了但旧报告仍被交付"。

    命中'四、命中现实分布'空白的根因: 旧缓存只按目标期判断, 修复 ssq_power_report.json
    + ssq_auto.py 锚定后, 仍把修复前生成的旧报告(第四节空)顶在前面交付。把生成代码的
    mtime+size 与关键数据文件一起纳入签名, 任一改动即触发重算。
    """
    sig_files = [
        os.path.join(LIB_DIR, "ssq_auto.py"),
        os.path.join(LIB_DIR, "ssq_power_engine.py"),
        os.path.join(LIB_DIR, "ssq_power_report.json"),
        os.path.join(LIB_DIR, "ssq_power_baseline.json"),
        os.path.join(LIB_DIR, "ssq_ml_selfcheck.json"),
        os.path.join(LIB_DIR, "ssq_history.json"),
    ]
    parts = []
    for p in sig_files:
        try:
            st = os.stat(p)
            parts.append(f"{os.path.basename(p)}:{int(st.st_mtime)}:{st.st_size}")
        except OSError:
            parts.append(f"{os.path.basename(p)}:missing")
    return "|".join(parts)


def _cache_get(target):
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            m = json.load(f)
        if m.get("target_period") != target:
            return None
        if m.get("cache_sig") != _cache_sig():
            return None  # 数据/代码已变, 旧报告失效, 触发重算
        return m
    except Exception:
        return None


def _cache_put(target, report_abs):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({"target_period": target, "report_abs": report_abs,
                       "generated_at": datetime.now().isoformat(),
                       "cache_sig": _cache_sig()},
                      f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _read_report_path():
    p = os.path.join(LIB_DIR, "REPORT_PATH.txt")
    try:
        with open(p, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return None


def _latest_enhanced_in_lib():
    """定位 lib/ 内最新增强版报告(缓存源, 不依赖桌面副本)。"""
    cands = sorted(glob.glob(os.path.join(LIB_DIR, "双色球*V15_增强版.html")),
                   key=os.path.getmtime, reverse=True)
    return cands[0] if cands else None


def _deliver_cached(report_abs):
    """缓存命中时: 把已验证报告直接投递到桌面 + 写 REPORT_PATH.txt(与正常路径一致)。"""
    import shutil
    desktop = _resolve_desktop()
    if desktop and report_abs and os.path.exists(report_abs):
        try:
            shutil.copy2(report_abs, os.path.join(desktop, os.path.basename(report_abs)))
            shutil.copy2(report_abs, os.path.join(desktop, "双色球分析报告_最新.html"))
        except Exception as e:
            print(f"  ⚠ 复制失败(非致命): {e}")
    try:
        with open(os.path.join(LIB_DIR, "REPORT_PATH.txt"), "w", encoding="utf-8") as f:
            f.write(report_abs or "")
    except Exception:
        pass
    print("=" * 64)
    print("REPORT_DESKTOP_PATH: " + (os.path.join(desktop, os.path.basename(report_abs)) if (desktop and report_abs) else ""))
    print("REPORT_ABS_PATH: " + os.path.abspath(report_abs))
    if desktop:
        print("REPORT_LATEST_PATH: " + os.path.join(desktop, "双色球分析报告_最新.html"))
    print("REPORT_PATH_FILE: " + os.path.join(LIB_DIR, "REPORT_PATH.txt"))
    print("=" * 64)


def _run_analysis(extra_args):
    """分析模式（预测+报告）：跑完后保证报告落到桌面并打印绝对路径。

    性能优化(v2.1.26): 按"目标期"缓存。同一期(两次开奖之间)预测是确定性、
    不变的, 复访直接交付已验证报告(秒级), 跳过约 2 分钟完整重算；仅目标期变化
    （出现新开奖）或 --fresh 时重新生产（仍跑 22 项护栏保证诚实）。
    """
    if "--fresh" not in sys.argv:
        target = _current_target_period()
        hit = _cache_get(target) if target else None
        rap = (hit or {}).get("report_abs")
        if hit and rap and os.path.exists(rap):
            print("=" * 64)
            print(f"⚡ 缓存命中 (目标期 {target}): 跳过完整重算, 直接交付已验证报告")
            print(f"   上次生成: {(hit or {}).get('generated_at', '?')}")
            print("=" * 64)
            _deliver_cached(rap)
            return 0

    rc = _run("ssq_smart.py", ["--force"] + extra_args)
    _ensure_report_delivery()
    # 开奖核对（高级验证）：展开本系统推荐的全部注，逐注算奖，对照蒙特卡洛随机基线。
    # 非致命，失败仅告警，不影响主报告交付。
    try:
        _run("ssq_draw_check.py", ["--auto", "--sim", "20000"])
    except Exception as e:
        print(f"  ⚠ 开奖核对异常(非致命): {e}")
    target = _current_target_period()
    rap = _latest_enhanced_in_lib()
    if target and rap:
        _cache_put(target, rap)
    return rc


def _print_help():
    print("""
双色球算法选号防被骗 · 使用说明（中文）
====================================
立场：本工具产出的是「娱乐性参考组合 + 诚实分析报告」，不保证结果。
      数学上任何选号思路都不优于随机，长期玩必亏，请量力而行、理性娱乐。

普通用户只需这一条命令：
  python run_ssq.py
      → 完整跑一遍：联网取数 → 预测 → 22 项自检 → 生成报告
      → 报告会自动复制到你的桌面（双击浏览器打开即可），并提示预览路径

进阶用法（一般用不到，按需）：
  --skip-download   离线跑（用内置离线数据，不联网）
  --healthcheck     只跑 22 项自检护栏，退出码 0 = 一切正常
  --explore         跑「选号思路到底有没有用」的样本外证伪
  --randomness      跑开奖序列随机性检验
  --fresh           强制重新生成（忽略缓存）
  --help            显示本说明

遇到问题：先看 references/faq.md（常见问题集中页）。
完整模块职责：见 references/scripts.md。
""")


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        _print_help()
        return 0
    if "--healthcheck" in args:
        _friendly_banner(args)
        return _run("ssq_healthcheck_all.py", [])
    if "--explore" in args:
        _friendly_banner(args)
        return _run("ssq_method_explorer.py", [])
    if "--randomness" in args:
        _friendly_banner(args)
        return _run("ssq_randomness_test.py", [])

    # 透传支持
    passthrough = []
    if "--passthrough" in args:
        i = args.index("--passthrough")
        passthrough = args[i + 1:]

    if "--skip-download" in args:
        _friendly_banner(args)
        return _run_analysis(["--skip-download"] + passthrough)

    _friendly_banner(args)
    return _run_analysis(passthrough)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n⚠️ 已手动中断。未生成报告，无需处理。")
        sys.exit(130)
    except Exception as e:  # 顶层兜底：把任何意外变成友好提示，而非一串技术报错
        import traceback as _tb
        _log = os.path.join(LIB_DIR, "ssq_error_log.txt")
        try:
            with open(_log, "a", encoding="utf-8") as _f:
                _f.write("\n%s\n%s\n" % ("=" * 40, _tb.format_exc()))
        except Exception:
            _log = "(日志写入失败，不影响本次提示)"
        print("=" * 64)
        print("⚠️ 运行中出现意外情况，本工具未能完成本次分析。")
        print("  这通常源于网络不通、数据文件缺失或运行环境差异，不是你操作有误。")
        print("  可尝试：① 重试一次；② python run_ssq.py --skip-download 离线跑；")
        print("          ③ 查看 references/faq.md 的「运行报错」章节。")
        print("  技术细节已自动记录到日志文件：")
        print("    %s" % _log)
        print("  如需进一步排查，可把这个文件发给开发者，无需自行解读。")
        print("=" * 64)
        sys.exit(1)
