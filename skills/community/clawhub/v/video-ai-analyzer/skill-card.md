## Description:

Video AI Analyzer helps agents transcribe and analyze local or linked videos, then generate summaries, rewrites, quotes, storyboards, translations, and other reusable content from custom prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, content teams, and developers use this skill to turn video URLs or local video files into clean transcripts and prompt-directed content such as summaries, meeting notes, social-media copy, quotes, and translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can download arbitrary URLs, which may expose private network resources or consume local disk.

Mitigation: Use only trusted public video URLs or vetted local files, avoid private or internal URLs, and apply deployment-level file size and network egress controls.

Risk: Selected local videos are uploaded to the external provider for processing.

Mitigation: Do not submit sensitive or restricted media unless provider processing is approved for that data, and treat provider retention promises as policy claims that the client cannot enforce.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/why20261/skills/video-ai-analyzer)
- [Server-Resolved Source Provenance](https://github.com/why20261/video-ai-analyzer)
- [GuaiKei Video Text Extraction Service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown-style prose printed to stdout; progress and diagnostics are written separately to stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected video, GUAIKEI_API_TOKEN, and optional custom prompt.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and package.json declare 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
