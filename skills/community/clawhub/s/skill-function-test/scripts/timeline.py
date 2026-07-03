"""
timeline.py — 测试流程时间线计时引擎

三级嵌套计时体系（L1 技能加载 / L2 各阶段 / L3 测试运行时）：
  - Python 脚本执行 → 脚本自身在入口/出口自动记 marker
  - subprocess 调用目标技能脚本 → 调用侧记 wall time（自动）
  - LLM 时间 → 由 py_script marker 之间的 gap 自动推导，无需手动标记

用法:
  python timeline.py init <skill-dir>                       — 初始化时间线
  python timeline.py mark <skill-dir> <phase> <label> [end] — 记录 marker
  python timeline.py report <skill-dir>                     — 基础时间线报告
  python timeline.py report <skill-dir> --validate          — 带 gap 推导验证的报告
"""
import json
import os
import sys
import tempfile
import time
from datetime import datetime

# 强制 stdout 使用 UTF-8，避免 Windows GBK 编码问题
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# R-12 审计锚点
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-function-test/data/"

_SKILL_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."
))
_data_dir_abs = os.path.normpath(os.path.join(
    _SKILL_DIR, "..", ".standardization", "skill-function-test", "data"
))

# 流程钩子
_HOOKS_SCRIPT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "hooks.py"
))
def _hook_check(skill_dir: str, step: str):
    """调用 hooks.py 前置检查，失败则 exit"""
    import subprocess as _sp
    r = _sp.run([sys.executable, _HOOKS_SCRIPT, "check", skill_dir, step],
                capture_output=True, text=True, encoding="utf-8")
    if r.stdout and r.stdout.strip():
        print(r.stdout)
    if r.returncode != 0:
        sys.exit(r.returncode)

def _hook_done(skill_dir: str, step: str):
    """调用 hooks.py 标记完成"""
    import subprocess as _sp
    r = _sp.run([sys.executable, _HOOKS_SCRIPT, "done", skill_dir, step],
                capture_output=True, text=True, encoding="utf-8")
    if r.stdout and r.stdout.strip():
        print(r.stdout)

F_TIMELINE = ".timeline.json"
_counter = iter(range(1, 10000))

# 标准工作流序列（用于 --validate gap 推导）
WORKFLOW_SEQUENCE = [
    ("backup",          "备份"),
    ("blueprint",       "蓝皮书扫描"),
    ("scenario",        "场景测试 (S1-S3)"),
    ("function_test",   "功能测试 (D1-D6)"),
    ("s4_constraints",  "S4 约束提取"),
    ("s4_scope",        "S4 全量测试范围"),
    ("s4_validate",     "S4 噪音方案校验"),
    ("s4_play",         "S4 随机化回放"),
    ("s4_report",       "S4 坚守率报告"),
    ("s4_repair",       "S4 结构性修复"),
    ("d1_subprocess",   "D1 subprocess 运行时"),
]


def _next_id() -> str:
    return f"M{next(_counter):04d}"


def _data_dir_for(skill_dir: str) -> str:
    target_name = os.path.basename(os.path.abspath(skill_dir))
    d = os.path.join(_data_dir_abs, target_name)
    os.makedirs(d, exist_ok=True)
    return d


def _timeline_path(skill_dir: str) -> str:
    return os.path.join(_data_dir_for(skill_dir), F_TIMELINE)


def _safe_write_json(path: str, data: dict):
    """原子写入 JSON：先写临时文件，replace 到目标路径，防止截断"""
    fd, tmp = tempfile.mkstemp(suffix=".json", prefix=".tl_tmp_",
                                dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(fd)
        os.replace(tmp, path)
    except Exception:
        # 清理临时文件
        try:
            os.unlink(tmp)
        except Exception:
            pass
        raise


def _load_timeline(skill_dir: str) -> dict:
    path = _timeline_path(skill_dir)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def cmd_init(skill_dir: str):
    """重置时间线文件"""
    tl = {
        "started_at": time.perf_counter(),
        "started_at_iso": datetime.now().isoformat(timespec="milliseconds"),
        "markers": [],
        "workflow_label": {},  # phase → 工作流标签映射
    }
    path = _timeline_path(skill_dir)
    _safe_write_json(path, tl)
    print(f"  [TIMELINE] 已初始化: {path}")


def cmd_mark(skill_dir: str, phase: str, label: str, mark: str = "start",
             parent_id: str = None, marker_type: str = "py_script",
             detail: str = "", manual_time: float = None,
             tags: list[str] = None):
    """记录一个时间 marker"""
    path = _timeline_path(skill_dir)
    if not os.path.exists(path):
        cmd_init(skill_dir)

    with open(path, "r", encoding="utf-8") as f:
        tl = json.load(f)

    entry = {
        "id": _next_id(),
        "parent_id": parent_id,
        "phase": phase,
        "label": label,
        "type": marker_type,
        "mark": mark,
        "t": manual_time if manual_time is not None else time.perf_counter(),
        "detail": detail,
        "tags": tags or [],
    }
    tl["markers"].append(entry)

    _safe_write_json(path, tl)

    marker_icon = "[START]" if mark == "start" else "[END]"
    t_sec = entry["t"]
    rel = f"{t_sec - tl['started_at']:.3f}s" if tl["markers"] else "0.000s"
    print(f"  [TIMELINE] {marker_icon} [{phase}] {label}  @{rel}  ({entry['id']})")


# ═══════════════════════════════════════════════════════
# 子流程计时包装器
# ═══════════════════════════════════════════════════════

def run_with_timing(skill_dir: str, cmd_args: list[str], label: str,
                    parent_id: str = None, phase: str = "subprocess",
                    timeout: int = 30, cwd: str = None) -> dict:
    """
    执行 subprocess 并记录 wall time，返回结果 + 计时信息。
    返回: {returncode, stdout, stderr, wall_time, pure_time, marker_id}
    """
    import subprocess as _sp

    t0 = time.perf_counter()
    tl_path = _timeline_path(skill_dir)
    started_at = None
    if os.path.exists(tl_path):
        with open(tl_path, "r") as f:
            d = json.load(f)
            started_at = d.get("started_at", t0)

    start_mid = _next_id()
    _append_marker(skill_dir, start_mid, parent_id, phase, label,
                   "start", "subprocess_wall", t0, f"启动: {' '.join(cmd_args[-3:])}")
    rel = f"{t0 - started_at:.3f}s" if started_at else "0.000s"
    print(f"  [TIMELINE] [START] [{phase}] {label}  @{rel}  ({start_mid})")

    try:
        result = _sp.run(
            cmd_args, capture_output=True, text=True, timeout=timeout, cwd=cwd
        )
    except _sp.TimeoutExpired:
        result = type("obj", (), {"returncode": -1, "stdout": "", "stderr": "timeout"})
    except Exception as e:
        result = type("obj", (), {"returncode": -2, "stdout": "", "stderr": str(e)})

    t1 = time.perf_counter()
    wall = t1 - t0
    detail = f"rc={result.returncode}, wall={wall:.3f}s"
    end_mid = _next_id()
    _append_marker(skill_dir, end_mid, start_mid, phase, label,
                   "end", "subprocess_wall", t1, detail,
                   tags=[f"rc={result.returncode}", f"wall={wall:.3f}s"])
    rel_end = f"{t1 - started_at:.3f}s" if started_at else "0.000s"
    print(f"  [TIMELINE] [END] [{phase}] {label}  @{rel_end}  ({end_mid}) wall={wall:.3f}s")

    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "wall_time": wall,
        "pure_time": None,
        "start_marker_id": start_mid,
        "end_marker_id": end_mid,
    }


def _append_marker(skill_dir: str, mid: str, parent_id: str,
                   phase: str, label: str, mark: str,
                   marker_type: str, t: float, detail: str,
                   tags: list[str] = None):
    """向时间线文件追加一条 marker"""
    path = _timeline_path(skill_dir)
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        tl = json.load(f)
    tl["markers"].append({
        "id": mid,
        "parent_id": parent_id,
        "phase": phase,
        "label": label,
        "type": marker_type,
        "mark": mark,
        "t": t,
        "detail": detail,
        "tags": tags or [],
    })
    _safe_write_json(path, tl)


# ═══════════════════════════════════════════════════════
# Gap 推导：从 py_script marker 间隙自动识别 LLM 时间
# ═══════════════════════════════════════════════════════

def analyze_gaps(markers: list[dict], started_at: float) -> dict:
    """
    分析 marker 间的 gap，自动推导 LLM 工作时段。

    逻辑:
    1. 只关注 py_script 类型的 start/end（忽略 subprocess_wall，它们嵌套在 py_script 内）
    2. 按时间排序后，py_script end → 下一个 py_script start 之间的 gap = LLM 时段
    3. 根据工作流序列给每个 gap 打标签

    返回:
        {
            "py_script_times": [{"phase", "dur", "start", "end"}, ...],
            "llm_gaps": [{"from_phase", "to_phase", "dur", "label", "rel_start"}, ...],
            "unaccounted": [{"start", "end", "dur"}, ...],  # gap > 30s 的未归属时段
        }
    """
    # 只取 py_script 类型的 start/end
    py_events = []
    for m in markers:
        if m["type"] == "py_script":
            py_events.append(m)
        # subprocess_wall 也纳入：subprocess_wall end = py_script 内
        if m["type"] == "subprocess_wall" and m["mark"] == "end":
            py_events.append(m)

    # 排序
    py_events.sort(key=lambda m: m["t"])

    # 提取完整的时间段（start→end pairs）
    type_starts = {}
    py_script_times = []
    for m in py_events:
        phase = m["phase"]
        if m["mark"] == "start":
            type_starts.setdefault(phase, []).append(m["t"])
        elif m["mark"] == "end" and phase in type_starts and type_starts[phase]:
            ts = type_starts[phase].pop(0)
            py_script_times.append({
                "phase": phase,
                "label": m["label"],
                "dur": m["t"] - ts,
                "start": ts,
                "end": m["t"],
            })

    py_script_times.sort(key=lambda x: x["start"])

    # 推导 gap
    llm_gaps = []
    unaccounted = []
    total_llm = 0.0
    prev_end = started_at

    for seg in py_script_times:
        gap = seg["start"] - prev_end
        if gap > 0.01:  # 10ms 以上的 gap 才计入（过滤计时精度噪声）
            # 找工作流序列标签
            gap_label = _find_gap_label(seg["phase"], py_script_times, seg["start"])
            total_llm += gap
            llm_gaps.append({
                "from_time": prev_end - started_at,
                "dur": gap,
                "label": gap_label,
                "after_phase": seg["phase"],
            })
            if gap > 30:
                unaccounted.append({
                    "rel_start": prev_end - started_at,
                    "rel_end": seg["start"] - started_at,
                    "dur": gap,
                })
        prev_end = seg["end"] if seg["end"] > prev_end else prev_end

    return {
        "py_script_times": py_script_times,
        "llm_gaps": llm_gaps,
        "total_llm": total_llm,
        "unaccounted": unaccounted,
    }


def _find_gap_label(next_phase: str, segments: list, gap_start: float) -> str:
    """根据工作流上下文给 gap 打标签"""
    phase_labels = {
        "backup":           "准备阶段（加载、备份）",
        "blueprint":        "蓝皮书扫描与分析",
        "scenario":         "场景测试审查 + S4 规划",
        "function_test":    "功能测试审查 + LLM 分析",
        "s4_constraints":   "S4 约束评估与推理",
        "s4_scope":         "S4 测试范围分析",
        "s4_play":          "S4 回放结果审查",
        "s4_repair":        "S4 修复审查",
        "d1_subprocess":    "运行时验证等待",
    }
    # 上一个已完成阶段的标签
    returned = []
    for seg in segments:
        if seg["end"] <= gap_start + 0.001:
            returned.append(seg["phase"])
    if returned:
        prev = returned[-1]
        return phase_labels.get(prev, f"阶段间处理（{prev} 后）")

    # 无前置阶段 → 初始准备
    return "初始准备"


# ═══════════════════════════════════════════════════════
# 报告生成（含 --validate）
# ═══════════════════════════════════════════════════════

def cmd_report(skill_dir: str, validate: bool = False):
    """生成层级时间线报告"""
    tl = _load_timeline(skill_dir)
    if not tl or not tl.get("markers"):
        print("  [TIMELINE] ⚠️ 无时间线数据，请先运行 init + mark")
        return

    markers = tl["markers"]
    started_at = tl["started_at"]
    lines = []

    lines.append("=" * 62)
    lines.append("  测试流程时间线报告")
    lines.append(f"  起始: {tl.get('started_at_iso', '?')}")
    lines.append("=" * 62)

    total_end = max(m["t"] for m in markers)
    total_duration = total_end - started_at

    # ── Gap 推导（自动计算 LLM 时间） ──
    gap_data = analyze_gaps(markers, started_at)

    total_py = sum(s["dur"] for s in gap_data["py_script_times"])
    total_llm = gap_data["total_llm"]

    lines.append(f"  总耗时: {total_duration:.3f}s")
    lines.append(f"  脚本执行: {total_py:.3f}s  |  LLM 时段: {total_llm:.3f}s  |  其他: {total_duration - total_py - total_llm:.3f}s")
    lines.append("")

    # ── 时间线详情 ──
    lines.append("── 时间线:")

    sorted_markers = sorted(markers, key=lambda m: m["t"])

    # 插入推导的 LLM gap 时段到时间线
    timeline_entries = []
    for seg in gap_data["py_script_times"]:
        timeline_entries.append({
            "rel": seg["start"] - started_at,
            "text": f"[SCRIPT] {seg['label']} ({seg['dur']:.3f}s)",
            "type": "script",
        })
    for gap in gap_data["llm_gaps"]:
        timeline_entries.append({
            "rel": gap["from_time"],
            "text": f"[LLM]   {gap['label']} ({gap['dur']:.3f}s)",
            "type": "llm",
        })

    timeline_entries.sort(key=lambda e: e["rel"])

    for entry in timeline_entries:
        lines.append(f"  @{entry['rel']:>8.3f}s  {entry['text']}")

    # ── 耗时汇总（分组） ──
    lines.append("")
    lines.append("── 耗时汇总:")

    # Python 脚本按 phase 分组
    phase_durs = {}
    target_durs = {}
    for m in sorted_markers:
        p = m["phase"]
        if m["type"] == "subprocess_wall" and m["mark"] == "start":
            # 找对应的 end
            for me in sorted_markers:
                if me.get("parent_id") == m["id"] and me["mark"] == "end":
                    wall = me["t"] - m["t"]
                    # 判断是否是目标技能脚本
                    if p.startswith("target_") or p == "d1_subprocess":
                        target_durs[p] = target_durs.get(p, 0) + wall
                    break

    # 高亮目标技能耗时
    total_target = sum(target_durs.values())
    total_script = total_py - total_target

    lines.append(f"  {'本技能脚本':<25s} {total_script:>8.3f}s ({total_script/total_duration*100:>5.1f}%)")
    lines.append(f"  {'目标技能脚本':<25s} {total_target:>8.3f}s ({total_target/total_duration*100:>5.1f}%)")
    lines.append(f"  {'LLM 处理':<25s} {total_llm:>8.3f}s ({total_llm/total_duration*100:>5.1f}%)")

    # ── Validate 检查 ──
    if validate:
        lines.append("")
        lines.append("── Validate 检查:")
        all_phases = set(m["phase"] for m in markers)

        # 检查预期阶段
        for phase_id, phase_label in WORKFLOW_SEQUENCE:
            found = any(phase_id in p or p.startswith(phase_id) for p in all_phases)
            status = "OK" if found else "MISS"
            lines.append(f"  [{status}] {phase_label}")

        # 未归属 gap 检查
        if gap_data["unaccounted"]:
            lines.append("")
            lines.append("  ⚠️ 未归属长间隙 (>30s):")
            for ua in gap_data["unaccounted"]:
                lines.append(f"    @{ua['rel_start']:.1f}s → @{ua['rel_end']:.1f}s  ({ua['dur']:.1f}s)")

        # 完整性
        missing = [f"{p[1]}" for p in WORKFLOW_SEQUENCE
                   if not any(p[0] in ph or ph.startswith(p[0]) for ph in all_phases)]
        if missing:
            lines.append(f"  ❌ 缺失阶段: {', '.join(missing)}")
        else:
            lines.append("  ✅ 所有标准阶段已覆盖（按需）")

    lines.append("=" * 62)
    print("\n".join(lines))

    # 返回数据结构供外部调用
    return {
        "total_duration": round(total_duration, 3),
        "total_py_script": round(total_py, 3),
        "total_llm": round(total_llm, 3),
        "total_target_skill": round(total_target, 3),
        "gap_data": gap_data,
    }


# ═══════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════

def _parse_tags(args: list[str]) -> list[str]:
    tags = []
    i = 0
    while i < len(args):
        if args[i] == "--tag" and i + 1 < len(args):
            tags.append(args[i + 1])
            args.pop(i)
            args.pop(i)
        else:
            i += 1
    return tags


USAGE = """
用法:
  python timeline.py init <skill-dir>                       — 初始化时间线
  python timeline.py mark <skill-dir> <phase> <label> [end] — 记录 marker
  python timeline.py report <skill-dir>                     — 基础报告
  python timeline.py report <skill-dir> --validate           — 验证+gap推导报告

mark 选项:
  --type <type>    py_script | subprocess_wall
  --detail <text>  附加说明
  --tag <k=v>      标签（可多次）
"""


def main():
    if len(sys.argv) < 3:
        print(USAGE)
        return

    cmd = sys.argv[1]
    skill_dir = sys.argv[2]

    if cmd == "init":
        cmd_init(skill_dir)
        _hook_done(skill_dir, "init")

    elif cmd == "mark":
        if len(sys.argv) < 4:
            print("用法: ... mark <skill-dir> <phase> <label> [end]")
            return
        phase = sys.argv[3]
        label = sys.argv[4] if len(sys.argv) > 4 else phase
        mark = "end" if len(sys.argv) > 5 and sys.argv[5] == "end" else "start"

        parent_id = None
        marker_type = "py_script"
        detail = ""
        manual_time = None

        rest = sys.argv[5:]
        parsed_tags = _parse_tags(rest)
        for j in range(len(rest)):
            if rest[j] == "--parent" and j + 1 < len(rest):
                parent_id = rest[j + 1]
            elif rest[j] == "--type" and j + 1 < len(rest):
                marker_type = rest[j + 1]
            elif rest[j] == "--detail" and j + 1 < len(rest):
                detail = rest[j + 1]
            elif rest[j] == "--time" and j + 1 < len(rest):
                try:
                    manual_time = float(rest[j + 1])
                except ValueError:
                    pass

        cmd_mark(skill_dir, phase, label, mark, parent_id, marker_type,
                 detail, manual_time, parsed_tags)

    elif cmd == "report":
        validate = "--validate" in sys.argv
        cmd_report(skill_dir, validate=validate)

    else:
        print(f"未知命令: {cmd}")
        print(USAGE)


if __name__ == "__main__":
    main()
