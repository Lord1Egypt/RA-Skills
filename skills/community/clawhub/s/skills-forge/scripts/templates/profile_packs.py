"""Profile-specific scaffold templates for skill generation."""

PROFILE_HINTS = {
    "academic": {"citation", "bibliography", "references", "apa", "mla", "essay", "paper", "assignment"},
    "product": {"prd", "mvp", "roadmap", "competitor", "onboarding", "requirements", "acceptance"},
    "integration": {"api", "oauth", "webhook", "token", "sync", "database", "connector", "telegram", "notion"},
    "script": {"export", "convert", "validate", "parse", "batch", "cli", "generate", "report"},
}

PROFILE_PACKS = {
    "academic": {
        "freedom_level": "medium freedom: keep reasoning flexible, but require explicit citation safety checks before producing bibliography-like output.",
        "resource_policy": [
            "Read `references/citation-style-checklist.md` when the user asks for a named citation style.",
            "Read `references/academic-output-template.md` when the user needs a reusable essay, paper, or assignment structure.",
            "Read `references/source-metadata-intake.md` before treating source leads as complete references.",
        ],
        "default_triggers": [
            "APA format",
            "MLA format",
            "Chicago citation",
            "Harvard referencing",
            "in-text citation",
            "reference list",
            "works cited",
            "source metadata",
        ],
        "interface": {
            "short_description": "Build citation-safe academic scaffolds",
            "default_prompt": "Create a citation-safe academic plan with missing metadata checks.",
        },
        "workflow": [
            "Identify the assignment or academic output the user needs.",
            "Detect the requested citation style and edition, or state the style assumption.",
            "Collect source metadata into a missing-fields table before drafting citations.",
            "Separate verified claims, source leads, and writing advice.",
            "Produce a structured academic artifact with citation reminders and safe placeholders.",
            "Flag incomplete or unverifiable citations instead of inventing source details.",
        ],
        "output_contract": [
            "Task and citation-style assumptions",
            "Working thesis or purpose statement",
            "Claim-to-evidence plan",
            "Source metadata or missing-fields table",
            "Draft structure or bibliography scaffold",
            "Citation risk notes",
        ],
        "quality_gates": [
            "Never invent authors, years, titles, journal names, page numbers, URLs, or DOIs.",
            "When the user provides only a URL or title, mark it as a source lead until metadata is verified.",
            "When the user asks for finished references without enough metadata, return a missing-fields table.",
        ],
        "references": {
            "citation-style-checklist.md": """# Citation Style Checklist

## Required metadata

- author
- year or publication date
- title
- publisher, journal, or site
- URL or DOI when available
- access date only when the style or source type requires it

## Common trigger phrases

- APA format
- MLA format
- Chicago citation
- Harvard referencing
- in-text citation
- reference list
- works cited
- bibliography

## Style reminders

- APA: author-date emphasis, year near the author, sentence-case article titles.
- MLA: author-page emphasis when page numbers exist, title formatting matters.
- Chicago: decide between notes-bibliography and author-date before drafting.
- Harvard: author-date structure, institution-specific variants are common.

## Hard rule

Never invent a citation. Mark missing metadata explicitly.
If the user asks for a finished bibliography and metadata is incomplete, produce a missing-fields table instead.
""",
            "academic-output-template.md": """# Academic Output Template

## Task

## Citation style assumption

## Working thesis

## Claim-to-evidence plan

| Claim | Evidence needed | Candidate source | Citation status |
| --- | --- | --- | --- |

## Citation requirements

## Source metadata intake

| Source lead | Author | Date | Title | Publisher/journal/site | URL/DOI | Missing fields |
| --- | --- | --- | --- | --- | --- | --- |

## Draft structure

## Missing source data

## Citation risk notes

## Safe phrasing

- "Use this as a source lead, not a finished citation."
- "The citation cannot be completed until publication metadata is provided."
- "This claim needs a peer-reviewed or primary source before submission."
""",
            "source-metadata-intake.md": """# Source Metadata Intake

## Minimum fields before a reference is treated as complete

- author or responsible institution
- date or clear no-date marker
- title
- container or publisher
- URL, DOI, page range, or stable locator when applicable

## Verification behavior

- If source metadata is provided by the user, preserve it and flag gaps.
- If only a URL is provided, treat it as a lead unless a browsing/search tool verifies the metadata.
- If no sources are provided, produce a research plan rather than fake references.
""",
        },
    },
    "product": {
        "freedom_level": "high-to-medium freedom: adapt product judgment to context, but keep MVP, non-goals, and acceptance criteria structured.",
        "resource_policy": [
            "Read `references/prd-shape.md` when producing a PRD, feature spec, or implementation handoff.",
            "Read `references/prioritization.md` when scope decisions, MVP cuts, or roadmap tradeoffs are central.",
        ],
        "default_triggers": [
            "PRD",
            "MVP scope",
            "user story",
            "acceptance criteria",
            "roadmap",
            "competitive analysis",
            "feature spec",
            "Dev handoff",
        ],
        "interface": {
            "short_description": "Turn product ideas into testable specs",
            "default_prompt": "Turn this product idea into an MVP spec and Dev Agent handoff.",
        },
        "workflow": [
            "Clarify the user, problem, and target behavior.",
            "Define the smallest useful MVP scope.",
            "Separate must-have requirements from later work.",
            "Write acceptance criteria that Dev Agent can test.",
            "End with a handoff block for implementation.",
        ],
        "output_contract": [
            "Product goal",
            "Target user and scenario",
            "MVP scope",
            "Non-goals",
            "Acceptance criteria",
            "Dev Agent handoff",
        ],
        "quality_gates": [
            "Keep the MVP small enough to validate the core behavior.",
            "Make acceptance criteria observable and testable.",
            "Call out non-goals so Dev Agent does not overbuild.",
        ],
        "references": {
            "prd-shape.md": """# PRD Shape

## Goal

## User and scenario

## Problem

## MVP scope

## Non-goals

## Acceptance criteria

## Risks

## Dev handoff
""",
            "prioritization.md": """# Prioritization Rules

- Must-have: required for the first successful user journey.
- Should-have: improves the first journey but can ship later.
- Not-now: attractive but not needed to test the core value.
""",
        },
    },
    "integration": {
        "freedom_level": "medium freedom: adapt setup details to the target API, but keep credentials, health checks, and failure behavior explicit.",
        "resource_policy": [
            "Read `references/integration-checklist.md` before proposing setup steps or claiming an integration is ready.",
        ],
        "default_triggers": [
            "API key",
            "OAuth",
            "webhook",
            "Telegram bot",
            "Notion database",
            "connector",
            "sync job",
            "health check",
        ],
        "interface": {
            "short_description": "Plan safe API and tool integrations",
            "default_prompt": "Plan this integration with credentials, health checks, and failure handling.",
        },
        "workflow": [
            "Identify the external system, auth model, and target operation.",
            "Check required credentials and permissions before giving commands.",
            "Define a minimal health check.",
            "Document safe failure behavior and retry limits.",
            "Keep secrets out of generated examples and logs.",
        ],
        "output_contract": [
            "Integration purpose",
            "Required credentials",
            "Setup steps",
            "Health check",
            "Failure handling",
            "Security notes",
        ],
        "quality_gates": [
            "Never print real secrets into examples, logs, commits, or reports.",
            "Require a health check before claiming the integration works.",
            "Prefer least-privilege tokens and explicit failure handling.",
        ],
        "references": {
            "integration-checklist.md": """# Integration Checklist

- What external system is used?
- Which credentials are required?
- Where should credentials be stored?
- What is the smallest health check?
- What errors should stop retries?
- What data must never be logged?
""",
        },
    },
    "script": {
        "freedom_level": "low freedom for execution: prefer deterministic scripts, validated inputs, dry-run paths, and explicit exit codes.",
        "resource_policy": [
            "Read `references/script-contract.md` before editing or running bundled scripts.",
            "Run `scripts/run.py` only after confirming inputs and whether mutation is allowed.",
        ],
        "default_triggers": [
            "CLI",
            "batch process",
            "parse files",
            "generate report",
            "validate input",
            "export data",
            "convert files",
            "automation script",
        ],
        "interface": {
            "short_description": "Package repeatable work into scripts",
            "default_prompt": "Design a deterministic script contract for this repeated task.",
        },
        "workflow": [
            "Identify the repeated operation and expected inputs.",
            "Prefer a deterministic script over repeated prompt-only execution.",
            "Validate inputs before modifying files or external systems.",
            "Return machine-readable output when useful.",
            "Document representative commands.",
        ],
        "output_contract": [
            "Command examples",
            "Input contract",
            "Output contract",
            "Validation behavior",
            "Failure modes",
        ],
        "quality_gates": [
            "Prefer dry-run behavior for file or external-system mutations.",
            "Use explicit exit codes for predictable automation.",
            "Do not hide parse or validation failures behind best-effort output.",
        ],
        "references": {
            "script-contract.md": """# Script Contract

## Inputs

## Outputs

## Exit codes

## Safety checks

## Example commands
""",
        },
        "scripts": {
            "run.py": """#!/usr/bin/env python3
import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser(description="Skill-specific deterministic entry point. Customize before publishing.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = {"status": "scaffold", "next_step": "wire deterministic behavior for this skill"}
    print(json.dumps(payload, indent=2) if args.json else payload["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
""",
        },
    },
    "workflow": {
        "freedom_level": "high freedom for judgment, medium freedom for output shape: adapt the workflow, but keep triggers, steps, and quality checks stable.",
        "resource_policy": [
            "Read `references/workflow-template.md` when turning the workflow into a reusable checklist or handoff artifact.",
        ],
        "default_triggers": [
            "recurring workflow",
            "standard operating procedure",
            "handoff checklist",
            "repeatable process",
            "quality gate",
            "decision rules",
        ],
        "interface": {
            "short_description": "Standardize repeatable agent workflows",
            "default_prompt": "Turn this repeated task into a reusable workflow with quality gates.",
        },
        "workflow": [
            "Clarify the user's repeated job.",
            "Choose the smallest stable workflow.",
            "Produce a structured output with explicit assumptions.",
            "Note when to use a script, reference file, or external tool.",
            "Record open questions that affect reuse.",
        ],
        "output_contract": [
            "Purpose",
            "Trigger conditions",
            "Workflow",
            "Expected output",
            "Quality checks",
        ],
        "quality_gates": [
            "Do not create a skill for a one-off task.",
            "Prefer a narrow reusable workflow over broad role instructions.",
            "Capture assumptions that affect repeatability.",
        ],
        "references": {
            "workflow-template.md": """# Workflow Template

## Purpose

## Trigger

## Steps

## Output

## Quality checks
""",
        },
    },
}
