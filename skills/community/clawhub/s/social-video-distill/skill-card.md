## Description:

Distill public social-video and short-form media with AI-first delegation for transcripts, summaries, humor reads, best lines, caption ideas, and theme extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[little7unifai](https://clawhub.ai/user/little7unifai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn public social-video clips, local clips, captions, transcripts, or rough notes into concise summaries, transcript-grounded takeaways, humor analysis, best-line extraction, caption ideas, or thematic synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, transcripts, notes, and browser AI interactions may be sent to Gemini or NotebookLM.

Mitigation: Use only public or non-sensitive clips and source material unless the user is comfortable sharing that content with the browser AI service.

Risk: Browser automation accepts configurable browser and app endpoints.

Mitigation: Run automation in a dedicated local browser profile and avoid remote CDP endpoints or custom app URLs.

Risk: Media retrieval can process arbitrary video URLs and create local downloads.

Mitigation: Avoid private or internal media URLs, download only when necessary, and clean downloaded media and caption files after use.

Risk: Runtime installation uses mutable package installs for yt-dlp and puppeteer-core.

Mitigation: Review installation steps before use and consider pinning dependencies in controlled deployments.

## Reference(s):

- [Prompt patterns](references/prompts.md)
- [Troubleshooting](references/troubleshooting.md)
- [Gemini web app](https://gemini.google.com/app)
- [ClawHub skill page](https://clawhub.ai/little7unifai/skills/social-video-distill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise distillations, transcript notes, caption ideas, and inline shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates directly supported transcript evidence from inference when source quality is uncertain.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
