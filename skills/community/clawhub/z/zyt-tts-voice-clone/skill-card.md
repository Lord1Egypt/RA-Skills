## Description:

Use Chanjing TTS API to synthesize speech from text, using user-provided voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyuting214](https://clawhub.ai/user/zuoyuting214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create Chanjing custom voices from public reference audio URLs and generate speech from text with optional speech-rate and timestamp support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a Chanjing app_id and secret_key.

Mitigation: Keep the credential file private, use a dedicated Chanjing credential where possible, and avoid sharing cached tokens.

Risk: Reference voice audio URLs and synthesis text are sent to Chanjing's API.

Mitigation: Avoid sensitive text and only use voice samples that are authorized for cloning and synthesis.

## Reference(s):

- [Chanjing Open API](https://open-api.chanjing.cc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Chanjing voice IDs, task IDs, status results, and generated audio download URLs when used with valid credentials.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
