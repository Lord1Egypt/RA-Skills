## Description:

Search and download licensed music from Trackyard's AI-powered catalog for videos, social content, podcasts, and other projects needing royalty-free tracks, with natural-language search, smart audio trimming, and filters for genre, mood, BPM, vocals, energy, and instruments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benny-conn](https://clawhub.ai/user/benny-conn)

### License/Terms of Use:


## Use Case:

Developers, creators, and media-production teams use this skill to search Trackyard's licensed catalog, select tracks that match a content brief, and download full or trimmed MP3 clips for social videos, ads, podcasts, demos, and related content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires network access to Trackyard using a Trackyard API key.

Mitigation: Install only when Trackyard API access is expected, provide the API key through the TRACKYARD_API_KEY environment variable, and avoid exposing the key in shared logs or shell history.

Risk: The download command can write to a caller-supplied writable path without containment or overwrite protection.

Mitigation: Run downloads from a safe working directory, prefer the default filename, avoid absolute or parent-directory output paths, and review downloaded file destinations before execution.

## Reference(s):

- [Trackyard](https://trackyard.com)
- [Trackyard ClawHub Skill](https://clawhub.ai/benny-conn/skills/trackyard)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; Trackyard API responses as JSON; downloaded music as MP3 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and TRACKYARD_API_KEY. Search and download operations consume Trackyard credits; account and usage checks return JSON.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
