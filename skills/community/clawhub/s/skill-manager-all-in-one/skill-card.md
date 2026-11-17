## Description:

Manages OpenClaw skills end to end across creation, modification, publishing, updating, versioning, promotion, and audit workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moroiser](https://clawhub.ai/user/moroiser)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw skill authors and maintainers use this skill to create, modify, publish, update, promote, and audit skills while keeping versioning, review checklists, and confirmation gates explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad edits to persistent OpenClaw memory and workspace files.

Mitigation: Require exact diffs and separate approval before editing MEMORY.md, memory/*.md, TOOLS.md, or other persistent workspace records.

Risk: Promotion templates may contain hard-coded attribution that is not appropriate for every publisher.

Mitigation: Replace any fixed attribution with the approved author or omit attribution before public promotion.

Risk: Publishing, renaming, release, deletion, and promotion workflows can make persistent local or external changes.

Mitigation: Show the exact command and wait for the required confirmation signature before executing external or destructive operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/moroiser/skills/skill-manager-all-in-one)
- [ClawHub Publish Reference | ClawHub 发布参考](references/clawhub-publish.md)
- [GitHub Publishing Guide | GitHub 上传专项](references/github-publish.md)
- [Search and Audit Guide | 搜索与审计指南](references/search-and-audit.md)
- [Promotion Guide | 宣传指南](references/promotion.md)
- [ClawFlows Workflow Format Guide | ClawFlows Workflow 格式指南](references/clawflows-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, checklists, and release text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact commands, diffs, changelogs, checklist statuses, and confirmation prompts.]

## Skill Version(s):

4.5.14 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
