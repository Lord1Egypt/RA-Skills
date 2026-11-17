## Description:

This skill helps creators, brand editors, and subtitle teams analyze short-video captions and spoken copy, then produce caption hierarchy, keyword emphasis, rewritten copy, CTA options, prompts, runnable AI-HIVE commands, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brand editors, subtitle editing teams, and developers use this skill to turn video captions or transcripts, brand voice, platform constraints, and prohibited terms into production-ready Chinese short-video copy workflows. It supports content analysis, original adaptation planning, AI-HIVE media generation commands, and acceptance checks for ecommerce, advertising, marketing, short drama, and social content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE uploads or generation requests may expose media and consume paid credits.

Mitigation: Require explicit user confirmation before uploads or generation, use a limited AI-HIVE API key, and keep API keys out of chat logs and project files.

Risk: Custom API base URLs can redirect sensitive media or credentials to an endpoint the user does not control.

Mitigation: Use the default AI-HIVE API base unless the endpoint is fully controlled and reviewed.

Risk: The analyzer branding may understate the skill's ability to upload, generate, poll, and download media.

Mitigation: Review the skill before installing and disclose media-generation behavior before running commands.

## Reference(s):

- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Base](https://ai-hive.iclip.cn/api)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/viral-video-caption-copy-analyzer-ai-hive)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON files and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task records with route, model, price snapshot, taskId, status, and local file paths when generation is performed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
