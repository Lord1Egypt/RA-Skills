## Description:

Safely uninstall and reinstall OpenClaw while preserving user configurations, credentials, memory files, skills, and custom settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albertpan2018](https://clawhub.ai/user/albertpan2018)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to perform a clean OpenClaw reinstall, preserve user data, restore configuration, and troubleshoot common post-restore issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup and reinstall commands could delete sensitive OpenClaw data.

Mitigation: Create and verify an encrypted backup before running commands, inspect what will be restored, and prefer renaming old directories before deletion.

Risk: Install commands could execute unverified npm code with elevated privileges.

Mitigation: Avoid sudo npm and @latest where possible, and use a trusted pinned OpenClaw version or verified local binary.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/albertpan2018/skills/reinstall-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, and wsl according to server-resolved metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
