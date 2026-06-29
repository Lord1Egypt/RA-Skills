"""
round-robin-allocator  |  CLI 主入口
======================================
支持两种使用模式：

  模式 A：对话式（逐步引导）
      python main.py

  模式 B：一行统计数据直接输入
      python main.py --input "5个方案，4周，33个项目，比例7:8:10:3:5"
      python main.py --input "3 options, 6 rounds, 20 items, ratio 1:1:2"

输出（每次运行均生成以下文件，路径可通过 --outdir 指定）：
  allocation_result.md   Markdown 表格
  allocation_result.csv  CSV 数据
  allocation_result.html 可交互 HTML 可视化

依赖：Python 标准库（无第三方包）
      可视化需要浏览器打开 HTML（无需服务器）
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

# 确保能找到同目录下的 allocator / visualizer
_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE))

from allocator import allocate, compute_stats, post_process
from visualizer import render_html


# ─────────────────────────────────────────────
# 自然语言解析
# ─────────────────────────────────────────────

# 支持的数字中文/英文词
_CN_NUM = {
    "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
    "十一": 11, "十二": 12, "二十": 20, "三十": 30,
    "百": 100,
}


def _to_int(s: str) -> int | None:
    s = s.strip()
    if s.isdigit():
        return int(s)
    if s in _CN_NUM:
        return _CN_NUM[s]
    return None


def parse_one_line(text: str) -> dict | None:
    """
    从一行文字中尝试提取 N / T / K / ratios。
    仅 T 为必选项，N/K 可二选一，ratios 可选（默认等比例）。

    示例：
      "5个方案，4个周期，33个项目，比例7:8:10:3:5"  (全量)
      "33个项目，4个月"                              (N+T，缺K)
      "4个月，5套方案"                                (T+K，缺N)
      "N=20 T=3 K=4 ratios=1,1,1,2"                  (全量)
      "4个月"                                         (仅 T)
    返回 dict(N?, T, K?, ratios?)；只在 T 也取不到时返回 None
    """
    text = text.strip()

    result: dict = {}

    # 尝试识别 N
    for pat in [
        r"(\d+)\s*(?:个|名|条|位|件|只|台)?\s*(?:项目|对象|样本|用户|学生|员工|商品|条目|item|object|subject|entity)",
        r"N\s*[=:＝]\s*(\d+)",
        r"(?:对象|主体|item)[数量共有]*\s*(\d+)",
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            result["N"] = int(m.group(1))
            break

    # 尝试识别 T（轮次）
    for pat in [
        r"(\d+)\s*(?:个|轮|次)?\s*(?:周期|轮次|轮|周|月|阶段|round|period|week|month|turn)",
        r"T\s*[=:＝]\s*(\d+)",
        r"(?:周期|轮次|轮数|round)[数共]*\s*(\d+)",
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            result["T"] = int(m.group(1))
            break

    # 尝试识别 K
    for pat in [
        r"(\d+)\s*(?:个|套|种|类|条)?\s*(?:方案|选项|策略|类别|组|颜色|option|choice|type|category|scheme|variant)",
        r"K\s*[=:＝]\s*(\d+)",
        r"(?:方案|选项|策略)[数共]*\s*(\d+)",
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            result["K"] = int(m.group(1))
            break

    # 尝试识别比例
    for pat in [
        r"(?:比例|ratio|ratios|权重|weight)\s*[=:＝]?\s*([\d\s:,，/]+)",
    ]:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            raw = m.group(1).strip()
            nums = re.findall(r"\d+\.?\d*", raw)
            if nums:
                result["ratios"] = [float(x) for x in nums]
            break

    # ── 纯数字顺序推断（辅助定位，不覆盖已提取值） ──
    if "T" not in result:
        nums = re.findall(r"\d+", text)
        if len(nums) >= 1:
            # 至少能取到 T
            result.setdefault("T", int(nums[0] if "T" not in result else 0))

    # 如果只有数字且量够，尝试位置推断
    if len(result) < 2:
        nums = re.findall(r"\d+", text)
        if len(nums) >= 2:
            result.setdefault("N", int(nums[0]))
            result.setdefault("T", int(nums[1]))
        if len(nums) >= 3:
            result.setdefault("K", int(nums[2]))
        if len(nums) >= 4:
            k = result.get("K", len(nums) - 3)
            result.setdefault("ratios", [float(x) for x in nums[3:3 + k]])

    # ── T 都没取到 → 无法解析 ──
    if "T" not in result:
        return None

    # 如果 K 已知但没比例 → 等比例
    if "K" in result and "ratios" not in result:
        result["ratios"] = [1.0] * result["K"]

    return result


# ─────────────────────────────────────────────
# 对话式引导
# ─────────────────────────────────────────────

def _ask(prompt: str, validator=None, default=None):
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw = input(f"{prompt}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        try:
            val = validator(raw) if validator else raw
            return val
        except Exception as e:
            print(f"  ⚠️  输入无效：{e}，请重新输入")


def interactive_input(labels: dict | None = None) -> dict:
    """
    逐步对话收集参数。
    labels 可自定义术语，例如 {"obj": "学生", "slot": "月", "option": "方案"}
    """
    if labels is None:
        labels = {}
    obj_name   = labels.get("obj",    "对象")
    slot_name  = labels.get("slot",   "轮次")
    opt_name   = labels.get("option", "选项")

    print()
    print("═" * 50)
    print("  均匀轮转分配工具  |  交互式设置")
    print("═" * 50)
    print(f"  说明：将若干「{obj_name}」在多个「{slot_name}」中，")
    print(f"        按比例分配「{opt_name}」，并尽量让每个{obj_name}")
    print(f"        每次都获得不同的{opt_name}。")
    print()
    print("  提示：直接粘贴一行描述也可自动解析")
    print("        例：「33个项目，4个周期，5个方案，比例7:8:10:3:5」")
    print()

    # 尝试一行解析（支持部分参数）
    first = input("  ▶ 请输入描述（或直接回车进入逐步设置）: ").strip()
    if first:
        parsed = parse_one_line(first)
        if parsed and "T" in parsed:
            n_ok = "N" in parsed
            k_ok = "K" in parsed
            print(f"\n  ✅ 识别：T={parsed['T']}", end="")
            if n_ok: print(f", N={parsed['N']}", end="")
            if k_ok: print(f", K={parsed['K']}", end="")
            if "ratios" not in parsed and k_ok:
                parsed["ratios"] = [1.0] * parsed["K"]
                print(f", 比例等分", end="")
            print()

            if n_ok and k_ok:
                # 全量 → 直接返回
                confirm = input("  确认使用？(y/n) [y]: ").strip().lower()
                if confirm != "n":
                    return parsed
            else:
                # 二维 → 告知用户进入什么路径
                if not n_ok:
                    print(f"  ℹ️  未指定对象数 N，将按「{slot_name}×{opt_name}」二维路径计算")
                if not k_ok:
                    print(f"  ℹ️  未指定方案数 K，将按「{obj_name}×{slot_name}」二维路径计算")
                confirm = input("  确认？(y/n) [y]: ").strip().lower()
                if confirm != "n":
                    return parsed

    # 逐步引导（始终要求全量）
    N = _ask(f"  {obj_name}数量 N", lambda x: int(x) if int(x) > 0 else (_ for _ in ()).throw(ValueError("必须>0")))
    T = _ask(f"  {slot_name}数量 T", lambda x: int(x) if int(x) > 0 else (_ for _ in ()).throw(ValueError("必须>0")))
    K = _ask(f"  {opt_name}数量 K", lambda x: int(x) if int(x) > 0 else (_ for _ in ()).throw(ValueError("必须>0")))

    print(f"\n  请输入 {K} 个{opt_name}的比例（空格/冒号/逗号分隔，例：7 8 10 3 5）")
    ratios_raw = _ask(f"  比例", default=" ".join(["1"] * K))
    nums = re.findall(r"\d+\.?\d*", ratios_raw)
    if len(nums) != K:
        print(f"  ⚠️  识别到 {len(nums)} 个数，期望 {K} 个，将使用等比例")
        ratios = [1.0] * K
    else:
        ratios = [float(x) for x in nums]

    return {"N": N, "T": T, "K": K, "ratios": ratios}


# ─────────────────────────────────────────────
# 输出：Markdown 表格
# ─────────────────────────────────────────────

def write_markdown(
    results: list[dict],
    stats: dict,
    params: dict,
    outpath: Path,
    labels: dict | None = None,
) -> None:
    if labels is None:
        labels = {}
    obj_name  = labels.get("obj",    "对象")
    slot_name = labels.get("slot",   "轮次")
    opt_name  = labels.get("option", "选项")

    T = params["T"]
    K = params["K"]

    lines = []
    lines.append(f"# 均匀轮转分配结果\n")
    lines.append(f"- **{obj_name}总数 N**：{params['N']}")
    lines.append(f"- **{slot_name}数 T**：{T}")
    lines.append(f"- **{opt_name}数 K**：{K}")
    lines.append(f"- **比例**：{params['ratios']}")
    lines.append(f"- **平均覆盖率**：{stats['avg_coverage']:.1%}")
    lines.append(f"- **全覆盖{obj_name}数**：{stats['full_coverage']} / {params['N']}")
    lines.append("")

    # 分配明细表
    header = f"| {obj_name}ID |"
    for t in range(T):
        header += f" {slot_name}{t+1} |"
    header += " 覆盖率 |"
    lines.append(header)

    sep = "|------|" + " ------|" * T + " ------|"
    lines.append(sep)

    for obj in results:
        row = f"| {obj['id']:>4} |"
        for opt in obj["slots"]:
            row += f" {opt_name}{opt} |"
        row += f" {obj['coverage']:.1%} |"
        lines.append(row)

    lines.append("")
    lines.append("## 各轮次分布统计\n")

    stat_header = f"| {slot_name} |"
    for k in range(1, K + 1):
        stat_header += f" {opt_name}{k} |"
    lines.append(stat_header)
    lines.append("|------|" + " ------|" * K)

    for t in range(T):
        row = f"| {slot_name}{t+1} |"
        for k in range(1, K + 1):
            cnt = stats["period_dist"][t].get(k, 0)
            row += f" {cnt} |"
        lines.append(row)

    outpath.write_text("\n".join(lines), encoding="utf-8")
    print(f"  📄 Markdown → {outpath}")


# ─────────────────────────────────────────────
# 输出：CSV
# ─────────────────────────────────────────────

def write_csv(
    results: list[dict],
    params: dict,
    outpath: Path,
    labels: dict | None = None,
) -> None:
    if labels is None:
        labels = {}
    obj_name  = labels.get("obj",    "对象")
    slot_name = labels.get("slot",   "轮次")

    T = params["T"]
    with outpath.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [f"{obj_name}ID"] + [f"{slot_name}{t+1}" for t in range(T)] + ["覆盖率"]
        )
        for obj in results:
            writer.writerow(
                [obj["id"]] + obj["slots"] + [f"{obj['coverage']:.1%}"]
            )
    print(f"  📊 CSV    → {outpath}")


# ─────────────────────────────────────────────
# 配置系统（持久化，代码强制，不靠 LLM 自觉）
# ─────────────────────────────────────────────

_CONFIG_PATH = Path(__file__).parents[2] / ".standardization" / "round-robin-allocator" / "data" / "_allocator_config.json"

_DEFAULT_CONFIG = {
    "skip_confirm": False,
    "default_mode": "algorithm",
}

def _load_config() -> dict:
    """加载配置，文件不存在则创建默认"""
    if _CONFIG_PATH.exists():
        try:
            data = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
            return {**_DEFAULT_CONFIG, **data}
        except Exception:
            pass
    _save_config(_DEFAULT_CONFIG)
    return dict(_DEFAULT_CONFIG)


def _save_config(config: dict) -> None:
    """保存配置"""
    _CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")


_MODE_LABEL = {
    "algorithm": "4-ID排序",
    "random":    "5-随机打乱",
    "fair":      "6-均匀分布",
    "custom":    "7-自定义",
}
_CN_MODE = {}
for k in ("4","5","6","7"):
    key = {"4":"algorithm","5":"random","6":"fair","7":"custom"}[k]
    _CN_MODE[k] = key

def _confirm_or_skip(params: dict, mode_name: str, args, repeat_ratio=None):
    """
    确认表（一级菜单，不嵌套，全中文）：
    1-4=切换后处理, 5=确认, 6=取消, 7=永久跳过, 8=设为默认
    """
    config = _load_config()
    if config.get("skip_confirm") and not args.no_confirm:
        return True, mode_name
    if args.no_confirm:
        return True, mode_name

    # 绘制确认表
    _draw_confirm_table(params, mode_name, args, repeat_ratio)

    while True:
        ans = input("  请输入选项 [1]: ").strip()

        # ── 4-7: 后处理模式 ──
        if ans in _CN_MODE:
            if "N" not in params or "K" not in params:
                print("  ⚠️  参数不全，请先按9补充")
                continue
            new_mode = _CN_MODE[ans]
            if new_mode == "custom" and not repeat_ratio:
                new_mode = "fair"
            return True, new_mode

        # ── 5: 确认执行 ──
        if not ans or ans == "1":
            return True, mode_name

        # ── 2: 取消 ──
        if ans == "2":
            return False, mode_name

        # ── 3: 永久跳过 ──
        if ans == "3":
            config["skip_confirm"] = True
            _save_config(config)
            print("  ℹ️  已保存：永久跳过确认")
            return True, mode_name

        # ── 8: 设置默认后处理（二级菜单：选模式→保存→执行） ──
        if ans == "8":
            print("  ┌─────────────────────────────────────┐")
            print("  │ 选择要设为默认的后处理模式：          │")
            print("  │ 4=ID排序  5=随机打乱  6=均匀分布     │")
            print("  │ 7=自定义                              │")
            print("  └─────────────────────────────────────┘")
            dft = input("  请输入 [4-7]: ").strip()
            if dft in _CN_MODE:
                dft_mode = _CN_MODE[dft]
                if dft_mode == "custom" and not repeat_ratio:
                    dft_mode = "fair"
                config["default_mode"] = dft_mode
                _save_config(config)
                print(f"  ℹ️  默认后处理 → {_MODE_LABEL[dft_mode]}")
                return True, dft_mode  # 设完直接走
            continue

        # ── 9: 等待用户输入补充/修改参数 ──
        if ans == "9":
            print()
            print("  ════════════════════════════════════════")
            print("  当前参数：", end="")
            parts = []
            if "N" in params: parts.append(f"N={params['N']}")
            if "T" in params: parts.append(f"T={params['T']}")
            if "K" in params: parts.append(f"K={params['K']}")
            if "ratios" in params:
                r = ":".join(str(int(x) if x == int(x) else x) for x in params['ratios'])
                parts.append(f"比例={r}")
            print(", ".join(parts) if parts else "无")
            missing = []
            if "N" not in params: missing.append("N(对象数)")
            if "K" not in params: missing.append("K(方案数)")
            if "ratios" not in params: missing.append("比例(默认等分)")
            missed = ", ".join(missing) if missing else "（无）"
            print(f"  缺失/可补充：{missed}")
            print("  ════════════════════════════════════════")
            sup = input("  请输入补充/修改内容：").strip()
            if sup:
                for pat, key in [
                    (r"(\d+)\s*(?:个|名|位|条|只|台)?\s*(?:项目|对象|样本|用户|学生|员工|商品|条目|item|object|subject|entity)", "N"),
                    (r"(\d+)\s*(?:个|轮|次)?\s*(?:周期|轮次|轮|周|月|阶段|round|period|week|month|turn)", "T"),
                    (r"(\d+)\s*(?:个|套|种|类|条)?\s*(?:方案|选项|策略|类别|组|颜色|option|choice|type|scheme|variant)", "K"),
                ]:
                    m = re.search(pat, sup, re.IGNORECASE)
                    if m:
                        params[key] = int(m.group(1))
                m = re.search(r"(?:比例|ratio|ratios|权重|weight)\s*[=:＝]?\s*([\d\s:,，/]+)", sup, re.IGNORECASE)
                if m:
                    nums = re.findall(r"\d+\.?\d*", m.group(1))
                    if nums:
                        params["ratios"] = [float(x) for x in nums]
                print("  ℹ️  已更新参数")
            _draw_confirm_table(params, mode_name, args, repeat_ratio)
            continue

        print("  1=确认  2=取消  3=永久跳过  4-7=后处理  8=设默认  9=修改参数")


def _draw_confirm_table(params, mode_name, args, repeat_ratio):
    # 动态选项 9
    missing_9 = []
    if "N" not in params: missing_9.append("N")
    if "K" not in params: missing_9.append("K")
    opt9 = f"9=补充{'/'.join(missing_9)}" if missing_9 else "9=修改参数"

    print()
    print("  ┌──────────┬" + "─" * 40 + "┐")
    print(f"  │ 参数     │ 值{'':>36}│")
    print("  ├──────────┼" + "─" * 40 + "┤")
    print(f"  │ N (对象) │ {params.get('N','? (缺) 按9补充'):<38}│")
    print(f"  │ T (轮次) │ {params.get('T','? (缺) 按9补充'):<38}│")
    print(f"  │ K (方案) │ {params.get('K','? (缺) 按9补充'):<38}│")
    if "ratios" in params:
        ratio_str = ":".join(str(int(r) if r == int(r) else r) for r in params['ratios'])
        print(f"  │ 比例     │ {ratio_str:<38}│")
    else:
        print(f"  │ 比例     │ ? (缺)（未指定，默认等分）按9补充{'':>3}│")
    print(f"  │ 后处理   │ {_MODE_LABEL.get(mode_name, mode_name):<38}│")
    if args.seed is not None:
        print(f"  │ 随机种子 │ {args.seed:<38}│")
    if mode_name == "custom":
        rr_str = ":".join(str(int(r) if r == int(r) else r) for r in (repeat_ratio or []))
        if rr_str:
            print(f"  │ 月间重复 │ {rr_str:<38}│")
    print("  ├──────────┴" + "─" * 40 + "┤")
    print("  │ 1=确认执行  2=取消  3=永久跳过确认         │")
    print("  │ 后处理: 4=ID排序  5=随机打乱  6=均匀分布    │")
    print("  │         7=自定义                            │")
    print("  │ 8=设默认后处理  9=补充修改参数              │")
    print("  └─────────────────────────────────────────────┘")


def _confirm_or_skip_2d(info: dict, labels: dict, args) -> bool:
    """2D 路径的简化确认表"""
    config = _load_config()
    if config.get("skip_confirm") or args.no_confirm:
        return True, False

    obj_name = labels.get("obj", "对象")
    slot_name = labels.get("slot", "轮次")
    opt_name = labels.get("option", "方案")
    lacks_n = "N" not in info
    lacks_k = "K" not in info
    opt9 = f"9=补充{'/'.join(['N' if lacks_n else '','K' if lacks_k else ''])}" if (lacks_n or lacks_k) else "9=修改参数"

    print()
    print("  ┌──────────┬" + "─" * 40 + "┐")
    print(f"  │ 参数     │ 值{'':>36}│")
    print("  ├──────────┼" + "─" * 40 + "┤")
    print(f"  │ {obj_name}数 │ {str(info.get('N','? (缺)')):<38}│")
    print(f"  │ {slot_name}数 │ {str(info.get('T','? (缺)')):<38}│")
    print(f"  │ {opt_name}数 │ {str(info.get('K','? (缺)')):<38}│")
    if "ratios" in info and info["ratios"]:
        r = info["ratios"]
        rs = ":".join(str(int(x) if x == int(x) else x) for x in r) if len(r) <= 10 else f"{len(r)}项等分"
        print(f"  │ 比例     │ {rs:<38}│")
    print("  ├──────────┴" + "─" * 40 + "┤")
    print("  │ 5=确认执行  6=取消  7=永久跳过  {0:<22}│".format(opt9))
    print("  └─────────────────────────────────────────────┘")

    ans = input("  请输入选项 [5]: ").strip()
    if ans == "9":
        print("  请输入补充信息，例如「5套方案，比例7:8:10:3:5」")
        sup = input("  > ").strip()
        if sup:
            extra = parse_one_line(sup)
            if extra:
                for k in ("N","T","K"):
                    if k in extra: info[k] = extra[k]
                if "ratios" in extra and "K" in info:
                    info["ratios"] = extra["ratios"]
                print("  ℹ️  已更新参数")
        supplemented = "N" in info and "K" in info
        return True, supplemented
    if ans == "7":
        config["skip_confirm"] = True
        _save_config(config)
        print("  ℹ️  已保存：永久跳过确认")
        return True, False
    if ans == "6":
        return False, False
    return True, False  # 默认 5


# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="均匀轮转分配工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--input",  "-i", help="一行统计描述（自动解析）", default=None)
    parser.add_argument("--outdir", "-o", help="输出目录（默认当前目录）", default=".")
    parser.add_argument("--obj",    help="对象术语（默认：对象）",  default=None)
    parser.add_argument("--slot",   help="轮次术语（默认：轮次）",  default=None)
    parser.add_argument("--option", help="选项术语（默认：选项）",  default=None)
    parser.add_argument("--mode",  choices=["algorithm","random","fair","custom"],
                        help="后处理模式", default=None)
    parser.add_argument("--repeat-ratio", help="custom 模式的月间重复比例，例如 4:2:7:1", default=None)
    parser.add_argument("--seed",  type=int, help="random 模式的随机种子", default=None)
    parser.add_argument("--no-html", action="store_true", help="不生成 HTML")
    parser.add_argument("--no-open", action="store_true", help="生成后不自动打开浏览器")
    # 配置相关
    parser.add_argument("--no-confirm", action="store_true", help="跳过本次确认（不影响配置文件）")
    parser.add_argument("--always", action="store_true", help="跳过确认并保存到配置（永久生效）")
    parser.add_argument("--set-default-mode", choices=["algorithm","random","fair","custom"],
                        help="设置默认后处理模式并保存到配置", default=None)
    args = parser.parse_args()

    # ── 处理配置变更指令（不执行分配） ──
    config = _load_config()
    config_changed = False

    if args.always:
        config["skip_confirm"] = True
        config_changed = True
        print("  ℹ️  已保存：永久跳过确认")

    if args.set_default_mode:
        config["default_mode"] = args.set_default_mode
        config_changed = True
        print(f"  ℹ️  已保存：默认后处理模式 → {args.set_default_mode}")

    if config_changed:
        _save_config(config)
        if not args.input:
            return  # 纯配置变更，不执行分配

    # ── 加载配置（覆盖默认值） ──
    config = _load_config()

    labels: dict = {}
    if args.obj:    labels["obj"]    = args.obj
    if args.slot:   labels["slot"]   = args.slot
    if args.option: labels["option"] = args.option

    repeat_ratio = None
    if args.repeat_ratio:
        nums = re.findall(r"\d+\.?\d*", args.repeat_ratio)
        if nums:
            repeat_ratio = [float(x) for x in nums]

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # ── 获取参数 ──
    if args.input:
        params = parse_one_line(args.input)
        if not params or "T" not in params:
            print(f"⚠️  无法解析输入：{args.input!r}")
            print("   至少需要指定周期数，例如：\"4个月，33个项目\"")
            sys.exit(1)

        n_given = "N" in params
        k_given = "K" in params

        if not n_given and not k_given:
            print(f"⚠️  仅识别到周期数 T={params['T']}，缺少 N 或 K")
            sys.exit(1)
    else:
        params = interactive_input(labels)

    # ── 缺失维度补齐提示 ──
    # （比例不写默认等分，确认表会注明）
    if "K" not in params:
        # 提供了 N 但没 K → 标注缺失
        pass

    # ── 确认/补充循环 ──
    mode_name = args.mode if args.mode else config.get("default_mode", "algorithm")

    while True:
        confirmed, mode_name = _confirm_or_skip(params, mode_name, args, repeat_ratio)
        if not confirmed:
            print("  已取消")
            sys.exit(0)

        # 检查参数完整性（N/K/T为必须，比例可选）
        if "N" not in params or "K" not in params:
            print("  ⚠️  N/K 不全，请按9补充")
            continue

        # 比例不提供则默认等分（静默）
        if "ratios" not in params:
            params["ratios"] = [1.0] * params["K"]

        # 完整 → 执行
        args.mode = mode_name
        print()
        run_3d(params, args, labels, outdir, repeat_ratio)
        break

def run_3d(params, args, labels, outdir, repeat_ratio):
    from allocator import allocate, compute_stats, post_process

    print("  ⏳ 正在计算分配方案……")
    results = allocate(params["N"], params["T"], params["K"], params["ratios"])

    mode_name = args.mode or "algorithm"
    print(f"  🔀 后处理模式：{mode_name}", end="")
    if mode_name == "algorithm":
        print("")
    elif mode_name == "random":
        print(f"（seed={args.seed})" if args.seed is not None else "")
    elif mode_name == "fair":
        print("")
    elif mode_name == "custom":
        print(f"（月间比例 {repeat_ratio}）" if repeat_ratio else "")

    results = post_process(
        results, params["N"], params["T"], params["K"],
        mode=mode_name,
        repeat_ratio=repeat_ratio if mode_name == "custom" else None,
        seed=args.seed,
    )
    stats = compute_stats(results, params["T"], params["K"])
    print(f"  ✅ 分配完成：平均覆盖率 {stats['avg_coverage']:.1%}，"
          f"全覆盖 {stats['full_coverage']}/{params['N']} 个对象")
    print()

    _write_outputs(results, stats, params, outdir, labels, args)

    # ── 钩子5：询问 CSV（代码强制，写入前问） ──
    _ask_csv(results, outdir, params, labels)


# ═════════════════════════════════════════════
# 输出工具
# ═════════════════════════════════════════════

def _write_outputs(results, stats, params, outdir, labels, args):
    from visualizer import render_html
    write_markdown(results, stats, params, outdir / "allocation_result.md", labels)
    # CSV 由 _ask_csv 钩子决定是否写入，这里不写
    if not args.no_html:
        render_html(results, stats, params, outdir / "allocation_result.html", labels)
    _open_html(outdir, args)


def _open_html(outdir, args):
    if not args.no_html and not args.no_open:
        try:
            import webbrowser
            html_path = outdir / "allocation_result.html"
            if html_path.exists():
                webbrowser.open(html_path.resolve().as_uri())
                print(f"  🌐 已在浏览器中打开可视化报告")
        except Exception:
            pass


# ═════════════════════════════════════════════
# 二维路径
# ═════════════════════════════════════════════

def _ask_csv(results, outdir, params=None, labels=None) -> None:
    """钩子：询问是否导出 CSV。results 为 None 时不执行写入。"""
    try:
        ans = input("  导出 CSV？(y/n) [n]: ").strip().lower()
        if ans == "y" and results is not None and params is not None:
            csv_path = outdir / "allocation_result.csv"
            write_csv(results, params, csv_path, labels or {})
            print(f"  📊 CSV → {csv_path}")
    except (EOFError, OSError):
        pass


def run_2d_nt(N: int, T: int, labels: dict, outdir: Path) -> None:
    """
    二维 N+T：将 N 个对象均匀分配到 T 个周期。
    无方案概念，仅做分组展示。
    """
    obj_name = labels.get("obj", "对象")
    slot_name = labels.get("slot", "轮次")

    base = N // T
    rem = N % T
    periods = []
    start = 1
    for t in range(T):
        count = base + (1 if t < rem else 0)
        ids = list(range(start, start + count))
        periods.append(ids)
        start += count

    lines = [f"# {obj_name} × {slot_name} 分配结果（二维，无方案概念）\n"]
    lines.append(f"- **{obj_name}总数**：{N}")
    lines.append(f"- **{slot_name}数**：{T}")
    lines.append(f"- **未指定方案数 K**，仅做轮次分组\n")
    for t in range(T):
        ids = periods[t]
        if len(ids) <= 10:
            samples = ", ".join(str(i) for i in ids)
        else:
            samples = f"{ids[0]} ~ {ids[-1]}（共 {len(ids)} 个）"
        lines.append(f"  **{slot_name}{t+1}**：{samples}")
    lines.append("")

    outpath = outdir / "allocation_result.md"
    outpath.write_text("\n".join(lines), encoding="utf-8")
    print(f"  📄 结果 → {outpath}")

    # 显示结果
    print(f"\n{'='*50}")
    print(f"  {N} 个{obj_name} → {T} 个{slot_name}")
    for t in range(T):
        ids = periods[t]
        if len(ids) <= 10:
            samples = ", ".join(str(i) for i in ids)
        else:
            samples = f"{ids[0]} ~ {ids[-1]} ({len(ids)}个)"
        print(f"  {slot_name}{t+1}: {samples}")
    print(f"{'='*50}")

    _ask_csv(None, outdir)


def run_2d_tk(T: int, K: int, ratios: list[float] | None, labels: dict, outdir: Path) -> None:
    """
    二维 T+K：展示各方案在各周期的配额分布。
    无对象概念，仅展示配额表。
    """
    from allocator import _hamilton_quota

    slot_name = labels.get("slot", "轮次")
    opt_name = labels.get("option", "方案")

    if not ratios:
        ratios = [1.0] * K

    total_r = sum(ratios)
    norm = [r / total_r for r in ratios]
    n_base = K * 2
    scaled = _hamilton_quota(n_base, norm, K)

    lines = [f"# {slot_name} × {opt_name} 配额分布（二维，无对象概念）\n"]
    lines.append(f"- **{slot_name}数**：{T}")
    lines.append(f"- **{opt_name}数**：{K}")
    if K <= 10:
        lines.append(f"- **比例**：{ratios}")
    lines.append(f"- **未指定对象数 N**，配额按 N=K×2={n_base} 计算\n")

    if K <= 20:
        header = f"| {slot_name} |"
        for k in range(1, K + 1):
            header += f" {opt_name}{k} |"
        lines.append(header)
        sep = "|------|" + " ------|" * K
        lines.append(sep)
        for t in range(T):
            row = f"| {slot_name}{t+1} |"
            for q in scaled:
                row += f" {q} |"
            lines.append(row)
    else:
        lines.append(f"  K={K} 过大，仅汇总：")
        lines.append(f"  每轮总配额 = {n_base}")
        lines.append(f"  每方案每轮配额 ≈ {n_base/K:.1f}（等比例）")

    lines.append("")
    outpath = outdir / "allocation_result.md"
    outpath.write_text("\n".join(lines), encoding="utf-8")
    print(f"  📄 结果 → {outpath}")

    # 显示结果
    print(f"\n{'='*50}")
    print(f"  {K} 个{opt_name} × {T} 个{slot_name} 配额分布")
    if K <= 10:
        for t in range(T):
            row = f"  {slot_name}{t+1}: "
            row += " | ".join(str(q) for q in scaled)
            print(row)
    else:
        print(f"  每轮每方案配额 ≈ {n_base/K:.1f}（等比例）")
        print(f"  每轮总配额: {n_base}")
    print(f"{'='*50}")

    _ask_csv(None, outdir)


if __name__ == "__main__":
    main()
