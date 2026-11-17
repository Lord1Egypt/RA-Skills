#!/usr/bin/env python3
"""Render a Jinja2 template with metadata and output the result."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from cli import ArgumentParser
from common import (
    atomic_write_json,
    get_spex_root,
    get_template,
    load_meta,
    load_todo,
    local_iso_timestamp,
    logger,
    resolve_spec_dir,
    strip_front_matter,
)
from common import filter_completed_todos as _filter_completed_todos
from config import get_project_context


def validate_required_meta(content, metadata):
    """Check that all keys listed in front-matter 'required' are present in metadata."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return

    front_matter = match.group(1)
    required = []
    in_required = False
    for line in front_matter.splitlines():
        if re.match(r"required:\s*$", line):
            in_required = True
            continue
        if in_required:
            # Match YAML list item format: "  - item_name"
            m = re.match(r"\s+-\s+(.+)", line)
            if m:
                required.append(m.group(1).strip().strip("\"'"))
            else:
                break

    missing = [key for key in required if key not in metadata]
    if missing:
        logger.error(
            "Error: missing required metadata: %s", ", ".join(missing)
        )
        sys.exit(1)


def _format_item_verbose(item):
    """Format a single todo item in verbose markdown style."""
    task_id = item.get("id", "")
    name = item.get("name", "")
    details = item.get("details", "")
    lines = [f"- **{task_id}**: {name}"]
    if details:
        for line in details.splitlines():
            lines.append(f"  {line}" if line else "")
    return "\n".join(lines)


def _format_item_brief(item):
    """Format a single todo item as a brief one-liner."""
    return f"- {item.get('id', '')}: {item.get('name', '')} *(details omitted)*"


def _format_item_concise(item):
    """Format a single todo item as a concise one-liner (id + name only)."""
    return f"- **{item.get('id', '')}**: {item.get('name', '')}"


def _trim_spec_content(spec_content):
    """Trim spec content for commit context using include/exclude strategy.

    Include (primary): if requirement or user-clarification sections exist,
    keep only those. Exclude (fallback): otherwise drop detailed-design,
    test-plan, constraints and keep the rest.
    """
    if not spec_content:
        return ""

    from common import parse_front_matter_description, strip_front_matter

    description = parse_front_matter_description(spec_content)

    include_sections = {"requirement", "user-clarification"}
    exclude_sections = {"detailed-design", "test-plan", "constraints"}
    marker_pattern = re.compile(r"<!--\s*spex:begin:([a-z-]+)\s*-->")

    markers = list(marker_pattern.finditer(spec_content))
    if markers:
        parsed = []
        for i, m in enumerate(markers):
            name = m.group(1)
            start = m.end()
            end = markers[i + 1].start() if i + 1 < len(markers) else len(
                spec_content
            )
            parsed.append((name, spec_content[start:end].strip()))

        found_include = any(n in include_sections for n, _ in parsed)
        if found_include:
            seen = set()
            kept = []
            for name, content in parsed:
                if name in include_sections and name not in seen:
                    seen.add(name)
                    kept.append(content)
        else:
            kept = [c for n, c in parsed if n not in exclude_sections]
    else:
        body = strip_front_matter(spec_content)
        heading_pattern = re.compile(r"^(# .+)", re.MULTILINE)
        splits = heading_pattern.split(body)

        include_headings = {"# Requirement", "# User Clarification"}
        exclude_headings = {"# Detailed Design", "# Test Plan",
                            "# Constraints"}

        all_sections = []
        i = 1
        while i < len(splits):
            heading = splits[i].strip()
            content = splits[i + 1] if i + 1 < len(splits) else ""
            all_sections.append((heading, heading + content.rstrip()))
            i += 2

        found_include = any(h in include_headings for h, _ in all_sections)
        if found_include:
            seen = set()
            kept = []
            for h, s in all_sections:
                if h in include_headings and h not in seen:
                    seen.add(h)
                    kept.append(s)
        else:
            kept = [s for h, s in all_sections if h not in exclude_headings]

    parts = []
    if description:
        parts.append(description)
    if kept:
        parts.append("\n\n".join(kept))
    return "\n\n".join(parts)


def _build_task_context(spec_dir, verbose_items=20):
    """Extract task context from a spec directory.

    Reads spec.md and todo.json, computes completed/current/future task info.

    Args:
        spec_dir: Path to the spec directory.
        verbose_items: Max number of items to show with full details.
            Items beyond this limit are shown in brief format.

    Returns:
        Dict with keys: spec_content, completed_tasks, current_task_id,
        current_task_description, future_tasks.
    """
    spec_path = spec_dir / "spec.md"
    if spec_path.exists():
        spec_content = spec_path.read_text(encoding="utf-8")
    else:
        spec_content = ""
    spec_content_concise = _trim_spec_content(spec_content)

    todo = load_todo(spec_dir)
    if todo:
        done = [item for item in todo if item.get("completed_at")]
        if len(done) <= verbose_items:
            completed_tasks = "\n\n".join(
                _format_item_verbose(item) for item in done
            )
        else:
            brief_items = done[:-verbose_items]
            verbose_part = done[-verbose_items:]
            parts = [_format_item_brief(item) for item in brief_items]
            parts.extend(_format_item_verbose(item) for item in verbose_part)
            completed_tasks = "\n\n".join(parts)
        completed_tasks_concise = "\n".join(
            _format_item_concise(item) for item in done
        )

        undone = [item for item in todo if not item.get("completed_at")]
        if undone:
            current = undone[0]
            task_id = current.get("id", "")
            current_task_id = task_id
            current_task_description = _format_item_verbose(current)
            current_commit_title = current.get("commit_title") or ""
            # commit_title set but completed_at empty → resume at review
            resume_phase = (
                "review" if current_commit_title.strip() else "implement"
            )

            future = undone[1:]
            if future:
                if len(future) <= verbose_items:
                    future_tasks = "\n\n".join(
                        _format_item_verbose(item) for item in future
                    )
                else:
                    verbose_part = future[:verbose_items]
                    brief_items = future[verbose_items:]
                    parts = [
                        _format_item_verbose(item) for item in verbose_part
                    ]
                    parts.extend(
                        _format_item_brief(item) for item in brief_items
                    )
                    future_tasks = "\n\n".join(parts)
                future_tasks_concise = "\n".join(
                    _format_item_concise(item) for item in future
                )
            else:
                future_tasks = ""
                future_tasks_concise = ""
        else:
            current_task_id = ""
            current_task_description = ""
            current_commit_title = ""
            resume_phase = "implement"
            future_tasks = ""
            future_tasks_concise = ""
    else:
        completed_tasks = ""
        completed_tasks_concise = ""
        current_task_id = ""
        current_task_description = ""
        current_commit_title = ""
        resume_phase = "implement"
        future_tasks = ""
        future_tasks_concise = ""

    return {
        "spec_content": spec_content,
        "spec_content_concise": spec_content_concise,
        "completed_tasks": completed_tasks,
        "completed_tasks_concise": completed_tasks_concise,
        "current_task_id": current_task_id,
        "current_task_description": current_task_description,
        "current_commit_title": current_commit_title,
        "resume_phase": resume_phase,
        "future_tasks": future_tasks,
        "future_tasks_concise": future_tasks_concise,
    }



def _build_metadata(template_name, spec_name=None):
    """Build the metadata dict for template rendering.

    Different template names may produce different metadata.
    """
    metadata = {}
    if spec_name:
        spec_dir = resolve_spec_dir(spec_name)
        metadata["spec_name"] = spec_dir.name
        meta = load_meta(spec_dir)
        if meta:
            metadata.update(meta.to_dict())
    if not metadata:
        ctx = get_project_context()
        metadata["workdir"] = str(ctx.top_workdir) if ctx.in_git_workdir() else ""
        metadata["remote_url"] = ctx.remote_url
        metadata["branch"] = ctx.branch
        metadata["user_name"] = ctx.user_name
        metadata["user_email"] = ctx.user_email
        if ctx.main_worktree:
            metadata["main_worktree"] = ctx.main_worktree
        metadata["created_at"] = local_iso_timestamp()
        metadata["name"] = ""

    if template_name in ("apply-commit", "apply-review", "apply-fix"):
        metadata["spex_root"] = ""
        workdir = metadata.get("workdir", "")
        if workdir:
            try:
                spex_root = get_spex_root()
                rel = os.path.relpath(spex_root, workdir)
                if not rel.startswith(".."):
                    metadata["spex_root"] = rel
            except (ValueError, RuntimeError):
                pass
        ctx = get_project_context()
        if (metadata.get("user_name") == ctx.user_name
                and metadata.get("user_email") == ctx.user_email):
            metadata["user_name"] = ""
            metadata["user_email"] = ""
    # All spec-based templates except spec-template need task context:
    # apply-commit, apply-one-task, apply-review, apply-fix,
    # modify-spec, modify-todo
    if template_name != "spec-template" and spec_name:
        metadata.update(_build_task_context(spec_dir))

    return metadata


def _enrich_review_metadata(
    metadata, spec_name, commit_sha=None, finding_id=None,
):
    """Add review-loop fields from review-step-N.json and CLI args."""
    import review_helper

    metadata["spex_skill_dir"] = str(Path(__file__).resolve().parent.parent)
    step_id = metadata.get("current_task_id") or ""
    metadata["step_id"] = step_id
    metadata["finding_id"] = finding_id or ""

    if not step_id or not spec_name:
        metadata.setdefault("commit_sha", commit_sha or "")
        metadata.setdefault("review_round", 1)
        metadata.setdefault("review_file", "")
        metadata.setdefault("open_findings", "(no open findings)")
        return metadata

    path = review_helper.resolve_review_path(spec_name, step_id)
    metadata["review_file"] = str(path)

    if path.is_file():
        data = review_helper.load_review(path)
        metadata["review_round"] = int(data.get("round", 1))
        metadata["commit_sha"] = (
            commit_sha or data.get("commit_sha") or ""
        )
        if finding_id:
            item = review_helper.get_finding_by_id(data, finding_id)
            if item is None:
                logger.error(
                    "Error: finding id '%s' not found in %s",
                    finding_id, path.name,
                )
                sys.exit(1)
            if item.get("completed_at"):
                logger.error(
                    "Error: finding id '%s' is already completed",
                    finding_id,
                )
                sys.exit(1)
            metadata["open_findings"] = (
                review_helper._format_finding_markdown(item)
            )
            metadata["finding_id"] = finding_id
        else:
            metadata["open_findings"] = (
                review_helper._format_open_findings_markdown(
                    data.get("findings", []),
                )
            )
    else:
        metadata["review_round"] = 1
        metadata["commit_sha"] = commit_sha or ""
        metadata["open_findings"] = "(no open findings)"

    if commit_sha:
        metadata["commit_sha"] = commit_sha

    return metadata


def render_prompt(name, spec_name=None, extra_vars=None, metadata=None):
    """Render a template by name and return the result string.

    Args:
        name: Template name without .md extension (e.g. "spec-template").
        spec_name: Optional spec name for spec-specific metadata.
        extra_vars: Optional dict of additional variables to merge into metadata.
        metadata: Optional pre-built metadata dict. Skips _build_metadata when provided.

    Returns:
        Rendered template content with front-matter stripped.
    """
    from jinja2 import Template

    content = get_template(name + ".md")
    if metadata is None:
        metadata = _build_metadata(name, spec_name)
        if extra_vars:
            metadata.update(extra_vars)

    # All-done detection for task-based templates
    if name in (
        "apply-one-task", "apply-commit", "apply-review", "apply-fix",
    ) and not metadata.get("current_task_description"):
        return ""

    validate_required_meta(content, metadata)
    rendered = Template(content).render(**metadata)
    return strip_front_matter(rendered)


def _output_rendered(rendered, output_path):
    """Write rendered content to file or stdout."""
    if output_path:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)


def _build_parser():
    """Build the top-level parser with subcommand sub-parsers."""
    parser = ArgumentParser(
        prog="spex prompt",
        description="Render Jinja2 templates with metadata.",
    )
    subs = parser.add_subparsers(dest="subcmd", title="Subcommands")

    # apply-one-task
    p = subs.add_parser(
        "apply-one-task",
        description="Render apply-one-task template with spec metadata.",
        help="Render prompt for the next undone task",
    )
    p.add_argument(
        "--name", required=True, help="Spec name (required)",
    )
    p.add_argument(
        "--json", action="store_true", dest="json_mode",
        help="Output JSON with task_id and prompt",
    )
    p.add_argument(
        "-o", "--output", help="Output file path (default: stdout)",
    )

    # apply-commit
    p = subs.add_parser(
        "apply-commit",
        description="Render apply-commit template with spec metadata.",
        help="Render commit instructions for the current task",
    )
    p.add_argument("--name", help="Spec name")
    p.add_argument(
        "--stdin", action="store_true", dest="stdin_flag",
        help="Read raw text from stdin as prompt_context",
    )
    p.add_argument(
        "-o", "--output", help="Output file path (default: stdout)",
    )

    # apply-review
    p = subs.add_parser(
        "apply-review",
        description="Render apply-review template with spec metadata.",
        help="Render review instructions for the current task commit",
    )
    p.add_argument("--name", required=True, help="Spec name (required)")
    p.add_argument(
        "--commit", dest="commit_sha", default=None,
        help="Commit SHA under review (default: from review file)",
    )
    p.add_argument(
        "--json", action="store_true", dest="json_mode",
        help="Output JSON with prompt and review metadata",
    )
    p.add_argument(
        "-o", "--output", help="Output file path (default: stdout)",
    )

    # apply-fix
    p = subs.add_parser(
        "apply-fix",
        description=(
            "Render apply-fix template for a single open finding."
        ),
        help="Render fix instructions for one review finding",
    )
    p.add_argument("--name", required=True, help="Spec name (required)")
    p.add_argument(
        "--finding-id", required=True, dest="finding_id",
        help="Single open finding id to fix (required)",
    )
    p.add_argument(
        "--commit", dest="commit_sha", default=None,
        help="Commit SHA under fix (default: from review file)",
    )
    p.add_argument(
        "--json", action="store_true", dest="json_mode",
        help="Output JSON with prompt and review metadata",
    )
    p.add_argument(
        "-o", "--output", help="Output file path (default: stdout)",
    )

    # modify-spec
    p = subs.add_parser(
        "modify-spec",
        description="Render modify-spec template with spec metadata.",
        help="Render prompt for modifying a spec",
    )
    p.add_argument(
        "--name", required=True, help="Spec name (required)",
    )
    p.add_argument(
        "--stdin", action="store_true", dest="stdin_flag",
        help="Read raw text from stdin as prompt_context",
    )
    p.add_argument(
        "--remove-undone", action="store_true", dest="remove_undone",
        help="Remove undone tasks from todo.json before rendering",
    )
    p.add_argument(
        "--json", action="store_true", dest="json_mode",
        help="Output JSON with rendered prompt",
    )
    p.add_argument(
        "-o", "--output", help="Output file path (default: stdout)",
    )

    # modify-todo
    p = subs.add_parser(
        "modify-todo",
        description="Render modify-todo template with spec metadata.",
        help="Render prompt for modifying a todo list",
    )
    p.add_argument(
        "--name", required=True, help="Spec name (required)",
    )
    p.add_argument(
        "--stdin", action="store_true", dest="stdin_flag",
        help="Read raw text from stdin as prompt_context",
    )
    p.add_argument(
        "--json", action="store_true", dest="json_mode",
        help="Output JSON with rendered prompt",
    )
    p.add_argument(
        "-o", "--output", help="Output file path (default: stdout)",
    )

    return parser


# Known subcommands for routing (fallback to cli_render for others)
_KNOWN_SUBCMDS = {
    "apply-one-task", "apply-commit", "apply-review", "apply-fix",
    "modify-spec", "modify-todo",
}


def _do_apply_one_task(args):
    """Handle apply-one-task subcommand."""
    import json

    from jinja2 import TemplateError

    try:
        metadata = _build_metadata("apply-one-task", args.name)

        # Handle all-done in JSON mode
        if args.json_mode and not metadata.get("current_task_description"):
            print(json.dumps({
                "task_id": "",
                "prompt": "",
                "all_done": True,
                "resume_phase": "",
                "commit_title": "",
            }))
            sys.exit(0)

        # Handle all-done in non-JSON mode: exit(0) with empty stdout
        if not args.json_mode and not metadata.get("current_task_description"):
            sys.exit(0)

        # Emit task_id to stderr for orchestrator to capture (non-JSON only)
        if not args.json_mode:
            current_task_id = metadata.get("current_task_id", "")
            if current_task_id:
                print(f"task_id={current_task_id}", file=sys.stderr)

        rendered = render_prompt("apply-one-task", args.name, metadata=metadata)
    except FileNotFoundError as e:
        logger.error("Error: %s", e)
        sys.exit(1)
    except TemplateError as e:
        logger.error("Error rendering template: %s", e)
        sys.exit(1)

    task_id = metadata.get("current_task_id", "")
    if task_id and args.name:
        from debug_log import emit_apply_anchor

        emit_apply_anchor(
            resolve_spec_dir(args.name),
            f"===== APPLY task begin id={task_id} =====",
        )

    if args.json_mode:
        print(json.dumps({
            "task_id": metadata.get("current_task_id", ""),
            "prompt": rendered,
            "resume_phase": metadata.get("resume_phase", "implement"),
            "commit_title": metadata.get("current_commit_title", ""),
        }))
    else:
        _output_rendered(rendered, args.output)


def cli_apply_one_task(argv=None):
    """CLI handler for apply-one-task subcommand."""
    args = _build_parser().parse(["apply-one-task"] + (argv or []))
    _do_apply_one_task(args)


def _read_stdin_extra_vars(stdin_flag):
    """Read extra variables from stdin (JSON or raw text with --stdin flag)."""
    import json

    if sys.stdin.isatty():
        return None
    stdin_data = sys.stdin.read().strip()
    if not stdin_data:
        return None
    if stdin_flag:
        return {"prompt_context": stdin_data}
    try:
        return json.loads(stdin_data)
    except json.JSONDecodeError:
        logger.error("Error: stdin must be valid JSON")
        sys.exit(1)


def _do_apply_commit(args):
    """Handle apply-commit subcommand."""
    from jinja2 import TemplateError

    extra_vars = _read_stdin_extra_vars(args.stdin_flag)

    try:
        metadata = _build_metadata("apply-commit", args.name)
        if extra_vars:
            metadata.update(extra_vars)

        # Handle all-done: exit(0) with empty stdout
        if not metadata.get("current_task_description"):
            sys.exit(0)

        rendered = render_prompt("apply-commit", args.name, metadata=metadata)
    except FileNotFoundError as e:
        logger.error("Error: %s", e)
        sys.exit(1)
    except TemplateError as e:
        logger.error("Error rendering template: %s", e)
        sys.exit(1)

    _output_rendered(rendered, args.output)


def cli_apply_commit(argv=None):
    """CLI handler for apply-commit subcommand."""
    args = _build_parser().parse(["apply-commit"] + (argv or []))
    _do_apply_commit(args)


def _do_apply_review(args):
    """Handle apply-review subcommand."""
    import json

    from jinja2 import TemplateError

    try:
        metadata = _build_metadata("apply-review", args.name)
        if not metadata.get("current_task_description"):
            if args.json_mode:
                print(json.dumps({
                    "prompt": "", "all_done": True,
                }))
            sys.exit(0)

        _enrich_review_metadata(
            metadata, args.name, commit_sha=args.commit_sha,
        )
        if not metadata.get("commit_sha"):
            logger.error(
                "Error: --commit is required when no review file exists",
            )
            sys.exit(1)

        rendered = render_prompt(
            "apply-review", args.name, metadata=metadata,
        )
    except FileNotFoundError as e:
        logger.error("Error: %s", e)
        sys.exit(1)
    except TemplateError as e:
        logger.error("Error rendering template: %s", e)
        sys.exit(1)

    if args.name:
        from debug_log import emit_apply_anchor

        emit_apply_anchor(
            resolve_spec_dir(args.name),
            "===== APPLY review begin "
            f"round={metadata.get('review_round', 1)} "
            f"commit={metadata.get('commit_sha', '')} =====",
        )

    if args.json_mode:
        print(json.dumps({
            "prompt": rendered,
            "task_id": metadata.get("step_id", ""),
            "commit_sha": metadata.get("commit_sha", ""),
            "review_round": metadata.get("review_round", 1),
            "review_file": metadata.get("review_file", ""),
        }))
    else:
        _output_rendered(rendered, args.output)


def cli_apply_review(argv=None):
    """CLI handler for apply-review subcommand."""
    args = _build_parser().parse(["apply-review"] + (argv or []))
    _do_apply_review(args)


def _do_apply_fix(args):
    """Handle apply-fix subcommand."""
    import json

    from jinja2 import TemplateError

    try:
        metadata = _build_metadata("apply-fix", args.name)
        if not metadata.get("current_task_description"):
            if args.json_mode:
                print(json.dumps({
                    "prompt": "", "all_done": True,
                }))
            sys.exit(0)

        _enrich_review_metadata(
            metadata, args.name,
            commit_sha=args.commit_sha,
            finding_id=args.finding_id,
        )
        if not metadata.get("commit_sha"):
            logger.error(
                "Error: --commit is required when no review file exists",
            )
            sys.exit(1)

        rendered = render_prompt(
            "apply-fix", args.name, metadata=metadata,
        )
    except FileNotFoundError as e:
        logger.error("Error: %s", e)
        sys.exit(1)
    except TemplateError as e:
        logger.error("Error rendering template: %s", e)
        sys.exit(1)

    if args.json_mode:
        print(json.dumps({
            "prompt": rendered,
            "task_id": metadata.get("step_id", ""),
            "finding_id": metadata.get("finding_id", ""),
            "commit_sha": metadata.get("commit_sha", ""),
            "review_round": metadata.get("review_round", 1),
            "review_file": metadata.get("review_file", ""),
        }))
    else:
        _output_rendered(rendered, args.output)


def cli_apply_fix(argv=None):
    """CLI handler for apply-fix subcommand."""
    args = _build_parser().parse(["apply-fix"] + (argv or []))
    _do_apply_fix(args)


def _do_modify_spec(args):
    """Handle modify-spec subcommand."""
    import json

    from jinja2 import TemplateError

    extra_vars = _read_stdin_extra_vars(args.stdin_flag)

    try:
        # Side-effect: remove undone tasks from todo.json before building metadata
        if args.remove_undone:
            spec_dir = resolve_spec_dir(args.name)
            todo_path = spec_dir / "todo.json"
            if todo_path.exists():
                try:
                    data = json.loads(todo_path.read_text(encoding="utf-8"))
                    if isinstance(data, list):
                        completed = _filter_completed_todos(data)
                        atomic_write_json(todo_path, completed)
                except json.JSONDecodeError:
                    pass  # Silently skip if JSON is invalid

        metadata = _build_metadata("modify-spec", args.name)
        if extra_vars:
            metadata.update(extra_vars)

        rendered = render_prompt("modify-spec", args.name, metadata=metadata)
    except FileNotFoundError as e:
        logger.error("Error: %s", e)
        sys.exit(1)
    except TemplateError as e:
        logger.error("Error rendering template: %s", e)
        sys.exit(1)

    if args.json_mode:
        print(json.dumps({"prompt": rendered}))
    else:
        _output_rendered(rendered, args.output)


def cli_modify_spec(argv=None):
    """CLI handler for modify-spec subcommand."""
    args = _build_parser().parse(["modify-spec"] + (argv or []))
    _do_modify_spec(args)


def _do_modify_todo(args):
    """Handle modify-todo subcommand."""
    import json

    from jinja2 import TemplateError

    extra_vars = _read_stdin_extra_vars(args.stdin_flag)

    try:
        metadata = _build_metadata("modify-todo", args.name)
        if extra_vars:
            metadata.update(extra_vars)

        # Side-effect: clean undone todos from todo.json
        spec_dir = resolve_spec_dir(args.name)
        todo_path = spec_dir / "todo.json"
        if todo_path.exists():
            try:
                data = json.loads(todo_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    completed = _filter_completed_todos(data)
                    atomic_write_json(todo_path, completed)
            except json.JSONDecodeError:
                pass  # Silently skip if JSON is invalid

        rendered = render_prompt("modify-todo", args.name, metadata=metadata)
    except FileNotFoundError as e:
        logger.error("Error: %s", e)
        sys.exit(1)
    except TemplateError as e:
        logger.error("Error rendering template: %s", e)
        sys.exit(1)

    if args.json_mode:
        print(json.dumps({"prompt": rendered}))
    else:
        _output_rendered(rendered, args.output)


def cli_modify_todo(argv=None):
    """CLI handler for modify-todo subcommand."""
    args = _build_parser().parse(["modify-todo"] + (argv or []))
    _do_modify_todo(args)


def cli_render(argv):
    """Fallback CLI handler for generic template rendering."""
    from jinja2 import TemplateError

    parser = ArgumentParser(
        prog="spex prompt",
        description="Render a Jinja2 template with metadata.",
    )
    parser.add_argument("name", help="Template name (without .md extension)")
    parser.add_argument("--name", help="Spec name for spec-specific metadata")
    parser.add_argument("--stdin", action="store_true", dest="stdin_flag",
                        help="Read raw text from stdin as prompt_context")
    parser.add_argument("-o", "--output",
                        help="Output file path (default: stdout)")
    args = parser.parse(argv)

    extra_vars = _read_stdin_extra_vars(args.stdin_flag)

    try:
        metadata = _build_metadata(args.name, args.name)
        if extra_vars:
            metadata.update(extra_vars)

        rendered = render_prompt(args.name, args.name, metadata=metadata)
    except FileNotFoundError as e:
        logger.error("Error: %s", e)
        sys.exit(1)
    except TemplateError as e:
        logger.error("Error rendering template: %s", e)
        sys.exit(1)

    _output_rendered(rendered, args.output)


def _normalize_subcmd(name):
    """Normalize subcommand/template name: underscores -> hyphens."""
    return name.replace("_", "-")


def main(argv=None):
    """Route prompt subcommands to their handlers."""
    if argv is None:
        argv = sys.argv[1:]

    parser = _build_parser()

    if not argv:
        parser.print_help(sys.stderr)
        sys.exit(2)

    first = argv[0]

    # Let argparse handle flags like --help / -h
    if first.startswith("-"):
        parser.parse(argv)
        return

    # Normalize: accept both underscores and hyphens
    subcmd = _normalize_subcmd(first)

    if subcmd not in _KNOWN_SUBCMDS:
        # Fallback to generic template rendering
        cli_render(argv)
        return

    # Ensure normalized name is used for argparse
    argv = [subcmd] + list(argv[1:])
    args = parser.parse(argv)

    if args.subcmd == "apply-one-task":
        _do_apply_one_task(args)
    elif args.subcmd == "apply-commit":
        _do_apply_commit(args)
    elif args.subcmd == "apply-review":
        _do_apply_review(args)
    elif args.subcmd == "apply-fix":
        _do_apply_fix(args)
    elif args.subcmd == "modify-spec":
        _do_modify_spec(args)
    elif args.subcmd == "modify-todo":
        _do_modify_todo(args)


if __name__ == "__main__":
    from common import setup_logging
    setup_logging()
    main()
