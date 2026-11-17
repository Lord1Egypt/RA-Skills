## Description:

Audit workspace structure and memory files against OpenClaw conventions to catch drift from standard patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ortegarod](https://clawhub.ai/user/ortegarod)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw workspace maintainers use this skill to review workspace structure, memory hygiene, git status, file scope, and skill layout against documented OpenClaw conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects private OpenClaw workspace, profile, and memory files that may contain personal or sensitive context.

Mitigation: Use it only for intended local workspace audits, keep credentials and raw sensitive chat content out of memory files, and review generated findings before sharing them.

Risk: Expanded memory search paths or experimental session transcript indexing can increase the amount of sensitive material available during review.

Mitigation: Configure memorySearch.extraPaths and session transcript indexing deliberately, excluding secrets, credentials, and unrelated private records.

## Reference(s):

- [OpenClaw workspace conventions](references/openclaw-conventions.md)
- [Workspace review checklist](references/checklist.md)
- [ClawHub skill page](https://clawhub.ai/ortegarod/skills/workspace-review)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown workspace review with passing, warnings, issues, and recommendations sections; may include shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use a bundled shell script to summarize local workspace health when appropriate.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
