## Description:

Monitor available TestFlight beta slots with smart app lookups and silent batch checking. Get alerted when slots open up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jon-xo](https://clawhub.ai/user/jon-xo)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to monitor one or more trusted Apple TestFlight beta URLs, resolve join codes to readable app names, and receive alerts only when seats become available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill can save and repeatedly fetch arbitrary URLs instead of only TestFlight links.

Mitigation: Use it only with TestFlight URLs you personally trust, avoid shared batch configuration files, and prefer versions that strictly validate https://testflight.apple.com/join/<code> URLs and disable unsafe redirects before scheduled checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jon-xo/skills/testflight-monitor)
- [awesome-testflight-link lookup data](https://github.com/pluwen/awesome-testflight-link)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown and terminal text with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch checks are designed to stay silent unless a monitored TestFlight URL changes from full or unknown to available.]

## Skill Version(s):

1.0.1 (source: server release metadata and manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
