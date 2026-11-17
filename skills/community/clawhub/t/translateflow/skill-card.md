## Description:

TranslateFlow provides AI translation through the TranslateFlow API for multilingual translation, localization, tone adaptation, and batch translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbennett111](https://clawhub.ai/user/jbennett111)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to translate text, localize content, adapt tone, and batch translate strings for documents or applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Translation text, email addresses, and API keys may be sent to an external service.

Mitigation: Do not send confidential text unless the external service is trusted for the intended use case.

Risk: The helper script can expose newly created API keys in logged environments.

Mitigation: Use a pre-created TRANSLATEFLOW_API_KEY and avoid TRANSLATEFLOW_EMAIL auto-signup where command output or logs are retained.

Risk: A configurable API URL can redirect keys, email, and translation text to an arbitrary endpoint.

Mitigation: Avoid setting TRANSLATEFLOW_API_URL except in a controlled development environment.

## Reference(s):

- [TranslateFlow ClawHub skill page](https://clawhub.ai/jbennett111/skills/translateflow)
- [TranslateFlow API key endpoint](https://anton.vosscg.com/v1/keys)
- [TranslateFlow translate endpoint](https://anton.vosscg.com/v1/translate)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash snippets and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TranslateFlow API key and sends translation requests to an external API service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
