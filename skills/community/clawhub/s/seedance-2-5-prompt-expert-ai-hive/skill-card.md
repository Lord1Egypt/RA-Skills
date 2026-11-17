## Description:

Helps creators, directors, and merchants turn Seedance 2.5 video ideas into production blueprints, storyboards, T2V/I2V/R2V prompts, AI-HIVE generation commands, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, directors, merchants, and agent users use this skill to plan commercial short-video production for e-commerce, advertising, marketing, social media, and story-driven content. It helps structure inputs, prompts, commands, task records, and quality checks before submitting potentially billable generation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI-HIVE API key and may use local media files.

Mitigation: Install only when comfortable granting that access, keep API keys out of logs and shared projects, and use placeholders in examples.

Risk: Generated commands may submit potentially billable media-generation work.

Mitigation: Review prompts, routing, parameters, and cost assumptions before execution; run small samples before batch work.

Risk: Custom base URLs or generated downloads can increase trust and handling risk.

Mitigation: Avoid custom base URLs unless the endpoint is fully trusted, review generated commands, and prefer no-download behavior for untrusted tasks.

## Reference(s):

- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include production briefs, storyboards, per-shot prompts, AI-HIVE task records, local video-editing commands, and acceptance checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
