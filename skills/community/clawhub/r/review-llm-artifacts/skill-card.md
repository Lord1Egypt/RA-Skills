## Description:

Detects common LLM coding agent artifacts across four categories (tests, dead code, abstraction, style) over the project or changed files, using parallel subagents when supported or sequential passes otherwise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering reviewers use this skill to scan changed files or an entire project for likely LLM-generated coding artifacts, then receive a structured findings report grouped by tests, dead code, abstraction, and style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repository source files and may scan the full project when requested with --all.

Mitigation: Run it only in repositories and paths intended for review, and prefer the default changed-files scope when a full scan is unnecessary.

Risk: The skill writes a local .beagle/llm-artifacts-review.json report into the working tree.

Mitigation: Review the generated report before committing or sharing it.

Risk: Reported artifact findings can be false positives or need engineering judgment before code changes.

Mitigation: Verify findings before applying fixes, especially for deletions or broad refactors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/review-llm-artifacts)
- [Publisher profile](https://clawhub.ai/user/anderskev)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with shell commands and a structured JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes .beagle/llm-artifacts-review.json when findings are consolidated; no external API keys are indicated by evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
