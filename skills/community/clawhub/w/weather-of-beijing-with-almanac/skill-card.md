## Description:

Gets Beijing's next-day weather forecast and Chinese almanac details, then sends a daily Feishu notification with temperature-change and rain reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiaojie-1012](https://clawhub.ai/user/lixiaojie-1012)

### License/Terms of Use:


## Use Case:

External users and automation builders use this skill to prepare and send a Beijing next-day weather and almanac notification through Feishu, including rain and temperature-change reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated or manually triggered runs can send weather and almanac messages to a configured Feishu recipient.

Mitigation: Configure the Feishu openid deliberately and narrow manual triggers or add confirmation before sending.

Risk: Almanac API credentials may be required for the preferred holiday API path.

Mitigation: Store app_id and app_secret outside shared prompts or public logs and use the no-key search fallback when credentials are not available.

Risk: Delivered messages include a fixed attribution footer.

Mitigation: Remove or edit the footer before deployment if that attribution is not wanted in user-facing notifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lixiaojie-1012/skills/weather-of-beijing-with-almanac)
- [wttr.in Beijing JSON endpoint](https://wttr.in/Beijing?format=j1)
- [mxnzp holiday API endpoint](https://www.mxnzp.com/api/holiday/single/${TOMORROW}?ignoreHoliday=false&app_id=your_app_id&app_secret=your_secret)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown notification text with inline shell commands and configuration placeholders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, a Feishu openid, and optional almanac API credentials; produces Beijing-focused weather and almanac content for Asia/Shanghai daily scheduling.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
