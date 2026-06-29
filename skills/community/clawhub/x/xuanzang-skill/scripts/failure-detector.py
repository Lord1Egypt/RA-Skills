"""
failure-detector.py — 突破检测引擎
替代原始 pua 的 failure-detector.sh，运行于 Windows/Python 环境。

功能：
1. 错误签名收集与模式分类（SPINNING/EXPLORING/MIXED）
2. 连续失败追踪与突破检测（≥3 失败后一次成功 → 突破）
3. 峰值压力级别记录
4. 状态文件：data/error_history.jsonl / data/peak_pressure_level

⚠ 运行边界：
  - 本脚本需手动调用，传入上一条工具的执行结果。
  - 在无 hooks 基础设施的环境下无法自动触发，需由 P8 调度层在每轮
    工具调用后主动 invoke。
  - P8 自动化调度循环中，每次工具调用后主动运行本脚本。

用法：
  python scripts/failure-detector.py report <tool_name> <exit_code> [error_output...]
  python scripts/failure-detector.py status
  python scripts/failure-detector.py reset
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── 状态文件路径 ──────────────────────────────────────────
SKILL_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_ROOT / "data"
HISTORY_FILE = DATA_DIR / "error_history.jsonl"
PEAK_FILE = DATA_DIR / "peak_pressure_level"

# ── 错误模式签名 ──────────────────────────────────────────
# SPINNING：同类错误反复出现（工具名相同 / 错误关键字相同）
# EXPLORING：不同工具尝试但都失败（工具名变化 / 参数变化）
# MIXED：既有 SPINNING 又有 EXPLORING

SPINNING_PATTERNS = [
    "ModuleNotFoundError", "ImportError", "NameError",
    "SyntaxError", "IndentationError",
    "command not found", "不是内部或外部命令",
    "Access denied", "权限", "Permission denied",
    "FileNotFoundError", "系统找不到",
]

EXPLORING_PATTERNS = [
    "ConnectionError", "Timeout", "timed out",
    "404", "403", "500", "502",
    "Rate limit", "too many requests",
    "无法解析", "DNS",
]


def ensure_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def classify_pattern(error_text: str, tool_name: str, history: list) -> str:
    """根据错误文本和历史分类为 SPINNING / EXPLORING / MIXED"""
    # 提取最近 5 条失败记录
    recent = [h for h in history[-5:] if h.get("exit_code") != 0]

    has_spinning = False
    has_exploring = False

    # 检查当前错误是否命中 SPINNING 特征
    for pat in SPINNING_PATTERNS:
        if pat.lower() in error_text.lower():
            has_spinning = True
            break

    # 检查历史中是否有同工具重复失败 → SPINNING
    same_tool_fails = [h for h in recent if h.get("tool") == tool_name]
    if len(same_tool_fails) >= 2:
        has_spinning = True

    # 检查历史中是否有不同工具失败 → EXPLORING
    tool_set = {h.get("tool") for h in recent if h.get("tool")}
    if len(tool_set) >= 2:
        has_exploring = True

    if has_spinning and has_exploring:
        return "MIXED"
    elif has_spinning:
        return "SPINNING"
    elif has_exploring:
        return "EXPLORING"
    else:
        return "SPINNING"  # 默认归类为原地打转


def compute_consecutive_fails(history: list) -> int:
    """从最新往前数连续失败次数"""
    count = 0
    for entry in reversed(history):
        if entry.get("exit_code") != 0:
            count += 1
        else:
            break
    return count


def report(tool_name: str, exit_code: str, error_output: str = ""):
    """记录一次工具执行结果，返回检测结果"""
    ensure_dir()

    exit_code_int = int(exit_code)
    timestamp = datetime.now(timezone.utc).isoformat()

    # 读取历史
    history = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        history.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

    # 读取当前峰值压力级别（需在空 history 守卫之前）
    peak_level = 0
    if PEAK_FILE.exists():
        try:
            peak_level = int(PEAK_FILE.read_text(encoding="utf-8").strip())
        except (ValueError, FileNotFoundError):
            pass

    # 空 history 显式守卫：首次调用时无历史，直接降级为安全路径
    if not history:
        # 无历史记录，本条为本会话首条记录
        # 直接构建记录并跳过突破检测（首次不可能触发突破）
        record = {
            "ts": timestamp,
            "tool": tool_name,
            "exit_code": exit_code_int,
            "error_snippet": error_output[:200] if error_output else "",
            "pattern": "SPINNING",
            "consecutive_fails_before": 0,
            "current_level": 0 if exit_code_int == 0 else 1,
            "peak_level": peak_level,
        }
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        result = {
            "breakthrough": False,
            "level": record["current_level"],
            "previous_level": 0,
            "peak_level": peak_level,
            "pattern": record["pattern"],
            "consecutive_fails_before": 0,
            "total_entries": 1,
        }
        print(json.dumps(result, ensure_ascii=False))
        prune_history(keep=50)  # 自动裁剪
        return result

    # 分类模式
    pattern = classify_pattern(error_output, tool_name, history)

    # 计算连续失败（基于追加本条前的历史）
    fails_before = compute_consecutive_fails(history)

    # 确定本条紧箍咒 level
    # L0: 0次失败  L1: 1次  L2: 2次  L3: 3次  L4: 4+次
    if exit_code_int == 0:
        current_level = 0
    else:
        current_level = min(fails_before, 4)

    # 更新峰值
    if current_level > peak_level:
        peak_level = current_level
        PEAK_FILE.write_text(str(peak_level), encoding="utf-8")

    # 构建记录
    record = {
        "ts": timestamp,
        "tool": tool_name,
        "exit_code": exit_code_int,
        "error_snippet": error_output[:200] if error_output else "",
        "pattern": pattern,
        "consecutive_fails_before": fails_before,
        "current_level": current_level,
        "peak_level": peak_level,
    }

    # 追加历史
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # ── 上一轮 level（突破判断时需要）──
    previous_level = history[-1]["current_level"] if history else 0

    # ── 突破检测 ──
    breakthrough = False
    if exit_code_int == 0 and fails_before >= 3 and current_level == 0:
        breakthrough = True
        # L4 突破仅降到 L1，不归零（de-escalation.md Part 1）
        if peak_level >= 4:
            current_level = 1

    # 输出结果（给调用方解析）
    result = {
        "breakthrough": breakthrough,
        "level": current_level,
        "previous_level": previous_level,
        "peak_level": peak_level,
        "pattern": pattern,
        "consecutive_fails_before": fails_before,
        "total_entries": len(history) + 1,
    }
    print(json.dumps(result, ensure_ascii=False))

    if breakthrough:
        if peak_level >= 4:
            print("[紧箍咒 突破 ✨] L4 惨胜——连续 %d 次失败后突破。保留 L1，教训不丢。" % fails_before,
                  file=sys.stderr)
        else:
            print("[紧箍咒 突破 ✨] 连续 %d 次失败后突破。压力归零 L0。" % fails_before,
                  file=sys.stderr)
        # 写入 evolution.md 突破记录骨架（容错：磁盘满/权限不足时优雅降级）
        try:
            evolution_file = DATA_DIR / "evolution.md"
            entry = (
                f"\n## 突破 {timestamp[:10]}\n\n"
                f"- **连续失败**: {fails_before} 次\n"
                f"- **模式**: {pattern}\n"
                f"- **失败根因**: _（P8 降压时填写）_\n"
                f"- **有效方法**: _（P8 降压时填写）_\n"
                f"- **直达路径**: _（P8 降压时填写）_\n"
                f"---\n"
            )
            with open(evolution_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except (OSError, IOError):
            print("[紧箍咒] 突破记录写入失败（磁盘满/权限不足），沉降未持久化。",
                  file=sys.stderr)

    prune_history(keep=50)  # 自动裁剪，保留最近 50 条
    return result


def show_status():
    """查看当前状态"""
    ensure_dir()

    history = []
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        history.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

    peak_level = 0
    if PEAK_FILE.exists():
        try:
            peak_level = int(PEAK_FILE.read_text(encoding="utf-8").strip())
        except ValueError:
            pass

    fails = compute_consecutive_fails(history)
    status = {
        "total_entries": len(history),
        "consecutive_fails": fails,
        "current_level": fails if fails <= 4 else 4,
        "peak_level": peak_level,
        "last_5": history[-5:] if history else [],
    }
    print(json.dumps(status, ensure_ascii=False, indent=2))


def reset_state():
    """重置所有状态"""
    if HISTORY_FILE.exists():
        HISTORY_FILE.unlink()
    if PEAK_FILE.exists():
        PEAK_FILE.unlink()
    print(json.dumps({"reset": True, "message": "状态已清除"}))
    print("[紧箍咒] 状态重置。从 L0 重新开始。", file=sys.stderr)


def prune_history(keep=50):
    """裁剪 error_history.jsonl 只保留最近 N 条"""
    if not HISTORY_FILE.exists():
        return {"pruned": 0, "remaining": 0, "keep": keep}
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    total = len(lines)
    if total <= keep:
        return {"pruned": 0, "remaining": total, "keep": keep}
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines[-keep:])
    return {"pruned": total - keep, "remaining": keep, "keep": keep}


# ── CLI 入口 ──────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python failure-detector.py <report|status|reset|prune> [args...]",
              file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "report":
        if len(sys.argv) < 4:
            print("用法: python failure-detector.py report <tool_name> <exit_code> [error]", file=sys.stderr)
            sys.exit(1)
        tool_name = sys.argv[2]
        exit_code = sys.argv[3]
        error_output = sys.argv[4] if len(sys.argv) > 4 else ""
        report(tool_name, exit_code, error_output)

    elif cmd == "status":
        show_status()

    elif cmd == "reset":
        reset_state()

    elif cmd == "prune":
        keep = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        result = prune_history(keep)
        print(json.dumps(result, ensure_ascii=False))

    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        sys.exit(1)
