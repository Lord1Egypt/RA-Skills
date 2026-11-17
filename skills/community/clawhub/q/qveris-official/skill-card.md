## Description:

QVeris Official lets agents discover specialized API tools by capability and call selected tools for structured data, generation, extraction, and processing tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linfangw](https://clawhub.ai/user/linfangw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route tasks to QVeris-discovered APIs when native tools are missing, especially for structured data, media generation, OCR, translation, web extraction, PDF workflows, weather, finance, and similar external capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Capability queries and selected tool parameters are sent to qveris.ai using the user's API key.

Mitigation: Avoid sensitive personal, credential, or confidential business data unless that external transmission is intended.

Risk: The skill requires a QVERIS_API_KEY for authenticated external API access.

Mitigation: Protect the API key as a secret, scope and rotate it according to local policy, and revoke it if exposure is suspected.

Risk: Discovery returns candidate API tools rather than factual answers, so using it for direct fact lookup can produce inappropriate tool selection.

Mitigation: Use QVeris discovery for capability selection, inspect selected tools before calling them, and use web search for factual or qualitative information lookups.

## Reference(s):

- [QVeris homepage](https://qveris.ai)
- [ClawHub skill page](https://clawhub.ai/linfangw/skills/qveris-official)
- [Publisher profile](https://clawhub.ai/user/linfangw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API responses or shell commands when script execution is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QVERIS_API_KEY; sends capability queries and selected tool parameters to qveris.ai.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
