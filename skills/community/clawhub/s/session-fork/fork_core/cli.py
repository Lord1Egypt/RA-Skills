# role: cli — 命令行入口（pip 安装后 fork / fork-branch）
"""fork_core.cli — 命令行入口（pip 安装后 `fork` / `fork-branch` 命令）。

与 scripts/create_branch.py 共用同一套逻辑；后者保留为 WorkBuddy 技能目录
内的兼容入口（调本模块 main）。

⚠️ **必须支持「直接执行」**：`python3 fork_core/cli.py --list` 也要能跑。
   2026-09-15 真机实测（用户实际会话）：AI 会自然地试这条路——技能包的代码树里
   就列着 `fork_core/cli.py  # 命令行解析与输出`——而此前它抛
   `ImportError: attempted relative import with no known parent package`，
   在真实会话里**白烧了一轮往返**（该报错作为 function_call_result 留在会话文件里）。
   下面的 shim 在"被当脚本直接执行"时补上 `__package__` 与 sys.path，
   使 `python3 fork_core/cli.py` 与 `python3 -m fork_core.cli` **完全等价**。
"""

import argparse
import os
import shutil
import sys
import time

if __package__ in (None, ""):  # 被当作脚本直接执行（而非 -m / 被导入）
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "fork_core"

from . import available, create_fork, get_adapter, list_forks
from .adapter_base import harden_output
from .engine import ForkError, ForkRegisterError, ForkRollbackError, ForkVerifyError
from ._version import VERSION  # noqa: F401 — 单一来源


def print_tree(metas) -> None:
    """按 parent_id 链打印谱系树（父会话 → 子分支 → 孙分支）。"""
    if not metas:
        print("🌳 暂无谱系（尚未创建分支）")
        return
    by_id = {m.id: m for m in metas}
    children: dict[str, list] = {}
    roots = []
    for m in metas:
        p = m.parent_id or ""
        if p and p in by_id:
            children.setdefault(p, []).append(m)
        else:
            roots.append(m)

    def render(m, prefix="", is_last=True):
        branch_char = "└── " if is_last else "├── "
        label = m.title or m.id[:12]
        extra = ""
        if m.extra.get("at_seq") is not None:
            extra = f"  (atSeq={m.extra['at_seq']})"
        print(f"{prefix}{branch_char}{label}  [{m.id[:8]}]{extra}")
        kids = children.get(m.id, [])
        next_prefix = prefix + ("    " if is_last else "│   ")
        for i, k in enumerate(kids):
            render(k, next_prefix, i == len(kids) - 1)

    print("🌳 Fork 谱系树")
    for i, r in enumerate(roots):
        render(r, "", i == len(roots) - 1)


def _warn_free_text(value, flag: str, allow=None) -> None:
    # allow 允许传单个关键字或一组关键字（current / latest-working 都是合法关键字，
    # 不是"把一段文字当 ID"）。原先只支持单个字符串，新增关键字时容易被漏掉。
    """值明显不像会话/请求 ID（含空格、含中文、或长度 < 8）→ 提示正确写法。

    **只警告，不阻断**：各产品的 id 形态不统一（WorkBuddy 是 UUID；pi 是
    `<时间戳>_<id>`；Hermes 是 `20260914_173913_55daeb`；OpenClaw 是 `agent:…`），
    用严格规则去拦会误伤合法调用。这里只解决一类高频错：**把"一段文字"当成 ID**。

    ⚠️ **已知漏报（2026-09-15 复核，如实记录）**：判据基于"含空格/含中文/长度<8"，
    因此**单个 ≥8 字符的纯英文单词**（如 `refactor`、`moonlight`）不会被告警 ——
    它看起来就像个 id。这类输入会在后续查表阶段失败，届时由 engine 的报错 Hint 兜住
    （`--request-id` / `--session` 未命中时都会提示"若这是一段文字，请改用 --match"）。
    即：**形状体检负责"早提醒"，错误路径负责"全兜底"**，两层互补。
    """
    if not value:
        return
    if allow is not None:
        allowed = (allow,) if isinstance(allow, str) else tuple(allow)
        if value in allowed:
            return
    v = value.strip()
    looks_free = (
        any(ch.isspace() for ch in v)
        or any("\u4e00" <= ch <= "\u9fff" for ch in v)
        or len(v) < 8
    )
    if looks_free:
        print(f"⚠️ {flag} 收到的是「一段文字」而不是 ID：{v!r}", file=sys.stderr)
        print(
            "   若你想「从某段文字那条回复开始打分支」，正确写法是：\n"
            f'     python3 <技能目录>/scripts/create_branch.py --session current --match "{v}"',
            file=sys.stderr,
        )


def _main(argv=None) -> None:
    ap = argparse.ArgumentParser(
        prog="fork",
        description="Cross-product session forking (Fork = Projection Derivative).",
    )
    ap.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    ap.add_argument("--session",
                    help="source session id, or 'current' (this conversation), "
                         "or 'latest-working' (most recent active session)")
    ap.add_argument("--match", help="split-point text within the final assistant reply")
    ap.add_argument("--line", type=int, help="exact 1-based split line (alternative to --match)")
    ap.add_argument("--request-id", help="requestId from product UI 'Copy Request ID' (most precise)")
    ap.add_argument("--name", default=None, help="branch name (default: auto from topic)")
    ap.add_argument("--whole", action="store_true",
                    help="默认模式下强制「整份复制」（含当前未完成回合的叙述）；"
                         "只在会话内打分支时有区别——那种场景默认要切掉本轮（含本指令本身）")
    ap.add_argument("--dry-run", action="store_true", help="locate & validate without landing (writes only a temp file for disk-byte verification, then removes it)")
    ap.add_argument("--list", action="store_true", dest="list_branches", help="list branches in current workspace")
    ap.add_argument("--tree", action="store_true", dest="tree", help="show fork lineage as a tree (with --list)")
    ap.add_argument("--fix", metavar="SESSION_ID", help="re-truncate a branch (workbuddy only)")
    ap.add_argument("--verify", "--doctor", action="store_true", dest="verify", help="real-database health check (L2), alias --doctor")
    ap.add_argument("--adapter", default="workbuddy", choices=available(), help="product adapter")
    args = ap.parse_args(argv)

    # ── 参数形状体检：把"传错了参数"变成**会自我纠正的提示** ──────────────
    # 2026-09-15 实测（用 3B 小模型做输入探针）：它会把用户说的
    # 「从『teal』那条回复开始打分支」里的 teal 塞进 `--request-id`（甚至 `--session`），
    # 而正确写法是 `--session current --match "teal"`。
    # 原报错只把它当"查不到的 ID"，Hint 还往 `--session` 上引 —— 对小模型是误导。
    # 这里**只警告、不阻断**（各产品 id 形态不一，误判代价高于收益），并把正确写法直接写出来。
    _warn_free_text(args.session, "--session", allow=("current", "latest-working"))
    _warn_free_text(args.request_id, "--request-id")

    adapter = get_adapter(args.adapter)

    if args.verify:
        run_verify(adapter)
        return

    if args.list_branches:
        cwd = os.environ.get("WORKBUDDY_CWD")
        if args.tree and hasattr(adapter, "lineage_tree"):
            print_tree(adapter.lineage_tree(cwd))
            return
        branches = list_forks(adapter, cwd)
        if not branches:
            print("📂 当前工作区暂无分支")
        else:
            print(f"📂 当前工作区的分支列表（共 {len(branches)} 个）")
            for b in branches:
                print(f"  - {b.id[:12]}… | {b.title} | {b.status} | {b.created_at}")
        return

    if args.fix:
        if adapter.name != "workbuddy":
            raise SystemExit("--fix is only supported for the workbuddy adapter")
        run_fix(args.fix)
        return

    if not args.session and not args.request_id:
        ap.error("--session is required (or use --list / --request-id auto-resolve)")

    # request-id 模式默认源 = current（引擎会自动反查该 ID 所属的真实会话）
    session_ref = args.session or "current"

    r = create_fork(
        adapter=adapter,
        session_ref=session_ref,
        match_text=args.match,
        line_no=args.line,
        request_id=args.request_id,
        name=args.name,
        dry_run=args.dry_run,
        backups_dir=adapter.backups_dir(),
        whole=args.whole,
    )

    # 源会话**名字**必须回显：打错对话时，父 id 是看不出来的，名字一眼就能看出来
    # （2026-09-15 事故：`--session current` 静默打到另一个对话，输出里只有 id）
    _desc = getattr(adapter, "describe_session", None)
    _src_name = ""
    if callable(_desc):
        try:
            _src_name = _desc(r.src_id) or ""
        except Exception:
            _src_name = ""
    print(f"Source   : {r.src_id}  {'「%s」' % _src_name if _src_name else '（未取到名称）'}")
    print(f"           {r.transcript_path}")
    print(f"Split    : line {r.cut} / {r.total}  ({r.how})")
    print(f"Branch   : {r.new_id}  name={r.name!r}")
    if args.dry_run:
        # v2.4.3：dry-run 走完整校验路径（写 tmp + verify），verified=True 才有真实信息量
        print(f"Verify   : {'✅ OK' if r.verified else 'NOT RUN'} (dry-run 已校验磁盘字节)")
        print("DRY RUN — nothing written. (Would create + register a real branch)")
        return
    if r.backup_dir:
        print(f"Backup   : {r.backup_dir} ({adapter.backup_note()})")
    if r.replacements:
        print(f"Note     : replaced {r.src_id}->{r.new_id} in {r.replacements} structured fields")
    print(f"Verify   : OK ({r.cut} lines, sessionId consistent, zero residue, tail complete)")
    print(f"NEW SESSION ID: {r.new_id}")
    print(f"custom_title: {r.name}  | status: terminated")
    _ro = adapter.readonly_hint(r.dst_path)
    if _ro:
        print(f"⚠️  注意：{_ro}")
    print(f"ACTION   : 分支已创建——{adapter.activation_hint()}")


def run_verify(adapter) -> None:
    """fork --verify / --doctor：真库体检（L2 级，发布/打分支前必跑）。"""
    from .engine import verify_environment

    items = verify_environment(adapter)
    print(f"🩺 fork --verify — {adapter.name} 真库体检（验证分级：L1 fixture / L2 真库 / L3 产品终验）")
    print()
    n_fail = 0
    n_review = 0
    for it in items:
        if not it.ok:
            mark = "❌"
            n_fail += 1
        elif getattr(it, "review", False):
            mark = "⚠️"
            n_review += 1
        else:
            mark = "✅"
        print(f"  {mark} [{it.level}] {it.name}: {it.detail}")
    print()
    if n_fail:
        print(f"❌ 存在失败项（{n_fail} 项）— 请修复后再打分支/发布（L2 真库验证是发布前必须项）")
        sys.exit(1)
    if n_review:
        # "需复核"不阻塞：这是"查得到疑点、但断不定是缺陷"的一档（典型：你在分支里记录了血缘）。
        # 若把它判成失败，闸门会长期常驻红 ⇒ 真问题反而被淹没（v2.4.15 的取舍，见 engine 说明）。
        print(f"✅ 无失败项 — 但有 {n_review} 项需人工复核（见上 ⚠️；通常是你自己在分支里记录了血缘）")
    else:
        print("✅ 全部通过 — 该环境达到 L2 真库级验证，可安全打分支/发布")


def run_fix(fix_session_id: str) -> None:
    """修复被主进程追加了多余消息的分支（WorkBuddy 专用）。"""
    from .engine import _load_lines, locate_last_reply

    wb = get_adapter("workbuddy")
    fix_path, _ = wb.find_transcript(fix_session_id)
    if not fix_path:
        raise SystemExit(f"Transcript not found for {fix_session_id}")

    lines = _load_lines(fix_path)
    total = len(lines)
    cut, _ = locate_last_reply(wb, lines)
    print(f"Source   : {fix_session_id}")
    print(f"Current  : {total} lines")
    print(f"Target   : {cut} lines (locate_last_reply)")
    if cut >= total:
        print("Already correct — no fix needed.")
        return

    ts = time.strftime("%Y%m%d-%H%M%S")
    backup_dir = os.path.join(wb.backups_dir(), ts)
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy2(fix_path, os.path.join(backup_dir, os.path.basename(fix_path)))
    print(f"Backup   : {backup_dir}")

    wb.write_branch(fix_path, lines[:cut])
    check = _load_lines(fix_path)
    print(f"Verify   : {len(check)} lines (was {total}, removed {total - len(check)})")
    print(f"ℹ️  分支文件未锁定只读（**本技能不会替你修改文件权限**）。如需要，可自行设为只读，（用你系统的方式把该文件设为只读）{fix_path}")


def main(argv=None) -> None:
    """CLI 入口：引擎层 ForkError 分层 → 打印错误并退出（引擎不抛 SystemExit，转换在 CLI 层）。

    exit code 语义：1=ForkError 通用 / 2=自检失败（零副作用，可重试）/
    3=登记失败（文件已回滚，可安全重试）/ 4=回滚失败（需人工清理）。
    """
    harden_output()  # 非 UTF-8 终端（中文 Windows cp936）下别让装饰字符打断输出
    try:
        _main(argv)
    except ForkRollbackError as e:
        print(f"!!! 需人工清理 !!!\n{e}", file=sys.stderr)
        raise SystemExit(e.exit_code)
    except ForkRegisterError as e:
        print(f"REGISTER FAILED: {e}", file=sys.stderr)
        print("登记失败——文件已回滚（或已提示路径），可安全重试。", file=sys.stderr)
        raise SystemExit(e.exit_code)
    except ForkVerifyError as e:
        print(f"❌ {e}", file=sys.stderr)
        raise SystemExit(e.exit_code)
    except ForkError as e:
        print(f"❌ {e}", file=sys.stderr)
        raise SystemExit(e.exit_code)
    except Exception as e:  # noqa: BLE001 —— 兜底：缺陷不该以裸 traceback 示人
        # 2026-09-15（Hermes 适配器版本闸实测）：适配器/产品层抛出的非 ForkError 异常
        # 原先直接吐 Python 栈，用户看不到人话。此处统一渲染成一行可读错误。
        # 需要栈时置 FORK_DEBUG=1（保留排查能力，不牺牲可用性）。
        print(f"❌ 意外错误（{type(e).__name__}）：{e}", file=sys.stderr)
        if os.environ.get("FORK_DEBUG"):
            import traceback
            traceback.print_exc()
        raise SystemExit(1)


if __name__ == "__main__":
    sys.exit(main())
