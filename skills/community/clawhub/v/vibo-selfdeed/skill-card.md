## Description:

Structures an explicitly delegated multi-step task into a consent-gated autonomous mission that restores ViBo memory, scans for issues, proposes fixes, applies confirmed changes with backups, iterates, records lessons, and reports results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnbochkarev-netizen](https://clawhub.ai/user/vnbochkarev-netizen)

### License/Terms of Use:

MIT-0 for the ClawHub listing; ViBo EULA applies to product use

## Use Case:

Developers and operators use this skill when they explicitly delegate a multi-step code, document, or configuration task and want the agent to plan, confirm, execute, checkpoint, learn from the result, and report progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The mission workflow can edit local files and create backups or mission state.

Mitigation: Run it only in a tightly scoped workspace and keep confirmation gates enabled for sensitive or production projects.

Risk: Using --auto skips per-fix confirmations and can apply changes without review.

Mitigation: Avoid --auto unless the workspace is disposable or the allowed changes are narrowly bounded.

Risk: The skill stores mission progress and lessons in local ViBo memory.

Mitigation: Tell users what will be stored before starting, avoid secrets, and use the documented deletion paths for mission folders, backups, and ViBo facts.

Risk: The skill runs an external ViBo Python CLI.

Mitigation: Verify the exact vibo_use.py path before use and keep VIBO_CLI pointed only at the intended Python file.

Risk: Optional Telegram controls can send mission details to an external service.

Mitigation: Leave Telegram environment variables unset for confidential work and use local confirmation instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vnbochkarev-netizen/skills/vibo-selfdeed)
- [ViBo product site](https://wwwvibo.com)
- [ViBo CLI download](https://wwwvibo.com/download/skill)
- [ViBo trial download](https://wwwvibo.com/download/trial)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local mission state artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local mission checkpoints, backups, and ViBo memory entries during an approved mission.]

## Skill Version(s):

1.0.13 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
