## Description:

Create and edit Temu product catalog videos, factory demonstrations, assembly guides, variant clips and multi-market adaptations using Seedance generation and editing through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace sellers, ecommerce operators, and developers use this skill to generate or edit traceable product catalog videos, SKU variants, assembly guides, factory footage recuts, and localized market adaptations from verified product records and source media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A stored AI Hive API key can be sent to any configured API URL if the base URL is changed.

Mitigation: Use only trusted --base-url, AI_HIVE_BASE_URL, and config-file base_url values, verify the endpoint before use, and rotate the API key if it may have been used with an untrusted endpoint.

Risk: The skill depends on an external AI Hive service and the requests package at runtime.

Mitigation: Install dependencies in an isolated environment, pin dependency versions where possible, and confirm the configured endpoint remains the official service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/temu-ecommerce-video-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash commands and generated video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated tasks can download media outputs locally or return task status when --no-download is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
