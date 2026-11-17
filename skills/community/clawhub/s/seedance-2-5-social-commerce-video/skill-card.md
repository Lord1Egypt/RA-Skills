## Description:

Creates traceable Seedance 2.5 social-commerce reply videos from a real, customer-provided, or clearly synthetic product question while preserving question source, privacy handling, approved answers, scope limits, disclosures, and product facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce, customer-support, and social-media teams use this skill to turn one approved product question into a short reply video for platforms such as Douyin, Xiaohongshu, Kuaishou, TikTok Shop, Instagram Reels, and similar channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed through shell history, logs, or overly permissive local configuration files.

Mitigation: Use an isolated Python environment, prefer the protected AI_HIVE_API_KEY environment variable or the script's chmod-protected config file, and avoid passing the key directly in logged shell commands.

Risk: Product images or motion references are uploaded to AI Hive during normal generation.

Mitigation: Upload only approved product media that is allowed to leave the local machine; use --preview first when reviewing the prompt and model selection without upload or billing.

Risk: Reply videos can overstate product facts, compatibility, pricing, availability, or disclosure status if inputs are incomplete.

Mitigation: Provide approved answer sources, scope limits for sizing or compatibility, market and expiry for price or availability claims, disclosure plans, and at least five continuity locks before generation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/seedance-2-5-social-commerce-video)
- [AI Hive OpenAPI Endpoint](https://ai-hive.iclip.cn/api/openapi/v1)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with bash command examples, CLI status output, preview JSON, and optional downloaded MP4 video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses approved product images and optional motion reference videos; preview mode shows the selected model, prompt, sources, and parameters without uploading media.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
