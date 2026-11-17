## Description:

Extract transcripts from all videos in a YouTube channel for free, using yt-dlp to discover videos and fetch available subtitles, then saving combined transcripts as structured JSON or CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otomazeli](https://clawhub.ai/user/otomazeli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect available subtitles from every video in a YouTube channel or playlist and export the transcripts as a local dataset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local shell wrapper has unsafe input and temporary-file handling that could damage local files.

Mitigation: Review or patch the script before shared or automated use, avoid untrusted parameter values, and run it with a dedicated output directory.

Risk: The skill depends on local execution of yt-dlp against YouTube content.

Mitigation: Install only when comfortable running a local shell wrapper around yt-dlp, and prefer JSON output for easier review and downstream validation.

## Reference(s):

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ClawHub skill page](https://clawhub.ai/otomazeli/skills/youtube-full-channel-transcripts)

## Skill Output:

**Output Type(s):** [Files, Text, JSON, CSV]

**Output Format:** [Local transcripts.json or transcripts.csv file plus a console summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp, jq, and network access to YouTube; skips videos with no available transcript.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
