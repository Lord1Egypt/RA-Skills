#!/usr/bin/env python3
"""Inventory likely WCAG 4.1.2 components in static HTML source."""

from __future__ import annotations

import argparse
import json
import sys
from html.parser import HTMLParser
from pathlib import Path


STATE_ATTRIBUTES = {
    "aria-busy",
    "aria-checked",
    "aria-current",
    "aria-disabled",
    "aria-expanded",
    "aria-hidden",
    "aria-invalid",
    "aria-live",
    "aria-pressed",
    "aria-selected",
    "aria-valuenow",
    "aria-valuetext",
}
STATEFUL_ROLES = {
    "checkbox",
    "combobox",
    "gridcell",
    "listbox",
    "menuitemcheckbox",
    "menuitemradio",
    "meter",
    "option",
    "progressbar",
    "radio",
    "scrollbar",
    "slider",
    "spinbutton",
    "switch",
    "tab",
    "treeitem",
}
STATEFUL_INPUT_TYPES = {"checkbox", "number", "radio", "range"}


class ComponentInventory(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.components: list[dict[str, object]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.lower(): value for key, value in attrs}
        role = attributes.get("role")
        input_type = (attributes.get("type") or "text").lower()
        native_interactive = (
            (tag == "a" and "href" in attributes)
            or tag in {"button", "select", "textarea", "summary"}
            or (tag == "input" and input_type != "hidden")
            or tag == "details"
            or tag in {"meter", "progress"}
        )
        custom_interactive = (
            role is not None
            or (
                attributes.get("tabindex") is not None
                and attributes.get("tabindex") != "-1"
            )
        )
        has_state_attribute = any(name in attributes for name in STATE_ATTRIBUTES) or (
            "data-wcag-412-dynamic" in attributes
        )
        if not native_interactive and not custom_interactive and not has_state_attribute:
            return

        reasons = sorted(name for name in STATE_ATTRIBUTES if name in attributes)
        if tag == "details":
            reasons.append("native details disclosure")
        if tag == "summary":
            reasons.append("native details trigger")
        if tag == "select":
            reasons.append("native select value")
        if tag == "input" and input_type in STATEFUL_INPUT_TYPES:
            reasons.append(f"native input type={input_type}")
        if tag in {"meter", "progress"}:
            reasons.append(f"native {tag} value")
        if role in STATEFUL_ROLES:
            reasons.append(f"stateful role={role}")
        if "data-wcag-412-dynamic" in attributes:
            reasons.append("application-declared dynamic state")

        dynamic = bool(reasons)
        manual_at_review = "aria-live" in attributes or role is not None
        review_statuses = [
            "4.1.2-dynamic-required" if dynamic else "4.1.2-static"
        ]
        if manual_at_review:
            review_statuses.append("4.1.2-manual-AT-review")
        self.components.append(
            {
                "line": self.getpos()[0],
                "tag": tag,
                "id": attributes.get("id"),
                "role": role,
                "status": (
                    "4.1.2-dynamic-required"
                    if dynamic
                    else "4.1.2-static"
                ),
                "reasons": reasons,
                "accessible_name_and_semantics": "verify in rendered accessibility tree",
                "interaction_test": (
                    "DYNAMIC TEST REQUIRED" if dynamic else "review applicable interactions"
                ),
                "review_statuses": review_statuses,
                "manual_at_review": manual_at_review,
            }
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "List likely interactive/stateful components in a local HTML source "
            "file. This is a review aid, not a WCAG conformance checker."
        )
    )
    parser.add_argument("html_file", type=Path, help="HTML source file to inventory")
    parser.add_argument("--json", action="store_true", help="write machine-readable JSON")
    args = parser.parse_args()

    try:
        source = args.html_file.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Could not read {args.html_file}: {error}", file=sys.stderr)
        return 2

    inventory = ComponentInventory()
    inventory.feed(source)
    result = {
        "criterion": "4.1.2",
        "source": str(args.html_file),
        "limitation": (
            "Static source inventory only: it cannot calculate the rendered "
            "accessible name/tree or observe state transitions."
        ),
        "components": inventory.components,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"WCAG {result['criterion']} candidate inventory: {args.html_file}")
        print(result["limitation"])
        if not inventory.components:
            print("No likely interactive components found.")
        for component in inventory.components:
            identifier = f"#{component['id']}" if component["id"] else ""
            role = f" role={component['role']}" if component["role"] else ""
            reasons = ", ".join(component["reasons"]) or "no dynamic state inferred"
            print(
                f"Line {component['line']}: {component['tag']}{identifier}{role}: "
                f"{component['status']} ({reasons})"
            )
            print(f"  {component['interaction_test']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
