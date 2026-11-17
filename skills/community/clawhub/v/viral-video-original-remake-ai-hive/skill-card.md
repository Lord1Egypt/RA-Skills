## Description:

Helps e-commerce merchants, creative teams, and scaled content producers turn authorized reference videos and product materials into remake analyses, differentiated creative plans, shot-by-shot prompts, AI-HIVE generation tasks, and acceptance checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, e-commerce operators, marketing teams, and developers use this skill to plan original short-video remakes from authorized inputs, produce scripts and prompts, and optionally run AI-HIVE image or video generation workflows. It is intended for commercial content production where claims, permissions, cost-bearing generation, and final outputs remain subject to human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires an AI-HIVE API key that may be stored locally or supplied through the environment.

Mitigation: Use a dedicated API key, keep the local config file private, avoid logging or sharing the key, and rotate it if it may have been exposed.

Risk: Changing AI_HIVE_BASE_URL or passing --base-url can send credentials and media to an unintended endpoint.

Mitigation: Use only the intended AI-HIVE HTTPS endpoint and verify the endpoint before running commands that authenticate or upload media.

Risk: Video or image generation may upload user-provided media and may incur charges.

Mitigation: Confirm authorization, final prompts, routing mode, model choice, and budget before submitting generation tasks; start with a small sample for batch work.

Risk: Original-remake workflows can produce outputs that are too close to protected references or include unsupported product claims.

Mitigation: Use only authorized reference material, keep scripts and shot design materially distinct, and require factual review for brand, product, testimonial, platform, and performance claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/viral-video-original-remake-ai-hive)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown with inline bash commands and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local production briefs, query AI-HIVE model and pricing information, upload authorized media, poll asynchronous generation tasks, and download generated assets when the user provides an API key and approves cost-bearing work.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
