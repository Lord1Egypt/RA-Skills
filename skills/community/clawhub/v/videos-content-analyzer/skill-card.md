## Description:

Analyzes online or local video content by extracting speech into cleaned text and using custom prompts to produce summaries, rewrites, quote extraction, shot lists, translations, and other video-content outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, content teams, and agents use this skill to turn video links or local video files into transcripts, summaries, reusable copy, translated text, meeting notes, and other prompt-directed content artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch user-provided URLs and upload selected or downloaded media to third-party destinations.

Mitigation: Use only trusted video URLs and non-sensitive files; require user confirmation before uploads and confirm acceptable upload hosts and retention behavior with the publisher.

Risk: Prompts, task IDs, filenames, selected videos, downloaded URL contents, and GUAIKEI_API_TOKEN are sent to or used with a third-party service.

Mitigation: Do not use the skill with confidential media or credentials outside approved environments; rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/videos-content-analyzer)
- [Server-resolved source repository](https://github.com/why20261/videos-content-analyzer)
- [Guaikei service site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown written to stdout, with progress and status messages written to stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; outputs depend on the selected video, task ID, and optional prompt.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
