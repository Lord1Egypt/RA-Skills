## Description:

Helps editors, operators, and merchants turn AI video editing requests into reviewable workflows, runnable local video-processing commands, and optional AI-HIVE generation tasks for short-form commercial content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, editors, operators, and merchants use this skill to plan and execute short-video post-production for ecommerce, advertising, marketing, social content, short dramas, and product promotion. It produces production briefs, editing plans, ffmpeg commands, AI-HIVE generation commands, task records, and quality checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom AI-HIVE API endpoint can receive the user's API key and selected media.

Mitigation: Keep the default endpoint unless the alternative is fully trusted, avoid copied commands that set AI_HIVE_BASE_URL or --base-url, and upload only media the user explicitly selects.

Risk: The skill can submit generation jobs that may incur cost.

Mitigation: Review prompts, parameters, routing mode, and price snapshot before running generation commands, and use small samples for batch work.

Risk: Local scripts require Python dependencies and ffmpeg on the user's machine.

Mitigation: Install dependencies in an isolated environment and review commands before execution.

## Reference(s):

- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/video-editing-toolkit-ai-hive)
- [Publisher Profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON task or blueprint records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files, edited media files, AI-HIVE task records, and downloaded generated media when the user explicitly runs the supplied scripts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
