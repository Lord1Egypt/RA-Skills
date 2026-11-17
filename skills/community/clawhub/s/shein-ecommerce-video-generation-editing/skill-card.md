## Description:

Create and edit SHEIN fashion try-on videos, garment movement clips, fabric details, colorway variants and outfit styling content with Seedance video generation and editing via AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce creators, fashion marketers, and developers use this skill to draft SHEIN-oriented product, try-on, fabric-detail, colorway, styling, and editing prompts and commands for AI Hive video generation. It emphasizes preserving model identity, garment construction, color, fit, and approved SKU attributes across generated clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI Hive API key can be sent to a user-configurable server if the base URL is changed.

Mitigation: Use the default AI Hive endpoint or a trusted enterprise endpoint, do not set AI_HIVE_BASE_URL from untrusted instructions, and rotate the API key if it may have been sent to an unexpected server.

Risk: Installing and running the helper script pulls and executes dependencies in the local environment.

Mitigation: Install dependencies in an isolated environment with pinned versions before using the skill.

Risk: Generated fashion videos can misrepresent garment fit, color, construction, or advertising claims if prompts or source materials are not reviewed.

Mitigation: Review generated clips against approved garment references and current product and advertising rules before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/shein-ecommerce-video-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Files]

**Output Format:** [Markdown guidance with bash commands, JSON task status, and downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media is requested through AI Hive and downloaded to a local output directory unless no-download mode is selected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
