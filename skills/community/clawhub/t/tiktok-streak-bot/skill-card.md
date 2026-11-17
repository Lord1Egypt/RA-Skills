## Description:

Browser-automated TikTok streak messaging skill using Playwright that sends daily messages to configured usernames with state tracking, retry control, and optional content discovery via hashtags or keywords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrblackeg](https://clawhub.ai/user/mrblackeg)

### License/Terms of Use:

MIT-0

## Use Case:

External users who control their own TikTok account use this skill to automate one daily streak message to configured TikTok usernames, optionally sending discovered TikTok video links instead of text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored TikTok cookies can act like an active login session if exposed.

Mitigation: Keep cookies.json out of shared folders and source control, restrict local file access, and revoke the TikTok session if the file is exposed.

Risk: Scheduled or headless operation can send messages from the user's TikTok account without a final prompt.

Mitigation: Use only accounts and recipient lists you control, review configuration before execution, and avoid scheduled or headless sends unless unattended messaging is intended.

## Reference(s):

- [Overview](references/overview.md)
- [Architecture](references/architecture.md)
- [TikTok Selectors](references/selectors.md)
- [ClawHub Skill Page](https://clawhub.ai/mrblackeg/skills/tiktok-streak-bot)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Logs and JSON state files, with Markdown setup instructions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates state.json and cookies.json after execution.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
