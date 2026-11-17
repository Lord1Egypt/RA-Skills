## Description:

Find ski resorts and snowboarding destinations, including trail maps, difficulty levels, lift pass prices, equipment rental, snow conditions, and related travel services powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to retrieve ski resort and snowboarding destination options from the flyai CLI, then present concise Markdown comparisons with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run an unpinned global flyai CLI package.

Mitigation: Install only from a trusted source, prefer a pinned package version, and require review before installation in managed environments.

Risk: Travel queries are converted into CLI commands and may include user-provided city or keyword values.

Mitigation: Use only documented parameters, sanitize command arguments, and inspect generated commands before execution.

Risk: The skill requires booking links in normal responses.

Mitigation: Use only CLI-provided detailUrl values and validate booking-link domains before presenting them to users.

Risk: The artifact describes optional local persistence of raw execution logs.

Mitigation: Disable persistent logs where possible, or redact personal travel details before writing local log files.

## Reference(s):

- [Skill page](https://clawhub.ai/xiejinsong/skills/ski-resort)
- [Publisher profile](https://clawhub.ai/user/xiejinsong)
- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with comparison tables, booking links, brief guidance, and inline shell commands when setup or retries are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should mirror the user's language and include only CLI-sourced travel results with detailUrl booking links.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
