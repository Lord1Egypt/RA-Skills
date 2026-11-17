## Description:

Downloads YouTube videos as high-quality MP4 files, saves them as OpenClaw video assets, and records them in the asset registry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honeybee1130](https://clawhub.ai/user/honeybee1130)

### License/Terms of Use:


## Use Case:

External users and developers use this skill when they want an agent to download a provided YouTube URL, label the result, save it as an MP4 asset, and update the OpenClaw registry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weak URL validation could allow crafted inputs to download from unintended sites.

Mitigation: Validate hostnames against supported YouTube domains and accept only canonical YouTube video ID formats before invoking the downloader.

Risk: Weak filename and path handling could allow files to be saved outside the intended video asset folder.

Mitigation: Apply path containment checks after filename construction and reject outputs whose resolved path is not under the configured asset video directory.

Risk: Untrusted or unusually large sources could create operational or storage risk.

Mitigation: Add reasonable source and file-size controls before use with untrusted URLs or users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/honeybee1130/skills/yt-downloader)

## Skill Output:

**Output Type(s):** [Shell commands, Files, JSON]

**Output Format:** [Shell command execution with MP4 file output and JSON registry entry]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves MP4 videos under ~/.openclaw/workspace/assets/videos and records downloads in registry.json when jq is available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
