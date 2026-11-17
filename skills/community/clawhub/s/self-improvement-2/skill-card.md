## Description:

Captures learnings, errors, and corrections in project markdown files so coding agents can review, resolve, and promote reusable knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhihongyee](https://clawhub.ai/user/zhihongyee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record command failures, corrections, missing capabilities, outdated knowledge, and reusable practices so later agents can inspect or promote them into project guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files may capture sensitive conversation, error, personal, customer, or secret data.

Mitigation: Keep .learnings local by default and redact sensitive data before writing any learning, error, or feature request entry.

Risk: Promoting entries into agent instruction files can change future agent behavior based on unreviewed or misleading guidance.

Mitigation: Require explicit trusted-owner approval and review diffs before promoting learnings into CLAUDE.md, AGENTS.md, .github/copilot-instructions.md, or similar files.

Risk: The artifact includes unpinned npx install commands, which can resolve to changing remote content.

Mitigation: Use a pinned and reviewed source before installation, especially in CI or shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhihongyee/skills/self-improvement-2)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persistent .learnings markdown files and promote selected entries into agent instruction files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
