## Description:

Generates and edits Xiaohongshu ecommerce and brand-collaboration video assets, including product demos, shoppable notes, unboxing/review concepts, Pugongying collaborations, and Spotlight ad materials using Seedance through AI Hive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, brand teams, creators, and developers use this skill to plan, generate, edit, and check Xiaohongshu ecommerce videos grounded in real product facts, packaging, creator authorization, disclosure needs, and platform review requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API keys and uploaded commercial media through the AI Hive network service.

Mitigation: Install only when the AI Hive service and publisher are trusted, and use a dedicated low-privilege API key.

Risk: Custom base URL settings can redirect API traffic and media uploads to an untrusted endpoint.

Mitigation: Avoid custom --base-url or AI_HIVE_BASE_URL values unless the endpoint is fully trusted.

Risk: Generated files are written to a local output directory, which may affect important files if the directory is poorly chosen.

Mitigation: Use an isolated output directory for generated media and review files before reuse or publication.

Risk: Commercial product videos can become misleading if they add unsupported claims, reviews, prices, effects, or platform UI.

Mitigation: Ground prompts and final outputs in verified product facts, creator authorization, required disclosures, and current Xiaohongshu ecommerce and advertising rules.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wubin1836/skills/xiaohongshu-ecommerce-video-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files, JSON]

**Output Format:** [Markdown guidance with bash command examples, Python CLI commands, JSON task responses, and generated media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key; can upload user media to AI Hive and write generated files to a chosen output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
