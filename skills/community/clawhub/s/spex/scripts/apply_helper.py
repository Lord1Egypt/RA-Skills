"""Helper utilities for applying specs."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from cli import ArgumentParser
from common import (
    DEFAULT_SPEX_BRANCH_PREFIX,
    SpecMeta,
    logger,
    strip_date_prefix,
)


def _extract_spec_name_for_branch(spec_dir: Path, meta) -> str:
    """Get the spec name to use for branch naming."""
    return meta.name or spec_dir.name


def validate_apply_branch(
    config: dict, spec_dir: Path, cwd: str | Path | None = None,
) -> None:
    """Perform branch setup for applying a spec.

    Steps:
    1. If all spec tasks are completed, error and exit.
    2. If branch_management is False in config, return immediately.
    3. If meta.json has spex_branch, ensure current branch matches it;
       switch if not (exit on failure).
    4. If meta.json has no spex_branch, try creating a branch using
       spex/<spec-name-without-date-prefix>, then spex/<spec-name-with-date-prefix>.
       Exit on failure if both fail.
    5. On success, switch to the branch, set git branch description from
       the spec's description, and persist spex_branch to meta.json.
    """
    import common
    from branch import (
        branch_exists,
        create_and_switch_branch,
        get_current_branch,
        set_branch_description,
        switch_branch,
    )

    if common.is_spec_completed(spec_dir):
        status = common.format_spec(spec_dir, verbose=2)
        logger.error(f"Error: spec is already completed.\n{status}")
        sys.exit(1)

    if not bool(config["branch_management"]):
        return

    meta = common.load_meta(spec_dir) or SpecMeta()
    spex_branch = meta.spex_branch

    if spex_branch:
        current = get_current_branch(cwd)
        if current != spex_branch:
            if not branch_exists(spex_branch, cwd):
                logger.error(
                    f"Error: spex_branch '{spex_branch}' defined in meta.json "
                    f"does not exist.",
                )
                sys.exit(1)
            try:
                switch_branch(spex_branch, cwd)
            except subprocess.CalledProcessError as e:
                logger.error(
                    f"Error: failed to switch to '{spex_branch}': "
                    f"{e.stderr.strip() or e}",
                )
                sys.exit(1)
            logger.info(f"Switched to branch '{spex_branch}'.")
        return

    spec_name = _extract_spec_name_for_branch(spec_dir, meta)
    short_name = strip_date_prefix(spec_name)

    candidates = [
        f"{DEFAULT_SPEX_BRANCH_PREFIX}{short_name}",
        f"{DEFAULT_SPEX_BRANCH_PREFIX}{spec_name}",
    ]

    created_branch = None
    for candidate in candidates:
        if branch_exists(candidate, cwd):
            created_branch = candidate
            break
        try:
            create_and_switch_branch(candidate, cwd)
            created_branch = candidate
            break
        except subprocess.CalledProcessError:
            continue

    if created_branch is None:
        logger.error(
            f"Error: failed to create branch. Tried: {', '.join(candidates)}",
        )
        sys.exit(1)

    # create_and_switch_branch already uses `git switch -c` which switches to the new
    # branch, so no separate switch_branch call is needed here.

    description = common.get_spec_description(spec_dir)
    if description:
        try:
            set_branch_description(created_branch, description, cwd)
        except subprocess.CalledProcessError:
            pass

    meta_path = spec_dir / "meta.json"
    meta.spex_branch = created_branch
    common.atomic_write_json(meta_path, meta.to_dict())

    logger.info(f"Created and switched to branch '{created_branch}'.")


def _do_precheck(args):
    """Perform branch setup for applying a spec."""
    import common
    import config as cfg
    import hooks

    ctx = cfg.get_project_context()
    spec_dir = common.resolve_spec_dir(args.name)
    validate_apply_branch(ctx.config, spec_dir, cwd=ctx.top_workdir)

    meta = common.load_meta(spec_dir) or SpecMeta()
    hooks.run_pre_action(
        "apply",
        {
            "source_branch": meta.spex_branch or "",
            "target_branch": meta.branch or "main",
        },
        workdir=ctx.top_workdir,
        spec_name=spec_dir.name,
    )


def cli_precheck(argv=None):
    """CLI: perform branch setup for applying a spec."""

    args = _build_parser().parse(["precheck"] + (argv or []))
    _do_precheck(args)


def _do_post_action(args):
    """Run post-action hook, and show hint."""
    import common
    import config as cfg
    import hooks
    from debug_log import emit_apply_anchor

    spec_dir = common.resolve_spec_dir(args.name)
    spec_name = spec_dir.name
    meta = common.load_meta(spec_dir)
    spex_branch = meta.spex_branch if meta else ""
    if not spex_branch:
        return

    target = meta.branch or "main"
    ctx = cfg.get_project_context()
    workdir = ctx.top_workdir

    hooks.run_post_action(
        "apply",
        {
            "source_branch": spex_branch,
            "target_branch": target,
        },
        workdir,
        spec_name,
    )

    emit_apply_anchor(spec_dir, "===== APPLY post-action ok =====")

    if hooks.find_hook("post-action", workdir) is None:
        logger.info(
            f"Development completed on spec branch {spex_branch}.\n"
            f"After local code review, run /spex merge to merge into\n"
            f"branch {target}, or create a pull request."
        )


def cli_post_action(argv=None):
    """CLI: run post-action hook, and show hint."""

    args = _build_parser().parse(["post-action"] + (argv or []))
    _do_post_action(args)


def _build_parser():
    """Build the top-level parser with subcommand sub-parsers."""
    parser = ArgumentParser(
        prog="spex apply-helper",
        description="Helper utilities for applying specs.",
    )
    subs = parser.add_subparsers(dest="subcmd", title="Subcommands")

    p_precheck = subs.add_parser(
        "precheck",
        description=(
            "Validate branch setup for applying a spec."
        ),
        help="Validate branch setup for applying a spec",
    )
    p_precheck.add_argument(
        "--name", required=True, help="Spec name",
    )

    p_post = subs.add_parser(
        "post-action",
        description="Run post-action hook and show hint.",
        help="Run post-action hook and show hint",
    )
    p_post.add_argument(
        "--name", required=True, help="Spec name",
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
        _do_precheck(args)
    elif args.subcmd == "post-action":
        _do_post_action(args)
