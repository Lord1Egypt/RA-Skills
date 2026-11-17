## Description:

Extracts plain-text transcripts from YouTube videos for review, analysis, and summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alti-systems](https://clawhub.ai/user/alti-systems)

### License/Terms of Use:

ISC

## Use Case:

Developers and agents use this skill to retrieve transcript text from a YouTube URL or video ID so video content can be summarized, quoted, or analyzed without manual viewing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented behavior and wrapper paths may not fully match the shipped scripts.

Mitigation: Review the installed package and confirm the wrapper path and selected transcript method before use.

Risk: The lockfile contains scanner-flagged vulnerable dependencies.

Mitigation: Review and update dependency versions before installing in a trusted or production environment.

Risk: YouTube URLs, video IDs, or API keys may be sent to YouTube, Supadata, or third-party transcript libraries.

Mitigation: Avoid sensitive or private video references and keep API keys only in trusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alti-systems/skills/yt-transcript)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text transcript, optionally with timestamped lines and brief video metadata depending on the script path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a YouTube URL or video ID and optional language code; transcript retrieval may contact YouTube, Supadata, or third-party transcript libraries.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
