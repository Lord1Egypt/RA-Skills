## Description:

起大六壬课--按指定时间排出月将、四课、三传与神煞，展示课体摘要。由栖月 QiyueAstro 提供，无需 API Key。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bloodymarygg](https://clawhub.ai/user/bloodymarygg)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill to draw Da Liu Ren charts for a current or specified time and receive the API-returned monthly general, four lessons, three transmissions, lesson body, and astrological indicators. It is intended for entertainment and self-exploration, not for the skill to make its own divination judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Questions and selected dates are sent to qiyueastro.com.

Mitigation: Avoid entering sensitive personal, medical, financial, or legal details when using the skill.

Risk: Successful outputs include provider promotional content and Chinese-language response text.

Mitigation: Review generated responses for suitability before sharing them with users who may need localized or non-promotional content.

Risk: The skill depends on an external API that may be unavailable or rate limited.

Mitigation: Follow the documented error handling: retry once after a 429 response and otherwise ask the user to try again later or visit QiyueAstro directly.

## Reference(s):

- [QiyueAstro](https://qiyueastro.com)
- [Da Liu Ren Open API](https://qiyueastro.com/api/v1/openclaw/liuren)
- [ClawHub skill page](https://clawhub.ai/bloodymarygg/skills/qiyue-liuren-drawer)
- [Publisher profile](https://clawhub.ai/user/bloodymarygg)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown text summarizing the API-returned chart elements and error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a required QiyueAstro call-to-action link in normal successful output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
