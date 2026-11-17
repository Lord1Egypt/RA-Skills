## Description:

Helps Chinese-speaking video editors and marketing teams turn Seedance video editing or extension requests into reviewable production plans, AI-HIVE generation parameters, local editing commands, and delivery checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, ad post-production teams, and marketing operators use this skill to plan and execute Seedance video edits, extensions, AI fill shots, format changes, and delivery checks for commercial short-form content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use an AI-HIVE API key and store it in a local configuration file.

Mitigation: Prefer an environment variable or a dedicated limited API key, do not share real keys in prompts or logs, and review ~/.ai-hive/config.json after initialization.

Risk: Selected images, videos, or audio may be uploaded to AI-HIVE for generation workflows.

Mitigation: Upload only media that the user is authorized to use, and confirm privacy, copyright, trademark, and likeness rights before submitting tasks.

Risk: Video generation can create billable tasks and custom base URLs can redirect API traffic.

Mitigation: Review final prompts, model mode, routing, and pricing snapshots before execution; use small samples for batch work and avoid custom API endpoints unless fully trusted.

Risk: The shipped API helper includes broader AI-HIVE capabilities than the stated Seedance video workflow.

Mitigation: Use only the documented skill commands needed for video editing, extension, upload, task polling, and local ffmpeg processing unless the broader behavior has been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/seedance-video-extension-editor-ai-hive)
- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Base Endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON artifacts and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local blueprint JSON, ffmpeg commands, AI-HIVE task records, uploaded media identifiers, and downloaded generated media paths.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
