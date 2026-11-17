## Description:

End-to-end TikTok ad video pipeline. Product script -> Veo base video -> animated caption overlay -> audio mix -> final MP4. One command, full automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT

## Use Case:

Developers and marketing operators use this skill to generate vertical TikTok product ad videos from product identifiers, script text, optional logos, and optional background audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe command and path handling could allow crafted inputs to run unintended commands or write outside the intended output folder.

Mitigation: Run only in a low-privilege disposable workspace with trusted inputs, validate paths and arguments before execution, and avoid exposing unrelated secrets in the environment.

Risk: The pipeline depends on local binaries and external video-generation credentials.

Mitigation: Confirm uv, ffmpeg, node, the dependent video-generation skill, and GEMINI_API_KEY are configured only in the intended execution environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-tiktok-video-pipeline)
- [Skill README](artifact/SKILL.md)
- [Assets README](artifact/assets/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with command examples and generated MP4 file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces final vertical MP4 videos under output/tiktok and may emit MEDIA path lines.]

## Skill Version(s):

2.0.0 (source: frontmatter, artifact metadata, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
