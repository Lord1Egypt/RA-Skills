"""Submit/merge CLI logic for spex."""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys

from cli import ArgumentParser
from common import logger


def _build_submit_parser() -> ArgumentParser:
    """Build the argument parser for ``spex submit``."""
    parser = ArgumentParser(
        prog="spex submit",
        description="Submit (merge) a spex branch back to the target branch.",
    )
    parser.add_argument(
        "name",
        nargs="?",
        default="",
        help="Spec name to submit",
    )
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="Skip automatic archiving after successful merge",
    )
    parser.add_argument(
        "-n", "--dry-run",
        action="store_true",
        help="Preview merge without executing",
    )
    return parser


def _find_submittable_specs(ctx):
    """Find specs ready to submit: all tasks done + has spex_branch."""
    import common
    from common import Spec, find_completed_specs

    specs_dir = common.get_specs_dir()
    completed = find_completed_specs(specs_dir, ctx, force=True)
    results = []
    for d in completed:
        meta = common.load_meta(d)
        if meta and meta.spex_branch:
            spec = Spec.from_dir(d)
            if spec is not None:
                results.append(spec)
    return results


def cli_submit(argv=None, command="submit") -> None:
    """CLI: submit (merge) a spex branch back to target. Output JSON."""
    import common
    import config as cfg
    import hooks
    from branch import branch_exists, create_and_switch_branch, merge_branch, resolve_default_branch

    parser = _build_submit_parser()
    parsed = parser.parse(argv)
    spec_name = parsed.name

    ctx = cfg.get_project_context()
    conf = ctx.config

    if not spec_name:
        candidates = _find_submittable_specs(ctx)
        if not candidates:
            logger.error("No submittable specs found.")
            sys.exit(1)
        elif len(candidates) == 1:
            spec_dir = candidates[0].path
            spec_name = candidates[0].name
            logger.error("Auto-selected: %s", spec_name)
        else:
            from common import prompt_selection

            selected = prompt_selection(candidates)
            spec_dir = selected.path
            spec_name = selected.name
    else:
        spec_dir = common.resolve_spec_dir(spec_name)
        spec_name = spec_dir.name if spec_dir else spec_name

    if not ctx.is_related_to(spec_dir):
        meta = common.load_meta(spec_dir)
        workdir = meta.workdir if meta else "(unknown)"
        logger.error(
            "Error: spec '%s' is not related to current project, "
            "it is associated with %s", spec_name, workdir
        )
        sys.exit(1)
    meta = common.load_meta(spec_dir)
    source = meta.spex_branch if meta else ""
    target = meta.branch if (meta and meta.branch) else None
    if target is None:
        target = resolve_default_branch(cwd=ctx.main_worktree)
    method = conf["submit_method"]
    errors: list[str] = []

    if not source:
        errors.append("No spex_branch in spec meta.json")
        print(json.dumps({"action": method, "source": "", "target": target,
                          "errors": errors}))
        sys.exit(1)

    # Run pre-action hook before merge
    done, total = common.get_todo_progress(spec_dir)
    hooks.run_pre_action(
        command,
        {
            "source_branch": source,
            "target_branch": target,
            "done": done,
            "undone": total - done,
        },
        workdir=ctx.top_workdir,
        spec_name=spec_dir.name,
    )

    if parsed.dry_run:
        logger.info("Would merge: %s -> %s", source, target)
        if not parsed.no_archive:
            logger.info("Would archive: %s", spec_dir.name)
        print(json.dumps({"action": method, "source": source,
                          "target": target, "archived": not parsed.no_archive,
                          "dry_run": True, "errors": []}))
        return

    # If target branch doesn't exist, create it from the current branch
    if not branch_exists(target, cwd=ctx.main_worktree):
        logger.warning(
            "Warning: target branch '%s' does not exist. "
            "Creating from '%s'.", target, source,
        )
        try:
            create_and_switch_branch(target, cwd=ctx.main_worktree)
        except subprocess.CalledProcessError as e:
            errors.append(
                f"Failed to create target branch '{target}': "
                f"{e.stderr.strip() or str(e)}"
            )
            print(json.dumps({"action": method, "source": source,
                              "target": target, "errors": errors}))
            sys.exit(1)

    if method == "merge":
        try:
            merge_branch(target, source, cwd=ctx.main_worktree)
        except subprocess.CalledProcessError as e:
            errors.append(f"Merge failed: {e.stderr.strip() or str(e)}")
            print(json.dumps({"action": method, "source": source,
                              "target": target, "errors": errors}))
            sys.exit(1)
    else:
        errors.append(f"submit method '{method}' is not implemented")
        print(json.dumps({"action": method, "source": source,
                          "target": target, "errors": errors}))
        sys.exit(1)

    # Run post-action hook on success
    done, total = common.get_todo_progress(spec_dir)
    workdir = ctx.top_workdir
    hooks.run_post_action(
        command,
        {
            "source_branch": source,
            "target_branch": target,
            "action": method,
            "done": done,
            "undone": total - done,
        },
        workdir,
        spec_name,
    )

    # Auto-archive the spec unless --no-archive is set
    archived = False
    if not parsed.no_archive:
        try:
            import archive as archive_mod

            with contextlib.redirect_stdout(io.StringIO()):
                result = archive_mod.archive_single_spec(
                    spec_name,
                    common.get_specs_dir(),
                    common.get_archives_dir(),
                    force=True,
                )
            archived = result is not None
        except Exception:
            archived = False

    print(json.dumps({"action": method, "source": source,
                      "target": target, "archived": archived,
                      "errors": errors}))
