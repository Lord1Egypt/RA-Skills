## Description:

Searches Twitter/X data, monitors accounts and trends, and supports authorized posting, replies, likes, follows, and media publishing through the AISA relay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and autonomous-agent operators use this skill to search and monitor Twitter/X data, summarize social signals, and perform authorized posting or engagement through AISA relay workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured AISA API key can appear in normal command output, logs, or transcripts.

Mitigation: Avoid running status, authorization, or posting commands with sensitive keys until the key-output issue is fixed; rotate any key that may have been exposed.

Risk: Credentials and media can be sent to arbitrary HTTP or HTTPS relay URLs when TWITTER_RELAY_BASE_URL is changed.

Mitigation: Use the default trusted HTTPS relay unless a custom endpoint is fully trusted and approved.

Risk: The skill can perform real Twitter/X account actions, including publishing posts, likes, follows, replies, and media uploads.

Mitigation: Review intended write or engagement actions before execution and use OAuth authorization only for the account that should perform them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/twitter-autopilot-aisa)
- [AISA](https://aisa.one)
- [AISA API Reference](https://docs.aisa.one/reference/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API/client responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; write and engagement actions require OAuth authorization.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
