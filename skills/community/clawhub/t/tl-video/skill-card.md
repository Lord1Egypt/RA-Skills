## Description:

Generate text-to-video and image-to-video clips with TensorsLab's AI video generation API, including prompt enhancement, progress tracking, and local result saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bob5-tensorslab](https://clawhub.ai/user/bob5-tensorslab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate short videos from text prompts or source images through TensorsLab. It helps agents choose model settings, track long-running generation, and save generated MP4 files locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script may download content from URLs returned by the remote API and write files outside the intended output folder.

Mitigation: Run in an isolated workspace with a low-privilege account, review outputs before reuse, and prefer a patched version that validates download URLs, enforces size limits, and sanitizes task IDs before writing files.

Risk: API credentials and uploaded source images are sent to a third-party video generation provider.

Mitigation: Set the API key through TENSORSLAB_API_KEY, avoid command-line secrets, and do not use sensitive source images unless the provider is trusted for the intended use.

## Reference(s):

- [TensorsLab Video API Reference](references/api_reference.md)
- [TensorsLab API](https://api.tensorslab.com)
- [TensorsLab Console](https://tensorslab.tensorslab.com/)
- [ClawHub Skill Page](https://clawhub.ai/bob5-tensorslab/skills/tl-video)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and local video file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated videos are saved as MP4 files in a configurable local output directory after asynchronous API polling.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
