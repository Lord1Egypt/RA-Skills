## Description:

Converts YouTube videos into batches of short-form Spanish script drafts using FÓRMULA 100K frameworks, transcript extraction, and viral-reference checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social-media teams, and marketing operators use this skill to repurpose YouTube videos into 8 to 12 short-form script ideas and finished scripts adapted to their audience. The workflow helps extract or collect a transcript, identify high-potential moments, verify viral patterns, and organize a script batch for recording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Instagram connector can publish live content from a connected account.

Mitigation: Do not connect or use Instagram publishing unless direct posting is intended; require explicit approval for each post, including the target account, media, and caption.

Risk: The workflow may save generated scripts locally and send them through Telegram.

Mitigation: Install only in environments where local script storage and Telegram delivery are acceptable for the user's content and privacy requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/transcripcion-youtube-formula100k)
- [Proceso de Guion](references/proceso-guion.md)
- [MCPs Opcionales](references/mcps-opcionales.md)
- [yt-transcript-mcp connector](https://yt-transcript-mcp--alex2zimmermann-ux.run.tools)
- [Optional YouTube MCP connector](https://youtube-mcp--sfiorini.run.tools)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured analysis, script ideas, script drafts, and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown files under guiones/ and summarize or send them through Telegram when running in the OpenClaw environment.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
