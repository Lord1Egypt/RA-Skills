## Description:

Read-only OpenClaw workspace auditor that checks directory structure, task and memory health, knowledge-base indexing, and temporary or oversized files, then returns severity-graded findings and repair suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtsola](https://clawhub.ai/user/dtsola)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and workspace maintainers use it to inspect workspace organization and health, review prioritized findings, and decide which suggested fixes to apply.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports partial inspection: obfuscated text in a referenced script was not fully evaluated, and a binary image was outside analyzer scope.

Mitigation: Review the referenced script and binary asset manually before installation; the benign verdict has medium confidence and does not resolve these inspection gaps.

Risk: ClawScan says the skill description omits a package-install command and does not declare its file-reading scope.

Mitigation: Review the installation steps and the script's file access before running it against a workspace.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-workspace-auditor)
- [Project documentation and source](https://github.com/dtsola/xiaoyaoclaw-workspace-auditor)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Severity-graded Markdown or JSON audit report with findings and repair suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only workspace inspection; findings may be skipped when related workspace structures are absent.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
