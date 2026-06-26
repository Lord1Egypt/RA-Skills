#!/usr/bin/env python3
import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
COMPILE = ROOT / "compile_prompt.py"
VALID_MODES = ["plan-only", "build-first-slice", "bugfix", "architecture", "integration", "workflow"]
VALID_TARGET_TOOLS = ["generic", "cursor", "codex-cli", "claude-code", "gemini-cli"]
LANGUAGE_PRESETS = ["english-first", "chinese-first"]
RULESETS = ["none", "minimal-diff", "test-first", "repo-safe"]


def compile_request(request: str, task: str, stack: str, audience: str, language_preset: str, ruleset: str, repo_rules_file: str, repo_root: str, auto_repo_rules: bool) -> dict:
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
    if language_preset:
        cmd += ["--language-preset", language_preset]
    if ruleset:
        cmd += ["--ruleset", ruleset]
    if repo_rules_file:
        cmd += ["--repo-rules-file", repo_rules_file]
    if repo_root:
        cmd += ["--repo-root", repo_root]
    if auto_repo_rules:
        cmd += ["--auto-repo-rules"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def infer_mode(task_type: str, requested_mode: str) -> str:
    if requested_mode != "auto":
        return requested_mode
    if task_type == "bugfix":
        return "bugfix"
    if task_type == "architecture-review":
        return "architecture"
    if task_type == "integration":
        return "integration"
    if task_type == "automation-workflow":
        return "workflow"
    if task_type in ["new-project", "ai-feature", "deployment"]:
        return "plan-only"
    return "build-first-slice"


def build_execution_rules(mode: str, language_preset: str) -> list[str]:
    if language_preset == "chinese-first":
        base_rules = [
            "先简要重述目标。",
            "除非明确要求扩大范围，否则只实现当前切片。",
            "不要改动无关文件。",
            "说明如何验证结果。",
        ]
        if mode == "plan-only":
            return base_rules + [
                "在动手前先给出简短执行计划。",
                "不要在第一步就直接铺开大范围编码。",
            ]
        if mode == "bugfix":
            return base_rules + [
                "先做根因分析。",
                "优先最小且安全的修复，而不是顺手清理或重设计。",
            ]
        if mode == "architecture":
            return base_rules + [
                "先比较 2-3 个务实方案，再给出推荐。",
                "优先适配当前技术栈的最小稳妥路径。",
                "区分当前建议与未来演进方向。",
            ]
        if mode == "integration":
            return base_rules + [
                "把鉴权、重试、幂等和失败处理讲清楚。",
                "明确指出运维风险和验证检查点。",
            ]
        if mode == "workflow":
            return base_rules + [
                "定义触发方式、执行状态、重试行为和可观测性。",
                "优先可恢复、可检查的工作流切片，而不是黑盒自动化。",
            ]
        return base_rules + [
            "如果任务较大，先给一个简短计划。",
        ]

    base_rules = [
        "Start by restating the goal briefly.",
        "Only implement the current slice unless explicitly asked to do more.",
        "Do not modify unrelated files.",
        "Explain how to verify the result.",
    ]
    if mode == "plan-only":
        return base_rules + [
            "Produce a short execution plan before implementation.",
            "Do not jump into broad coding before scoping the first slice.",
        ]
    if mode == "bugfix":
        return base_rules + [
            "Start with root-cause analysis.",
            "Prefer the smallest safe fix over cleanup or redesign.",
        ]
    if mode == "architecture":
        return base_rules + [
            "Compare 2-3 practical options before recommending one.",
            "Prefer the smallest robust path for the current stack.",
            "Separate current-state recommendation from future-state evolution.",
        ]
    if mode == "integration":
        return base_rules + [
            "Make auth, retries, idempotency, and failure handling explicit.",
            "Call out operational risks and verification checkpoints.",
        ]
    if mode == "workflow":
        return base_rules + [
            "Define trigger, execution states, retry behavior, and observability.",
            "Prefer restartable, inspectable workflow slices over hidden automation.",
        ]
    return base_rules + [
        "If the task is large, produce a short plan first.",
    ]


def infer_non_goals(task_type: str, language_preset: str) -> list[str]:
    if language_preset == "chinese-first":
        shared = [
            "不要改动无关文件或模块。",
            "不要把范围扩到当前切片之外。",
        ]
        task_specific = {
            "bugfix": ["修 bug 时不要顺手重构无关代码。"],
            "architecture-review": ["除非当前系统明确无法承载需求，否则不要直接建议整体重写。"],
            "integration": ["在没有明确重试与验证策略前，不要假设第三方系统是可靠的。"],
            "automation-workflow": ["不要用模糊的自动化抽象掩盖失败处理。"],
            "deployment": ["没有明确收益时，不要引入额外运维复杂度。"],
        }
        return shared + task_specific.get(task_type, [])

    shared = [
        "Do not modify unrelated files or modules.",
        "Do not expand scope beyond the current slice.",
    ]
    task_specific = {
        "bugfix": ["Do not refactor unrelated code while fixing the bug."],
        "architecture-review": ["Do not recommend a rewrite unless the current system clearly cannot support the requirement."],
        "integration": ["Do not assume third-party reliability without explicit retries and verification."],
        "automation-workflow": ["Do not hide failure handling behind vague automation abstractions."],
        "deployment": ["Do not introduce operational complexity without a clear reason."],
    }
    return shared + task_specific.get(task_type, [])


def infer_deliverables(task_type: str, mode: str, language_preset: str) -> list[str]:
    if language_preset == "chinese-first":
        if mode == "architecture":
            return [
                "架构建议",
                "2-3 个备选方案及权衡",
                "分阶段落地计划",
                "验证与监控建议",
            ]
        if mode == "integration":
            return [
                "集成设计",
                "数据流与鉴权流",
                "重试/幂等规则",
                "验证清单",
            ]
        if mode == "workflow":
            return [
                "工作流设计",
                "执行状态",
                "失败与重试规则",
                "第一版实现切片",
            ]
        if task_type == "bugfix":
            return [
                "根因分析",
                "最小修复计划",
                "补丁或代码改动",
                "验证步骤",
            ]
        return [
            "澄清后的目标",
            "最小计划",
            "当前实现切片",
            "验证建议",
        ]

    if mode == "architecture":
        return [
            "Recommended architecture",
            "2-3 alternatives with trade-offs",
            "Phased rollout plan",
            "Validation and monitoring guidance",
        ]
    if mode == "integration":
        return [
            "Integration design",
            "Data and auth flow",
            "Retry/idempotency rules",
            "Verification checklist",
        ]
    if mode == "workflow":
        return [
            "Workflow design",
            "Execution states",
            "Failure and retry rules",
            "First implementation slice",
        ]
    if task_type == "bugfix":
        return [
            "Root-cause analysis",
            "Minimal fix plan",
            "Patch or code change",
            "Verification steps",
        ]
    return [
        "Clarified goal",
        "Minimal plan",
        "Current implementation slice",
        "Verification guidance",
    ]


def build_tool_wrapper(target_tool: str, language_preset: str) -> dict:
    wrappers = {
        "generic": {
            "label": "Generic" if language_preset == "english-first" else "通用",
            "instruction": "Use this brief as the source of truth. Implement only the current slice and explain how to verify it." if language_preset == "english-first" else "以这份 brief 为唯一事实来源。只实现当前切片，并说明如何验证结果。",
        },
        "cursor": {
            "label": "Cursor",
            "instruction": "Use this brief as the source of truth. Plan briefly first, then implement only the first useful slice. Do not modify unrelated files." if language_preset == "english-first" else "以这份 brief 为唯一事实来源。先做一个简短计划，再只实现第一个有价值的切片。不要改动无关文件。",
        },
        "codex-cli": {
            "label": "Codex CLI",
            "instruction": "Use this brief as the source of truth. Work surgically, prefer minimal diffs, preserve existing conventions, and verify the current slice before moving on." if language_preset == "english-first" else "以这份 brief 为唯一事实来源。用外科手术式改动，优先最小 diff，保持现有约定，并在继续前先验证当前切片。",
        },
        "claude-code": {
            "label": "Claude Code",
            "instruction": "Use this brief as the source of truth. Start with a short plan for broad tasks, preserve existing conventions, and keep the patch focused on the current slice." if language_preset == "english-first" else "以这份 brief 为唯一事实来源。面对较宽的任务先给出简短计划，保持现有约定，并让补丁聚焦在当前切片。",
        },
        "gemini-cli": {
            "label": "Gemini CLI",
            "instruction": "Use this brief as the source of truth. Compare practical options when useful, then recommend or implement the smallest robust path for the current stack." if language_preset == "english-first" else "以这份 brief 为唯一事实来源。必要时先比较可行方案，再为当前技术栈推荐或实现最小且稳妥的路径。",
        },
    }
    return wrappers[target_tool]


def build_handoff(data: dict, mode: str, target_tool: str, language_preset: str) -> dict:
    task_type = data["task_type"]
    compiled_prompt = data["compiled_prompt"].strip()
    assumptions = data.get("assumptions", [])
    raw_request = data["request"]
    ruleset = data.get("ruleset", "none")
    must_rules = data.get("must_rules", [])
    must_not_rules = data.get("must_not_rules", [])
    validation_rules = data.get("validation_rules", [])
    scope_guardrails = data.get("scope_guardrails", [])
    execution_rules = build_execution_rules(mode, language_preset)
    non_goals = infer_non_goals(task_type, language_preset)
    deliverables = infer_deliverables(task_type, mode, language_preset)
    tool_wrapper = build_tool_wrapper(target_tool, language_preset)

    if language_preset == "chinese-first":
        handoff_text = f"""请把下面这份 vibe-coding brief 作为唯一事实来源。

目标工具：{tool_wrapper['label']}
任务类型：{task_type}
执行模式：{mode}
原始请求：{raw_request}

编译后的 brief：
{compiled_prompt}

假设：
"""
    else:
        handoff_text = f"""Use the following compiled vibe-coding brief as the source of truth.

Target tool: {tool_wrapper['label']}
Task type: {task_type}
Execution mode: {mode}
Raw request: {raw_request}

Compiled brief:
{compiled_prompt}

Assumptions:
"""
    for item in assumptions:
        handoff_text += f"- {item}\n"

    handoff_text += "\n非目标：\n" if language_preset == "chinese-first" else "\nNon-goals:\n"
    for item in non_goals:
        handoff_text += f"- {item}\n"

    handoff_text += "\n期望交付物：\n" if language_preset == "chinese-first" else "\nExpected deliverables:\n"
    for item in deliverables:
        handoff_text += f"- {item}\n"

    handoff_text += "\n执行规则：\n" if language_preset == "chinese-first" else "\nExecution rules:\n"
    for rule in execution_rules:
        handoff_text += f"- {rule}\n"

    if ruleset != "none":
        handoff_text += "\n开发规则：\n" if language_preset == "chinese-first" else "\nDevelopment rules:\n"
        if must_rules:
            handoff_text += "- Must:\n" if language_preset != "chinese-first" else "- 必须：\n"
            for item in must_rules:
                handoff_text += f"  - {item}\n"
        if must_not_rules:
            handoff_text += "- Must not:\n" if language_preset != "chinese-first" else "- 禁止：\n"
            for item in must_not_rules:
                handoff_text += f"  - {item}\n"
        if validation_rules:
            handoff_text += "- Validation required:\n" if language_preset != "chinese-first" else "- 验证要求：\n"
            for item in validation_rules:
                handoff_text += f"  - {item}\n"
        if scope_guardrails:
            handoff_text += "- Scope guardrails:\n" if language_preset != "chinese-first" else "- 范围护栏：\n"
            for item in scope_guardrails:
                handoff_text += f"  - {item}\n"

    handoff_text += f"\n{tool_wrapper['label']} 包装提示：\n" if language_preset == "chinese-first" else f"\nTool wrapper for {tool_wrapper['label']}:\n"
    handoff_text += f"{tool_wrapper['instruction']}\n"

    return {
        "task_type": task_type,
        "execution_mode": mode,
        "target_tool": target_tool,
        "target_tool_label": tool_wrapper["label"],
        "language_preset": language_preset,
        "ruleset": ruleset,
        "repo_rules_file": data.get("repo_rules_file", ""),
        "repo_root": data.get("repo_root", ""),
        "auto_repo_rules": data.get("auto_repo_rules", False),
        "must_rules": must_rules,
        "must_not_rules": must_not_rules,
        "validation_rules": validation_rules,
        "scope_guardrails": scope_guardrails,
        "tool_instruction": tool_wrapper["instruction"],
        "raw_request": raw_request,
        "compiled_prompt": compiled_prompt,
        "assumptions": assumptions,
        "non_goals": non_goals,
        "deliverables": deliverables,
        "execution_rules": execution_rules,
        "handoff_text": handoff_text.strip() + "\n",
    }


def main():
    parser = argparse.ArgumentParser(description="Create a portable execution handoff from a rough request.")
    parser.add_argument("--request", required=True, help="Raw user request")
    parser.add_argument("--task", default="auto", help="Task type override")
    parser.add_argument("--mode", default="auto", choices=["auto", *VALID_MODES], help="Execution mode")
    parser.add_argument("--target-tool", default="generic", choices=VALID_TARGET_TOOLS, help="Target coding tool preset")
    parser.add_argument("--language-preset", default="english-first", choices=LANGUAGE_PRESETS, help="Language style preset")
    parser.add_argument("--ruleset", default="none", choices=RULESETS, help="Development rule preset")
    parser.add_argument("--repo-rules-file", default="", help="Optional JSON file with repository-specific rules")
    parser.add_argument("--repo-root", default="", help="Repository root for automatic rule extraction")
    parser.add_argument("--auto-repo-rules", action="store_true", help="Automatically extract rules from common repository files")
    parser.add_argument("--stack", default="", help="Preferred tech stack")
    parser.add_argument("--audience", default="", help="Target users or stakeholders")
    parser.add_argument("--output", default="json", choices=["json", "handoff", "prompt"], help="Output format")
    args = parser.parse_args()

    compiled = compile_request(args.request, args.task, args.stack, args.audience, args.language_preset, args.ruleset, args.repo_rules_file, args.repo_root, args.auto_repo_rules)
    mode = infer_mode(compiled["task_type"], args.mode)
    handoff = build_handoff(compiled, mode, args.target_tool, args.language_preset)

    if args.output == "json":
        print(json.dumps(handoff, ensure_ascii=False, indent=2))
    elif args.output == "prompt":
        print(handoff["compiled_prompt"])
    else:
        print(handoff["handoff_text"])


if __name__ == "__main__":
    main()
