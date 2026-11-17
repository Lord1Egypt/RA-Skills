## Description:

Publishes or schedules content across supported Chinese social platforms with platform-specific formatting and publish logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, operators, and developers use this skill to adapt, publish, or schedule articles and social posts across supported Chinese platforms from file or command-line inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to store powerful social-media session cookies in plaintext.

Mitigation: Use test accounts first, protect the configuration file, avoid committing cookies, and prefer short-lived or revocable credentials where possible.

Risk: The skill can post or schedule content without a clear preview or safety boundary.

Mitigation: Manually preview scheduled or multi-platform posts and confirm the target accounts and platforms before relying on automation.

Risk: Platform-specific adaptation can truncate or change content before publishing.

Mitigation: Review platform-specific output for meaning, formatting, and compliance before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/zh-social-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration; runtime use can publish or schedule social content and write status logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires platform cookies for authenticated publishing and may make external social-platform API requests.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
