## Description:

Helps merchants and marketers turn Seedance product-video requests into product-accurate scripts, shot plans, AI-HIVE video-generation tasks, platform variants, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, marketers, and content teams use this skill to plan and run product-video workflows for ecommerce, advertising, livestream commerce, and social content. It helps transform authorized product assets and factual selling points into reviewable scripts, prompts, AI-HIVE tasks, delivery records, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI-HIVE API token can be sent to an arbitrary configured API base URL.

Mitigation: Use only the default AI-HIVE endpoint, do not set --base-url or AI_HIVE_BASE_URL to an untrusted host, and rotate the API key if it may have been used with an unknown endpoint.

Risk: Selected media may be uploaded to AI-HIVE and generation requests may incur charges.

Mitigation: Confirm final prompts, model mode, routing, budget, and media authorization before executing generation or upload commands; use a small sample before batch work.

Risk: Product videos can contain misleading claims, unauthorized references, or platform compliance issues if source facts and rights are not checked.

Mitigation: Use factual product inputs, authorized media, human review, and the included acceptance checklist before publishing generated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-product-video-studio-ai-hive)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE default API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with runnable command snippets, JSON task records, scripts, prompts, shot lists, and quality checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files, submit AI-HIVE generation tasks, upload selected media, poll task status, and download generated media when the user confirms execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
