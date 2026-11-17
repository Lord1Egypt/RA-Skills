## Description:

Provides agent guidance for signing up for and calling VCG's TranslateFlow API to translate text, documents, websites, and localized content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbennett111](https://clawhub.ai/user/jbennett111)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to route translation, localization, document translation, and language-detection requests through the TranslateFlow API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private, regulated, proprietary, unpublished, or account-related content may be sent to the external TranslateFlow/VCG service.

Mitigation: Review provider data handling and get appropriate approval before translating sensitive content; avoid submitting secrets or sensitive documents unless authorized.

Risk: The skill asks for an email address to create an API key and includes API-key-based request examples.

Mitigation: Confirm user consent before signup, store API keys securely, and avoid exposing keys in shared logs, prompts, or command history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jbennett111/skills/translateflow-api)
- [TranslateFlow API key endpoint](https://translateflow.vosscg.com/v1/keys)
- [TranslateFlow text translation endpoint](https://translateflow.vosscg.com/v1/translate)
- [TranslateFlow language list endpoint](https://translateflow.vosscg.com/v1/languages)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API signup steps, curl requests, API key handling guidance, and translated content returned by the external service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
