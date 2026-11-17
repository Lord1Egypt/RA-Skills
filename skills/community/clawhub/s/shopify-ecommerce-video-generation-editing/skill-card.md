## Description:

Create and edit Shopify PDP videos, homepage hero loops, DTC product stories, collection clips and paid-social adaptations with AI Hive video-generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ecommerce operators, and brand content teams use this skill to plan, generate, edit, extend, and adapt product videos for Shopify PDPs, homepage hero loops, collections, paid social, and retention channels. It helps keep product facts, brand voice, crops, and channel-specific handoff requirements consistent across video variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-selected prompts and product media to the AI Hive service.

Mitigation: Only provide product media, prompts, and brand assets that are approved for processing by AI Hive.

Risk: The skill stores an AI Hive API key in local configuration when initialized.

Mitigation: Install and run the skill in a virtual environment, restrict local credential access, and use environment or CLI credentials when that better matches policy.

Risk: Video generation may incur account charges.

Mitigation: Review live AI Hive pricing and routing choices before submitting generation jobs.

Risk: Unpinned Python dependencies can change behavior over time.

Mitigation: Pin the requests dependency in controlled deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/shopify-ecommerce-video-generation-editing)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API service](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash command examples; generated tasks can return JSON status and downloaded media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports t2v, i2v, r2v, edit, and extend modes; output directory, routing, model parameters, and submit-only behavior are configurable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
