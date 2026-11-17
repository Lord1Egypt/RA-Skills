## Description:

WiseDiag-Skin uploads a local skin photo to WiseDiag AI and returns reference-only analysis of possible skin conditions and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wisediag](https://clawhub.ai/user/wisediag)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit a local skin image and optional question to WiseDiag AI for reference-only condition analysis and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skin photos and related questions are sent to WiseDiag's cloud service for analysis.

Mitigation: Install and run only when remote processing is acceptable, verify WiseDiag's privacy policy independently, and avoid uploading private or unnecessary identifying content.

Risk: The skill requires a WiseDiag API key.

Mitigation: Use a temporary environment variable where practical and avoid storing the key in shared shell profiles, logs, or project files.

Risk: Custom output names or directories can write reports outside the default workspace.

Mitigation: Avoid untrusted --name or --output values and constrain output paths before broader deployment.

Risk: The returned analysis concerns health symptoms and may be incomplete or incorrect.

Mitigation: Treat results as reference-only guidance and consult a qualified healthcare professional for medical concerns.

## Reference(s):

- [WiseDiag-Skin ClawHub listing](https://clawhub.ai/wisediag/skills/wisediag-skin)
- [WiseDiag API key management](https://console.wisediag.com/apiKeyManage)
- [WiseDiag API service host](https://openapi.wisediag.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Streaming terminal text and a saved Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WISEDIAG_API_KEY; uploads one local image file and writes a Markdown result file.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
