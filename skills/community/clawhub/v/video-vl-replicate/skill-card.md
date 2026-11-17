## Description:

Analyzes short videos into aligned visual, transcript, and subtitle timelines, then helps generate adapted viral-style rewrite scripts from the analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyangwuye](https://clawhub.ai/user/fanyangwuye)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and agents use this skill to dissect short-video structure, align narration, subtitles, and keyframes into a timeline, and generate adapted scripts for derivative short-form content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs first-run network setup, dependency installation, and large model downloads under the user's account.

Mitigation: Install and run it in a reviewed environment; pin or review dependencies before production use.

Risk: The pipeline can fetch content from user-provided URLs.

Mitigation: Use only public or approved URLs that are intended to be downloaded and processed.

Risk: The pipeline writes and may overwrite files in the configured output directory.

Mitigation: Use a new empty work directory for each run and avoid pointing output at valuable existing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanyangwuye/skills/video-vl-replicate)
- [Publisher profile](https://clawhub.ai/user/fanyangwuye)
- [Prompt templates](references/prompt_templates.md)
- [Python dependencies](requirements.txt)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON analysis artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces analysis.json and may create extracted audio and keyframe files in the selected work directory.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
