## Description:

Search and analyze your own session logs (older/parent conversations) using jq.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect local OpenClaw session history when a user asks about prior chats, parent conversations, historical context, message contents, costs, or tool usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session logs may contain sensitive personal content, credentials, API keys, or tokens.

Mitigation: Confirm the requested scope before broad searches, keep processing local, and report secret presence without displaying secret values.

Risk: Unfiltered searches across all sessions can expose conversation patterns or content the user did not intend to review.

Mitigation: Prefer a specific session, date, or phrase, and require user confirmation before all-session searches.

Risk: Session log contents could be exfiltrated if piped or redirected to network-transmitting commands.

Mitigation: Do not send session log contents through curl, wget, nc, scp, ssh, or similar network tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/session-logs-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/session-logs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local jq and rg availability; outputs should stay local and avoid displaying credentials or tokens found in logs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
