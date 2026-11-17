## Description:

This skill helps agents plan and generate Seedream 5.0 Lite advertising images through AI Hive while checking that visual claims, proof points, calls to action, and landing-page content match.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, ecommerce operators, and developers use this skill to create advertising image prompts and AI Hive commands that keep products, evidence, claims, and destination-page content aligned across common paid media channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference images, and generated outputs are sent to AI Hive.

Mitigation: Use the skill only with content suitable for that service and avoid sensitive campaign, customer, or unreleased product data.

Risk: The evidence security summary reports downloader path handling that may write outside the chosen output folder.

Mitigation: Use a constrained output directory and review or patch downloader path handling before routine use.

Risk: Generated ad images may imply claims, discounts, certifications, inventory, or product attributes that the landing page does not support.

Mitigation: Review the message-match chain, landing page, platform policy, and approved copy before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedream-5-lite-ad-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and downloaded image files from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are created through the fixed public_model_seedream_5_0_lite model and can be downloaded to a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
