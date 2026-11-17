## Description:

Seedance 图生视频工作室｜AI-HIVE helps creators and merchants turn authorized product images, posters, or character references into reviewable image-to-video briefs, prompts, AI-HIVE commands, task records, and acceptance checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, merchants, and content teams use this skill to plan and optionally execute Seedance-style image-to-video workflows for ecommerce, advertising, marketing, social video, short drama, and character-based content. It emphasizes authorized source media, stable subject and product appearance, prompt design, task tracking, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an AI-HIVE API key and upload selected media to AI-HIVE.

Mitigation: Use a limited and rotatable API key, upload only media the user is authorized to use, and avoid exposing keys in files, logs, screenshots, or version control.

Risk: Generated or user-edited commands can point AI_HIVE_BASE_URL or --base-url at a custom endpoint.

Mitigation: Keep the default AI-HIVE endpoint unless the alternate endpoint is fully trusted, and review commands before running them.

Risk: The video script downloads generated outputs to local storage, and the security guidance notes that filenames should be sanitized before writes.

Mitigation: Use a dedicated output directory, inspect output paths before execution, and treat downloaded files cautiously.

Risk: The workflow can be misused for unauthorized content replication, false product claims, fake testimonials, or platform rule evasion.

Mitigation: Require rights to source media, preserve only abstract structure from references when rights are unclear, and verify factual claims before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-image-to-video-studio-ai-hive)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured Chinese sections, inline shell commands, JSON task records, and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE routing choices, pricing snapshots, task IDs, status notes, and local file paths when the user approves generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
