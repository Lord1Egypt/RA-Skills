"""零稀泥模式 — CLI 入口 cli.py

Usage:
    python -m lib.cli run-pipeline -b bug-001 -t config_error
    python -m lib.cli status
    python -m lib.cli resume -b bug-001
"""

import json, os, sys, time, logging
from .config import SKILL_VERSION
from . import state_manager as sm
from .orchestrator import Pipeline, PipelineConfig, PhaseResult, PipelinePhase

log = logging.getLogger("cli")


def cli_status(args):
    state = sm.read()
    checkpoints = state.get("_pipeline_checkpoints", {})
    if not checkpoints:
        print("无活跃流水线")
        return
    for bug_id, cp in checkpoints.items():
        completed = [k for k in ("phase0", "phase1", "phase2", "phase3", "phase4") if k in cp]
        print(f"  {bug_id}: {', '.join(completed)}")


def cli_run_pipeline(args):
    cfg = PipelineConfig(
        session_id=args.session_id or f"cli_{int(time.time())}",
        bug_id=args.bug_id, test_cmd=args.test_cmd or "",
        project_type=args.project_type or "unknown", vcs=args.vcs or "none",
        bug_type=args.bug_type, module=args.module or args.bug_type,
        project_name=args.project or "",
    )
    root_cause_md = ""
    if args.root_cause_file:
        with open(args.root_cause_file, "r", encoding="utf-8") as f:
            root_cause_md = f.read()
    elif args.root_cause_text:
        root_cause_md = args.root_cause_text
    else:
        root_cause_md = input("输入 BUG_ROOT_CAUSE.md 内容:\n")

    test_code = ""
    if args.test_file:
        with open(args.test_file, "r", encoding="utf-8") as f:
            test_code = f.read()

    pipe = Pipeline(cfg)
    results = pipe.run_full_pipeline(
        root_cause_md=root_cause_md, test_code=test_code,
        test_cmd=args.test_cmd or "", bug_type=args.bug_type,
        fix_type=args.fix_type or "permanent", module=args.module or args.bug_type,
        skip_regression=args.skip_regression, skip_reason=args.skip_reason or "",
        project_name=args.project or "", fallback_mode=args.fallback,
    )
    output_list = []
    for r in results:
        entry = {"phase": r.phase, "success": r.success, "blocking": r.blocking, "details": r.details}
        if r.cron_instructions:
            entry["cron_instructions"] = r.cron_instructions
        output_list.append(entry)
    print(json.dumps(output_list, ensure_ascii=False, indent=2))
    failures = [r for r in results if r.blocking and not r.success]
    if failures:
        print(f"失败: {len(failures)} 个阶段阻塞")
        sys.exit(1)
    print("OK: 流水线完成")


def cli_resume(args):
    cfg = PipelineConfig(
        session_id=args.session_id or f"resume_{int(time.time())}",
        bug_id=args.bug_id, state_path=os.environ.get("STATE_PATH", ""),
        test_cmd=args.test_cmd or "", project_type=args.project_type or "unknown",
        vcs=args.vcs or "none", bug_type=args.bug_type or "",
        module=args.module or "", project_name=args.project or "",
    )
    pipe = Pipeline(cfg)
    pending = pipe.resume()
    if not pending:
        print(f"OK: {args.bug_id} 全部阶段已完成")
        sys.exit(0)
    print(f"待执行阶段: {pending}")
    if args.root_cause_file and "phase1" in pending:
        with open(args.root_cause_file, "r", encoding="utf-8") as f:
            r1 = pipe.phase1_root_cause(f.read())
            print(f"Phase 1: {'OK' if r1.success else 'FAIL'}")
    if args.test_file and "phase2" in pending:
        with open(args.test_file, "r", encoding="utf-8") as f:
            r2 = pipe.phase2_test(f.read(), args.test_cmd or "")
            print(f"Phase 2: {'OK' if r2.success else 'FAIL'}")
    if "phase3" in pending:
        r3 = pipe.phase3_closure(test_skipped=True)
        print(f"Phase 3: {'OK' if r3.success else 'FAIL'}")


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="零稀泥模式编排器",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
示例:
  python -m lib.cli run-pipeline -b bug-001 -t config_error
  python -m lib.cli run-pipeline -b bug-001 --test-cmd "pytest tests/"
  python -m lib.cli status
  python -m lib.cli resume -b bug-001
""",
    )
    parser.add_argument("--version", action="version",
                        version=f"zero-cover-mode v{SKILL_VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("run-pipeline", help="运行完整流水线")
    p.add_argument("--bug-id", "-b", required=True)
    p.add_argument("--session-id", "-s")
    p.add_argument("--bug-type", "-t", required=True)
    p.add_argument("--module", "-m")
    p.add_argument("--fix-type", default="permanent", choices=["permanent", "workaround", "reverted"])
    p.add_argument("--test-cmd")
    p.add_argument("--project-type")
    p.add_argument("--vcs")
    p.add_argument("--project", "-p")
    p.add_argument("--root-cause-file")
    p.add_argument("--root-cause-text")
    p.add_argument("--test-file")
    p.add_argument("--skip-regression", action="store_true")
    p.add_argument("--skip-reason")
    p.add_argument("--fallback", action="store_true")

    sub.add_parser("status", help="显示流水线状态")

    p = sub.add_parser("resume", help="断线恢复")
    p.add_argument("--bug-id", "-b", required=True)
    p.add_argument("--session-id", "-s")
    p.add_argument("--bug-type", "-t")
    p.add_argument("--module", "-m")
    p.add_argument("--test-cmd")
    p.add_argument("--project-type")
    p.add_argument("--vcs")
    p.add_argument("--project", "-p")
    p.add_argument("--root-cause-file")
    p.add_argument("--test-file")

    args = parser.parse_args()
    try:
        if args.command == "status":
            cli_status(args)
        elif args.command == "run-pipeline":
            cli_run_pipeline(args)
        elif args.command == "resume":
            cli_resume(args)
    except Exception as e:
        log.error("执行失败: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
