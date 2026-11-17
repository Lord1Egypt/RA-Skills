## Description:

Scenario-focused Sparki skill for presenter-led and talking-head edits while using official Sparki setup, API-key, and upload workflow guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to guide Sparki workflows for tightening presenter videos, direct-to-camera footage, interviews, tutorials, founder videos, and explainers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store a Sparki API key and use it for future requests.

Mitigation: Prefer environment-based secret handling or restrictive config-file permissions for the API key.

Risk: A persisted custom service endpoint could receive future uploads.

Mitigation: Avoid using --base-url unless the endpoint is fully trusted.

Risk: Selected videos and prompts are sent to Sparki for processing.

Mitigation: Use the skill only when the user intends to send the selected media and prompt content to Sparki.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fischerlam/skills/talking-head-editor)
- [Sparki Homepage](https://sparki.io)
- [Sparki Telegram Upload](https://t.me/Sparki_AI_bot/upload)
- [Sparki API Endpoint](https://agent-api.sparki.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of local file paths or Telegram Mini App uploads; generated video assets are produced by Sparki outside the skill.]

## Skill Version(s):

1.0.12 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
