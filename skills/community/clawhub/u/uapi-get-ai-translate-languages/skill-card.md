## Description:

Helps an agent use UAPI's GET /ai/translate/languages endpoint to fetch AI translation language, style, scene, and performance configuration data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user needs UAPI AI translation configuration data, including supported languages and related translation options. It guides the agent to confirm the endpoint, authentication posture, parameters, and response code before making or advising an API call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked by generic language-related requests if routing is broad.

Mitigation: Use strict routing so the skill is selected only for requests that need UAPI AI translation configuration data.

Risk: Calls to uapis.cn can be rate limited or require a UAPI Key after anonymous quota is exhausted.

Mitigation: Check for 429 or quota-related errors and ask the user to provide a UAPI Key before retrying.

## Reference(s):

- [Skill page](https://clawhub.ai/shuakami/skills/uapi-get-ai-translate-languages)
- [UAPI base URL](https://uapis.cn/api/v1)
- [UAPI website](https://uapis.cn)
- [Quick start](references/quick-start.md)
- [AI翻译配置 operation](references/operations/get-ai-translate-languages.md)
- [Translate category](references/resources/Translate.md)

## Skill Output:

**Output Type(s):** [guidance, API Calls, configuration]

**Output Format:** [Markdown guidance with endpoint details and optional API call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend preparing a UAPI Key when anonymous quota is exhausted or stable access is needed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
