## Description:

Toonany helps creators turn novels and stories into AI-generated short dramas through guided story, script, storyboard, media generation, and post-production workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casperkwok](https://clawhub.ai/user/casperkwok)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and media teams use Toonany to convert written stories into short drama projects with generated storylines, outlines, scripts, storyboards, images, video clips, audio, subtitles, and final edited episodes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-configurable API endpoints or returned URLs could receive paid service credentials.

Mitigation: Review project.json before use, especially baseUrl fields, avoid projects from untrusted sources, and use limited-scope or disposable API keys where possible.

Risk: Creative manuscripts and prompts may be processed by third-party model providers.

Mitigation: Use only content approved for external processing and confirm provider terms before entering confidential manuscripts.

Risk: API keys stored directly in project files can be exposed through sharing or logs.

Mitigation: Prefer environment-variable configuration and do not print or share full API keys during setup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/casperkwok/skills/toonany)
- [Data Model Reference](references/data-model.md)
- [Production Workflow Reference](references/workflow.md)
- [Model Configuration Guide](references/model-config.md)
- [Command Reference](references/commands.md)
- [DeepSeek API Keys](https://platform.deepseek.com/api_keys)
- [Volcengine Ark Console](https://console.volcengine.com/ark/)
- [Kling AI](https://klingai.com/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Media files, Guidance]

**Output Format:** [Markdown, JSON project files, generated media assets, subtitles, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates project directories under output/{project-name}; media generation depends on configured third-party provider APIs and ffmpeg.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter and changelog show 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
