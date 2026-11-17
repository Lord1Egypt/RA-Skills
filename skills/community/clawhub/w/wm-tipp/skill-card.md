## Description:

Generates FIFA World Cup 2026 tips with Polymarket odds and sends daily Telegram messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcbuer](https://clawhub.ai/user/jcbuer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate scheduled German-language FIFA World Cup 2026 match tips with market odds and deliver them to configured Telegram recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated World Cup tip messages may be sent to unintended Telegram recipients if WM_CHAT_IDS is misconfigured.

Mitigation: Keep WM_CHAT_IDS limited to intended recipients and review the recipient list before scheduled execution.

Risk: An untrusted Telegram gateway could receive generated message content or route messages unexpectedly.

Mitigation: Set WM_TELEGRAM_API only to a trusted Telegram gateway endpoint.

Risk: Pointing WM_SKILL_DIR at a sensitive directory changes where the skill reads and writes its schedule, tips, and cache files.

Mitigation: Set WM_SKILL_DIR only to the intended skill directory and avoid sensitive filesystem locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcbuer/skills/wm-tipp)
- [Polymarket Gamma markets API](https://gamma-api.polymarket.com/markets)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Telegram Markdown text with optional shell configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON schedule and tip data, a one-hour Polymarket cache, and configured Telegram recipients.]

## Skill Version(s):

1.0.1 (source: release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
