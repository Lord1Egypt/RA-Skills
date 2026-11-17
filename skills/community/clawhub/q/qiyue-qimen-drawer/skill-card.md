## Description:

用奇门遁甲起局看时机——按指定时间排出阳遁/阴遁局，展示值符值使、干支、空亡驿马与九宫盘面。由栖月 QiyueAstro 提供，无需 API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bloodymarygg](https://clawhub.ai/user/bloodymarygg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request a Qi Men Dun Jia chart for the current or a specified time, then present the returned core elements, summary, and nine-palace panel without independent interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Questions and selected dates may be sent to qiyueastro.com.

Mitigation: Avoid entering sensitive personal, business, or financial details in the question field.

Risk: Chart responses include a QiyueAstro promotional link.

Mitigation: Review generated responses before deployment where promotional links require disclosure or policy approval.

Risk: The skill depends on a third-party public API that may be unavailable or rate limited.

Mitigation: Use the documented fallback message for connection failures and avoid repeated retries after rate limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bloodymarygg/skills/qiyue-qimen-drawer)
- [QiyueAstro homepage](https://qiyueastro.com)
- [QiyueAstro Qi Men public API](https://qiyueastro.com/api/v1/openclaw/qimen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with structured chart fields, summary lines, and nine-palace panel entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a QiyueAstro promotional link and should not add independent fortune interpretation beyond returned API data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
