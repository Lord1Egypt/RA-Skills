## Description:

A Sparki skill variant for TikTok-oriented short-video editing that guides agents through setup, API-key use, upload, prompt-driven editing, and command execution while preserving a viral TikTok pacing focus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and agents use this skill to turn local video assets into TikTok-style short videos with stronger hooks, faster pacing, and 9:16-oriented output through Sparki's remote video-editing workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads source videos and prompts to Sparki as part of a third-party remote editing workflow.

Mitigation: Use it only with video and prompt content that is approved for upload to Sparki.

Risk: API key storage and endpoint selection need review, especially when saving keys or using --base-url.

Mitigation: Prefer SPARKI_API_KEY for credentials and use the default endpoint unless a replacement endpoint is fully trusted.

Risk: Downloaded outputs can overwrite explicit paths and are not size-limited by the downloader.

Mitigation: Choose output paths deliberately, avoid critical filenames, and confirm available disk space before long runs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fischerlam/skills/tiktok-viral-editor-zh)
- [Sparki Homepage](https://sparki.io)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands; Sparki CLI commands emit JSON and may download edited video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SPARKI_API_KEY, uploads MP4 or MOV files to Sparki, and writes downloaded videos to a configured or explicit output path.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter, _meta.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
