#!/usr/bin/env python3
"""Show detailed information about a single spec."""

from __future__ import annotations

import os
import subprocess
import sys

from cli import ArgumentParser
from common import (
    Spec,
    format_spec,
    resolve_spec,
    select_spec_interactive,
    strip_front_matter,
)


def _paged_output(text):
    """Output text through a pager if stdout is a tty."""
    if not sys.stdout.isatty():
        print(text)
        return
    pager = os.environ.get("PAGER", "less -R")
    try:
        proc = subprocess.Popen(pager, shell=True, stdin=subprocess.PIPE)
        proc.communicate(input=text.encode())
    except (BrokenPipeError, OSError):
        print(text)


def _format_default(spec_dir):
    """Format spec in list -vv style, reused from common."""
    return format_spec(spec_dir, verbose=2)


def _format_verbose(spec_dir):
    """Format spec with full content and structured todo."""
    t = Spec.from_dir(spec_dir)
    if t is None:
        return f"(unable to load spec: {spec_dir.name})"

    parts = []

    parts.append(f"{t.icon} ({t.done}/{t.total}) {t.name}")
    parts.append("")
    parts.append("# **Specification**")
    parts.append("")
    if t.spec_content is not None:
        parts.append(strip_front_matter(t.spec_content).rstrip())
    else:
        parts.append("(no spec.md found)")

    parts.append("")
    parts.append("----")
    parts.append("")
    parts.append("# **TODO**")
    parts.append("")

    todo = t.todo_data
    if todo:
        for item in todo:
            step_id = item.get("id", "")
            step_name = item.get("name", "")
            details = item.get("details", "")
            parts.append(f"- **{step_id}: {step_name}**")
            parts.append("")
            if details:
                for line in details.splitlines():
                    parts.append(f"  {line}" if line else "")
                parts.append("")
    else:
        parts.append("(no tasks)")

    return "\n".join(parts).rstrip()



def main(argv=None):
    parser = ArgumentParser(
        prog="spex show",
        description="Show detailed information about a spec.",
    )
    parser.add_argument("name", nargs="?", help="Spec name or substring")
    parser.add_argument("-l", "--list", action="store_true",
                        dest="brief",
                        help="Show brief list format instead of full details")
    parser.add_argument(
        "--archives",
        action="store_true",
        help="Include archived specs in search",
    )
    parser.add_argument(
        "--all-projects",
        action="store_true",
        help="Show specs from all projects (disables project filter)",
    )
    args = parser.parse(argv)

    if args.name:
        spec_dir = resolve_spec(args.name, include_archives=args.archives)
    else:
        spec_dir = select_spec_interactive(
            include_archives=args.archives,
            all_projects=args.all_projects,
        )

    if args.brief:
        print(_format_default(spec_dir))
    else:
        _paged_output(_format_verbose(spec_dir))


if __name__ == "__main__":
    main()
