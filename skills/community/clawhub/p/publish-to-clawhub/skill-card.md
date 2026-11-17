## Description:

Prepare and publish a local skill to ClawHub and GitHub using a workflow that keeps the local publish directory clean.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zackz2025](https://clawhub.ai/user/zackz2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to clean, validate, publish, and optionally sync local agent skills to ClawHub and GitHub while reducing credential, force-push, and accidental-publication risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish local skill content to public services before the user notices private names, paths, credentials, or proprietary details.

Mitigation: Confirm the target repository and ClawHub listing, run the documented sensitive-content sweep, and review generated changes before publishing.

Risk: Authentication and GitHub publishing steps can expose credentials or alter public remote history if handled carelessly.

Mitigation: Use browser login, SSH, or a credential manager instead of pasted long-lived tokens, and require explicit user confirmation before any force-push.

## Reference(s):

- [Publish Checklist](references/publish-checklist.md)
- [ClawHub skill listing](https://clawhub.ai/zackz2025/skills/publish-to-clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed file edits, publish commands, authentication guidance, and follow-up checks.]

## Skill Version(s):

2.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
