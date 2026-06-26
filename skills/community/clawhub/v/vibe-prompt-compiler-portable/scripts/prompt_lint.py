#!/usr/bin/env python3
import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
COMPILE = ROOT / "compile_prompt.py"

VAGUE_REQUEST_MARKERS = [
    "优化一下",
    "弄一下",
    "看下",
    "搞一下",
    "improve it",
    "make it better",
    "fix this",
    "help with this",
]

GENERIC_CONTEXT_MARKERS = [
    "Not fully specified",
    "Not specified",
    "Infer the",
    "Use the existing project stack or choose the simplest suitable option",
]

WEAK_ACCEPTANCE_MARKERS = [
    "Match the intended behavior implied by the request",
    "Deliver the requested behavior with a minimal, testable implementation",
]


def compile_request(request: str, task: str, stack: str, audience: str) -> dict:
    cmd = [
        sys.executable,
        str(COMPILE),
        "--request",
        request,
        "--task",
        task,
        "--output",
        "json",
    ]
    if stack:
        cmd += ["--stack", stack]
    if audience:
        cmd += ["--audience", audience]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)



def split_sections(compiled_prompt: str) -> dict[str, str]:
    sections = {}
    current = None
    bucket = []
    for line in compiled_prompt.splitlines():
        stripped = line.strip()
        if stripped.endswith(":") and stripped[:-1] in {
            "Goal",
            "Current Task",
            "Context Already Known",
            "Assumptions",
            "Scope",
            "Out of Scope",
            "Tech Stack",
            "Constraints",
            "Acceptance Criteria",
            "Output Requirements",
        }:
            if current is not None:
                sections[current] = "\n".join(bucket).strip()
            current = stripped[:-1]
            bucket = []
        elif current is not None:
            bucket.append(line)
    if current is not None:
        sections[current] = "\n".join(bucket).strip()
    return sections



def add_issue(issues: list[dict], severity: str, code: str, message: str, suggestion: str):
    issues.append(
        {
            "severity": severity,
            "code": code,
            "message": message,
            "suggestion": suggestion,
        }
    )



def lint_result(result: dict, stack: str, audience: str) -> dict:
    request = result["request"]
    task_type = result["task_type"]
    assumptions = result.get("assumptions", [])
    compiled_prompt = result["compiled_prompt"]
    sections = split_sections(compiled_prompt)
    issues = []

    if len(request) < 18 or any(marker in request.lower() for marker in VAGUE_REQUEST_MARKERS):
        add_issue(
            issues,
            "warning",
            "vague-request",
            "The raw request is short or vague enough that downstream implementation may drift.",
            "Add one concrete outcome, one target surface, or one acceptance condition to tighten scope.",
        )

    generic_context_hits = sum(
        marker in compiled_prompt for marker in GENERIC_CONTEXT_MARKERS
    )
    generic_context_threshold = 2 if task_type in {"architecture-review", "integration", "automation-workflow"} else 3
    if generic_context_hits >= generic_context_threshold:
        add_issue(
            issues,
            "warning",
            "generic-context",
            "The compiled brief still relies heavily on fallback placeholders or inferred context.",
            "Provide stack, audience, product boundary, or business goal to replace generic defaults.",
        )

    if len(assumptions) >= 4 and not stack and not audience:
        add_issue(
            issues,
            "warning",
            "assumption-heavy",
            "The brief depends on several assumptions while request metadata remains sparse.",
            "Add stack, audience, or existing-system details so the prompt needs fewer inferred assumptions.",
        )

    acceptance = sections.get("Acceptance Criteria", "")
    if not acceptance or any(marker in acceptance for marker in WEAK_ACCEPTANCE_MARKERS):
        add_issue(
            issues,
            "warning",
            "weak-verification",
            "Acceptance criteria are generic and may be hard to verify objectively.",
            "Add measurable success checks such as a visible UI state, concrete API response, or reproducible bug scenario.",
        )

    if task_type == "general":
        add_issue(
            issues,
            "info",
            "general-task-type",
            "The request stayed in the general bucket, which may be fine but gives weaker downstream guidance.",
            "If possible, clarify whether this is a UI, backend, CRUD, bugfix, integration, or architecture task.",
        )

    score = max(0, 100 - 15 * len([i for i in issues if i["severity"] == "warning"]) - 5 * len([i for i in issues if i["severity"] == "info"]))

    return {
        "request": request,
        "task_type": task_type,
        "score": score,
        "issues": issues,
        "sections_checked": sorted(sections.keys()),
        "summary": "Looks solid." if not issues else f"Found {len(issues)} lint issue(s).",
    }



def main():
    parser = argparse.ArgumentParser(description="Lint a compiled vibe prompt for vagueness, weak verification, and assumption overload.")
    parser.add_argument("--request", required=True, help="Raw user request")
    parser.add_argument("--task", default="auto", help="Task type override")
    parser.add_argument("--stack", default="", help="Preferred tech stack")
    parser.add_argument("--audience", default="", help="Target users or stakeholders")
    parser.add_argument("--output", default="json", choices=["json", "text"], help="Output format")
    args = parser.parse_args()

    compiled = compile_request(args.request, args.task, args.stack, args.audience)
    linted = lint_result(compiled, args.stack, args.audience)

    if args.output == "json":
        print(json.dumps(linted, ensure_ascii=False, indent=2))
    else:
        print(f"Score: {linted['score']}")
        print(linted["summary"])
        for issue in linted["issues"]:
            print(f"- [{issue['severity']}] {issue['code']}: {issue['message']}")
            print(f"  Suggestion: {issue['suggestion']}")


if __name__ == "__main__":
    main()
