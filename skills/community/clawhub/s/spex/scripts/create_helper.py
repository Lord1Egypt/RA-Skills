"""Helper utilities for spec creation."""

from __future__ import annotations

import json
import re
import secrets
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from cli import ArgumentParser
from common import (
    DEFAULT_SPEX_BRANCH_PREFIX,
    SpecMeta,
    atomic_write_json,
    logger,
    resolve_spec_dir,
    strip_date_prefix,
    wrap_text,
)

SPEC_NAME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*$")
DATE_PREFIX_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-")
MAX_SPEC_NAME_BYTES = 64


def _new_session_id() -> str:
    """Generate a collision-resistant create-session id."""
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    return f"{stamp}-{secrets.token_hex(2)}"


def _require_spex_root() -> str:
    """Return spex_root or exit with an error."""
    import config as cfg

    spex_root = cfg.get_project_context().spex_root
    if not spex_root:
        logger.error(
            "Error: cannot determine spex_root. "
            "Configure .spex.toml with spex_root.",
        )
        sys.exit(1)
    return spex_root


def _do_begin_session(_args=None):
    """Create or reuse an active create session; print JSON to stdout."""
    from common import local_iso_timestamp
    from debug_log import (
        debug_enabled,
        get_active_session_id,
        session_debug_log_path,
        set_active_session,
    )

    spex_root = _require_spex_root()
    existing = get_active_session_id(spex_root)
    if existing:
        log_path = session_debug_log_path(spex_root, existing)
        print(
            json.dumps(
                {
                    "session_id": existing,
                    "log_path": str(log_path),
                    "active": True,
                }
            )
        )
        return

    session_id = _new_session_id()
    log_path = session_debug_log_path(spex_root, session_id)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    set_active_session(spex_root, session_id)

    if debug_enabled(sys.argv):
        ts = local_iso_timestamp()
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(
                f"===== CREATE session begin id={session_id} ts={ts} =====\n"
            )

    print(
        json.dumps(
            {
                "session_id": session_id,
                "log_path": str(log_path),
                "active": True,
            }
        )
    )


def _resolve_end_session_spec_dir(args, spex_root: str) -> Path | None:
    """Resolve optional --name / --spec-path to an existing spec directory.

    Returns ``None`` only when neither target flag was provided. When a target
    was given but cannot be resolved uniquely, logs an error and exits 1.
    """
    spec_path = getattr(args, "spec_path", None)
    if spec_path:
        path = Path(spec_path)
        if not path.is_dir():
            logger.error(
                "Error: spec path does not exist or is not a directory: %s",
                path,
            )
            sys.exit(1)
        return path

    name = getattr(args, "name", None)
    if not name:
        return None

    return resolve_spec_dir(name, Path(spex_root) / "specs")


def _do_end_session(args):
    """Clear active session; optionally merge-then-delete into a spec.

    When ``--name`` / ``--spec-path`` is provided, resolve the target before
    clearing the active pointer so a failed handoff leaves the session intact.
    """
    from debug_log import (
        clear_active_session,
        get_active_session_id,
        merge_session_log_into_spec,
    )

    spex_root = _require_spex_root()
    # Resolve explicit merge target first — may exit(1) without clearing.
    spec_dir = _resolve_end_session_spec_dir(args, spex_root)

    session_id = get_active_session_id(spex_root)
    merged_into = None
    deleted = False

    if session_id and spec_dir is not None:
        target = merge_session_log_into_spec(spex_root, session_id, spec_dir)
        if target is not None:
            merged_into = str(target)
            deleted = True

    clear_active_session(spex_root)
    print(
        json.dumps(
            {
                "ended": True,
                "merged_into": merged_into,
                "deleted": deleted,
            }
        )
    )


def _append_create_debug_anchor(log_path: Path, line: str) -> None:
    """Append a CREATE debug anchor; propagate OSError (hard success signal).

    Unlike APPLY's soft ``append_debug_anchor`` (tee best-effort), CREATE
    handoff/post-action anchors must fail loud so prepare does not clear
    the active session after a missing prepare-ok marker.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)
    text = line if line.endswith("\n") else f"{line}\n"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _handoff_session_after_prepare(
    spex_root: str, spec_dir: Path, spec_name: str,
) -> None:
    """Merge active session into spec debug.log, write prepare anchor, clear.

    Fixed order: (1) merge session content into ``spec_dir/debug.log`` and
    delete the session log; (2) if debug, append prepare-spec ok anchor;
    (3) clear the active-session pointer — only after a successful merge or
    when there was no session log to merge (so a failed merge keeps the
    pointer for retry).
    """
    from debug_log import (
        DEBUG_LOG_NAME,
        clear_active_session,
        debug_enabled,
        get_active_session_id,
        merge_session_log_into_spec,
        session_debug_log_path,
    )

    session_id = get_active_session_id(spex_root)
    should_clear = True
    if session_id:
        target = merge_session_log_into_spec(spex_root, session_id, spec_dir)
        if target is None:
            # merge returns None for no-file noop *and* OSError failure.
            # Keep the pointer only when the session log still exists.
            try:
                should_clear = not session_debug_log_path(
                    spex_root, session_id,
                ).is_file()
            except ValueError:
                should_clear = True

    if debug_enabled(sys.argv):
        _append_create_debug_anchor(
            Path(spec_dir) / DEBUG_LOG_NAME,
            f"===== CREATE prepare-spec ok name={spec_name} =====",
        )

    if should_clear:
        clear_active_session(spex_root)


def create_spec(spec, specs_dir, auto_prefix=True):
    """Create a spec directory under specs_dir.

    Returns (spec_name, spec_dir) tuple.
    Raises ValueError on invalid input, FileExistsError if spec exists.
    """
    specs_dir = Path(specs_dir)

    if not DATE_PREFIX_PATTERN.match(spec) and auto_prefix:
        prefix = datetime.now().strftime("%Y-%m-%d-%H-%M")
        spec = f"{prefix}-{spec}"

    if not SPEC_NAME_PATTERN.match(spec):
        raise ValueError(
            f"invalid spec name '{spec}'. "
            "Must match YYYY-MM-DD-HH-MM-<name> with [a-z0-9-]."
        )

    if len(spec.encode("utf-8")) > MAX_SPEC_NAME_BYTES:
        raise ValueError(f"spec name '{spec}' exceeds {MAX_SPEC_NAME_BYTES} bytes.")

    spec_dir = specs_dir / spec
    if spec_dir.exists():
        raise FileExistsError(f"'{spec}' already exists, use a different name.")

    specs_dir.mkdir(parents=True, exist_ok=True)
    spec_dir.mkdir()
    return (spec, spec_dir)


def _write_meta(spec_dir, ctx, prompt, timestamp, description=""):
    """Write meta.json into spec_dir with project context and prompt."""
    workdir = str(ctx.top_workdir) if ctx.in_git_workdir() else ""
    main_worktree = str(ctx.main_worktree) if ctx.main_worktree else workdir
    meta = SpecMeta(
        name=strip_date_prefix(Path(spec_dir).name),
        workdir=workdir,
        main_worktree=main_worktree,
        remote_url=ctx.remote_url,
        branch=ctx.branch,
        user_name=ctx.user_name,
        user_email=ctx.user_email,
        created_at=timestamp,
        prompts=[{"text": prompt, "timestamp": timestamp}] if prompt else [],
        description=wrap_text(description) if description else "",
    )
    meta_path = Path(spec_dir) / "meta.json"
    atomic_write_json(meta_path, meta.to_dict())


def validate_create_branch(
    config: dict, cwd: str | Path | None = None,
) -> str:
    """Validate whether branch creation is enabled and feasible.

    Prints errors to stderr and exits on failure.
    Returns the current branch name on success.
    """
    from branch import get_current_branch, switch_branch

    try:
        current = get_current_branch(cwd)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error: cannot determine current branch: {e}")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

    if not bool(config["branch_management"]):
        logger.info("Note: branch management is not enabled in .spex.toml, "
                    "will not create new branch for spec.")
        return current

    main_branch = config["main_branch_name"]
    if main_branch and current != main_branch:
        logger.warning(
            f"Warning: current branch '{current}' does not match "
            f"main_branch_name '{main_branch}'. "
            f"Switching to '{main_branch}'...",
        )
        try:
            switch_branch(main_branch, cwd)
        except subprocess.CalledProcessError as e:
            logger.error(
                f"Error: failed to switch to '{main_branch}': "
                f"{e.stderr.strip() or e}",
            )
            sys.exit(-1)
        logger.info(f"Switched to branch '{main_branch}'.")
        return main_branch

    if current.startswith(DEFAULT_SPEX_BRANCH_PREFIX):
        logger.error(
            f"Error: current branch '{current}' starts with "
            f"'{DEFAULT_SPEX_BRANCH_PREFIX}'.\n"
            f"Hint: configure 'main_branch_name' in .spex.toml "
            f"to enable automatic branch switching.",
        )
        sys.exit(1)

    return current


def cli_create_validate() -> None:
    """CLI: validate branch creation feasibility."""

    import config as cfg

    ctx = cfg.get_project_context()
    current = validate_create_branch(ctx.config, cwd=ctx.main_worktree)
    if current:
        logger.info(f"Valid: currently on branch '{current}'")


def _do_prepare_spec(args):
    """Create spec directory and return JSON with metadata."""
    import config as cfg
    import hooks
    from common import get_specs_dir, local_iso_timestamp

    specs_dir = get_specs_dir()
    prompt = "" if sys.stdin.isatty() else sys.stdin.read().strip()

    try:
        spec_name, spec_dir = create_spec(args.name, specs_dir)
    except (ValueError, FileExistsError) as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

    ctx = cfg.get_project_context()
    timestamp = local_iso_timestamp()
    _write_meta(spec_dir, ctx, prompt, timestamp, args.description)

    if ctx.spex_root:
        _handoff_session_after_prepare(ctx.spex_root, spec_dir, spec_name)

    spex_branch = DEFAULT_SPEX_BRANCH_PREFIX + strip_date_prefix(spec_name)
    hooks.run_pre_action(
        "create",
        {"spex_branch": spex_branch},
        workdir=ctx.top_workdir,
        spec_name=spec_name,
    )

    import prompt as prompt_mod

    result = {
        "spec_name": spec_name,
        "spec_path": str(spec_dir),
        "spec_template": prompt_mod.render_prompt("spec-template", spec_name),
    }
    print(json.dumps(result, indent=2))


def cli_prepare_spec(argv=None):
    """CLI: create spec directory and return JSON with metadata."""

    args = _build_parser().parse(["prepare-spec"] + (argv or []))
    _do_prepare_spec(args)


REQUIRED_FIELDS = ("id", "name", "details", "completed_at", "commit_title")


def _do_post_action(args):
    """Validate todo.json and trigger post-action hook."""
    from common import (
        SpecMeta,
        load_and_validate_todo_json,
        load_meta,
        parse_front_matter_description,
        validate_unique_ids,
    )
    from config import get_project_context

    spec_dir = resolve_spec_dir(args.name)
    json_path = spec_dir / "todo.json"

    if not json_path.is_file():
        logger.error(f"Error: {json_path} not found.")
        sys.exit(1)

    data = load_and_validate_todo_json(json_path)
    validate_unique_ids(data)
    for i, item in enumerate(data):
        for field in REQUIRED_FIELDS:
            if field not in item:
                logger.error(
                    f"Error: item[{i}]: missing required"
                    f" field '{field}'.",
                )
                sys.exit(1)
    logger.info(f"OK: {len(data)} step(s) validated.")

    # Update description from spec.md front-matter
    spec_path = spec_dir / "spec.md"
    if spec_path.is_file():
        spec_content = spec_path.read_text(encoding="utf-8")
        desc = parse_front_matter_description(spec_content)
        if desc:
            meta_path = spec_dir / "meta.json"
            meta_data = load_meta(spec_dir) or SpecMeta()
            meta_data.description = wrap_text(desc)
            atomic_write_json(meta_path, meta_data.to_dict())

    import hooks
    from debug_log import DEBUG_LOG_NAME, debug_enabled

    meta = load_meta(spec_dir)
    spec_name = spec_dir.name
    ctx = get_project_context()
    workdir = (meta.workdir if meta else "") or (
        str(ctx.top_workdir) if ctx.in_git_workdir() else None
    )
    done = sum(
        1 for item in data
        if isinstance(item, dict) and item.get("completed_at")
    )
    undone = len(data) - done
    spex_branch = meta.spex_branch if meta else ""

    if debug_enabled(sys.argv):
        _append_create_debug_anchor(
            spec_dir / DEBUG_LOG_NAME,
            f"===== CREATE post-action ok name={spec_name} "
            f"steps={len(data)} =====",
        )

    hooks.run_post_action(
        args.event_type,
        {"spex_branch": spex_branch, "done": done, "undone": undone},
        workdir or None,
        spec_name,
    )


def cli_post_action(argv=None):
    """CLI: validate todo.json and trigger post-action hook."""

    args = _build_parser().parse(["post-action"] + (argv or []))
    _do_post_action(args)


def _build_parser():
    """Build the top-level parser with subcommand sub-parsers."""
    parser = ArgumentParser(
        prog="spex create-helper",
        description="Helper utilities for spec creation.",
    )
    subs = parser.add_subparsers(dest="subcmd", title="Subcommands")

    subs.add_parser(
        "precheck",
        description="Validate branch creation feasibility.",
        help="Validate branch creation feasibility",
    )

    subs.add_parser(
        "begin-session",
        description=(
            "Create or reuse an active create debug session."
        ),
        help="Create or reuse an active create debug session",
    )

    p_end = subs.add_parser(
        "end-session",
        description=(
            "Clear active create session; optionally merge into spec."
        ),
        help="Clear active create session; optionally merge into spec",
    )
    p_end.add_argument(
        "--name", default=None, help="Spec name to merge session log into",
    )
    p_end.add_argument(
        "--spec-path", default=None,
        help="Spec directory path to merge session log into",
    )

    p_prepare = subs.add_parser(
        "prepare-spec",
        description=(
            "Create spec directory and return JSON metadata."
        ),
        help="Create spec directory and return JSON metadata",
    )
    p_prepare.add_argument(
        "--name", required=True, help="Spec name",
    )
    p_prepare.add_argument(
        "--description", default="",
        help="Brief description (saved to meta.json)",
    )

    p_post = subs.add_parser(
        "post-action",
        description=(
            "Validate todo.json and run post-action hook."
        ),
        help="Validate todo.json and run post-action hook",
    )
    p_post.add_argument(
        "--name", required=True, help="Spec name",
    )
    p_post.add_argument(
        "--event-type", default="create",
        help="Hook event type (default: create)",
    )

    return parser


def main(argv=None):
    """Parse args, route to subcommand."""

    parser = _build_parser()
    args = parser.parse(argv)

    if not args.subcmd:
        parser.print_help(sys.stderr)
        sys.exit(2)

    if args.subcmd == "precheck":
        cli_create_validate()
    elif args.subcmd == "begin-session":
        _do_begin_session(args)
    elif args.subcmd == "end-session":
        _do_end_session(args)
    elif args.subcmd == "prepare-spec":
        _do_prepare_spec(args)
    elif args.subcmd == "post-action":
        _do_post_action(args)
