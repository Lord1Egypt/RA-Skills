## Description:

Audit and fix all skills in the workspace for compliance with skill-creator requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1va7](https://clawhub.ai/user/1va7)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill maintainers use this skill to find OpenClaw skills in a workspace, audit them against skill-creator requirements, and repair non-compliant skill metadata, naming, location, and file layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct broad workspace scans and changes to skill files, including deletions, renames, or moves.

Mitigation: Run the audit in report-only mode first, review each proposed change, and apply repairs only in a version-controlled workspace.

Risk: Unpinned npx usage may introduce supply-chain uncertainty in sensitive workspaces.

Mitigation: Use a pinned package version or a vetted local installation when running in sensitive environments.

Risk: Workspace-wide discovery can include skills outside the expected skills directory.

Mitigation: Run against a scoped workspace path or a temporary copy when the workspace contains unrelated experimental skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1va7/skills/skill-refiner)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenClaw skill-creator](https://github.com/openclaw/openclaw/tree/main/skills/skill-creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown summaries with JSON audit results and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform workspace-wide skill file changes when used in repair mode.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
