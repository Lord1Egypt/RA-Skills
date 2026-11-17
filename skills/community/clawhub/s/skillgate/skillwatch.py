#!/usr/bin/env python3
"""skillwatch — Skill 发布后持续监控（只读）

安全边界声明（SECURITY BOUNDARY）：
- 本工具为**只读监控**：直接调用 SkillGate 进程内扫描函数，不执行子进程，
  不运行被监控 skill 的任何代码，无网络请求。
- 能力评测仅为 dry-run 预览（测试定义）。

Usage:
    python skillwatch.py watch <skill_dir>
    python skillwatch.py watch <skill_dir> --drop-threshold 10
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import skillgate  # noqa: E402


def run_scan(skill_dir: str) -> dict:
    """In-process SkillGate scan (no subprocess)."""
    try:
        result = skillgate.scan_skill(skill_dir)
        d = dataclasses.asdict(result)
        d["trust_score"] = result.trust_score
        d["grade"] = result.grade
        d["critical_count"] = result.critical_count
        d["high_count"] = result.high_count
        return d
    except Exception as e:
        return {"error": str(e)}


def run_bench(skill_dir: str) -> dict:
    """Dry-run benchmark preview (no execution)."""
    import skillbench
    skill_name, tests = skillbench.resolve_tests(skill_dir)
    return {"exit_code": 0, "skill": skill_name, "test_count": len(tests), "dry_run": True}


def _is_reparse_point(path: Path) -> bool:
    """True if the path is a symlink or a Windows junction/reparse point.
    Writing through such a link could redirect the write outside the
    monitored folder, so skillwatch never follows one."""
    try:
        st = path.lstat()
    except OSError:
        return False
    if getattr(st, "st_file_attributes", 0) & 0x400:  # FILE_ATTRIBUTE_REPARSE_POINT
        return True
    return path.is_symlink()


def _safe_history_path(skill_path: Path, history_file: str) -> Path:
    """Resolve the optional history location and refuse anything that could
    redirect the write outside the monitored folder (symlink/junction, or a
    resolved target outside the folder)."""
    target = Path(history_file)
    if not target.is_absolute():
        target = skill_path / target
    target = target.resolve()
    if _is_reparse_point(target):
        raise ValueError(f"历史文件 {history_file} 是符号链接/junction，拒绝写入")
    try:
        target.relative_to(skill_path.resolve())
    except ValueError:
        raise ValueError(f"历史文件 {history_file} 解析后位于监控目录之外，拒绝写入")
    return target


def watch_skill(skill_dir: str, drop_threshold: int = 10, history_file: str = None):
    """Watch a skill: scan + bench, compare to baseline, alert on drop.

    Read-only by default: no file is written unless an explicit
    --history FILE is given (user-chosen location, guarded against
    symlink/junction redirection)."""
    skill_path = Path(skill_dir).resolve()
    if not skill_path.is_dir():
        print(f"错误: 目录不存在 - {skill_dir}", file=sys.stderr)
        sys.exit(2)

    timestamp = datetime.now().isoformat()
    print(f"\n{'='*60}")
    print(f"  SkillWatch 监控报告")
    print(f"  时间: {timestamp}")
    print(f"  Skill: {skill_path.name}")
    print(f"{'='*60}")

    # Gate 1: Security scan
    print(f"\n📋 Gate 1: 安全扫描...")
    scan_result = run_scan(skill_dir)

    if "error" in scan_result:
        print(f"  ❌ 扫描失败: {scan_result['error']}")
        return 1

    current_score = scan_result.get("trust_score", 0)
    grade = scan_result.get("grade", "?")
    print(f"  Trust Score: {current_score}/100 ({grade})")
    print(f"  Critical: {scan_result.get('critical_count', 0)}, High: {scan_result.get('high_count', 0)}")

    # Compare with stored history (only if an explicit --history was given)
    history_path = None
    history = []
    if history_file:
        history_path = _safe_history_path(skill_path, history_file)
        if history_path.exists():
            history = json.loads(history_path.read_text(encoding="utf-8"))

    prev_score = history[-1]["trust_score"] if history else None
    if prev_score is not None:
        delta = current_score - prev_score
        if delta < -drop_threshold:
            print(f"  🚨 严重退化: {prev_score} → {current_score} ({delta:+.1f})")
            print(f"     跌幅超过阈值 {drop_threshold} 分，需要立即检查！")
        elif delta < 0:
            print(f"  ⚠️  轻微下降: {prev_score} → {current_score} ({delta:+.1f})")
        else:
            print(f"  ✅ 稳定/提升: {prev_score} → {current_score} ({delta:+.1f})")

    # Gate 2: Capability bench (dry-run preview)
    print(f"\n🧪 Gate 2: 能力评测（dry-run 预览）...")
    bench_result = run_bench(skill_dir)
    if bench_result["exit_code"] == 0:
        print(f"  ✅ 测试定义预览完成（{bench_result['test_count']} 项，未执行任何代码）")
        print(f"  ℹ️  实际执行请使用仓库 tests/ 下的 pytest 套件")
    else:
        print(f"  ❌ 有测试失败")

    # Save history (only when an explicit --history was given)
    if history_path is not None:
        history.append({
            "timestamp": timestamp,
            "trust_score": current_score,
            "grade": grade,
            "critical": scan_result.get("critical_count", 0),
            "high": scan_result.get("high_count", 0),
            "bench_pass": bench_result["exit_code"] == 0,
        })
        # Keep last 50 entries
        history = history[-50:]
        history_path.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n📊 历史记录已保存: {history_path}")
    else:
        print(f"\nℹ️  只读模式：未写入任何文件（如需持久化基线请指定 --history FILE）")

    # Final verdict
    print(f"\n{'='*60}")
    if scan_result.get("critical_count", 0) > 0 or scan_result.get("high_count", 0) > 0:
        print(f"  ❌ 告警: 发现高风险问题")
        return 1
    elif prev_score and (prev_score - current_score) > drop_threshold:
        print(f"  🚨 告警: Trust Score 暴跌")
        return 1
    else:
        print(f"  ✅ 一切正常")
        return 0


def main():
    ap = argparse.ArgumentParser(description="SkillWatch — Skill 发布后持续监控")
    sub = ap.add_subparsers(dest="command")

    watch_parser = sub.add_parser("watch", help="监控一个 skill")
    watch_parser.add_argument("skill_dir", help="skill 目录路径")
    watch_parser.add_argument("--drop-threshold", type=int, default=10,
                              help="分数跌幅超过此值则告警（默认 10）")
    watch_parser.add_argument("--history", default=None,
                              help="可选：持久化基线的文件路径（默认只读、不写任何文件）")

    args = ap.parse_args()

    if args.command == "watch":
        exit_code = watch_skill(args.skill_dir, drop_threshold=args.drop_threshold,
                                history_file=args.history)
        sys.exit(exit_code)
    else:
        ap.print_help()
        sys.exit(2)


if __name__ == "__main__":
    main()
