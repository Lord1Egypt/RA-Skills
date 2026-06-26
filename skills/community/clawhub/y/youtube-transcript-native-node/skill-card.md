## Description: <br>
Extracts clean plain-text or JSON transcripts from existing YouTube captions using native Node.js and a local yt-dlp binary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwestburg](https://clawhub.ai/user/jwestburg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user provides a YouTube URL and needs existing captions extracted for summarization, quoting, research triage, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-directed external queries may disclose sensitive information to a third-party service. <br>
Mitigation: Do not use the skill for secrets, private incident details, internal hostnames, client identifiers, or confidential research unless that disclosure is intentionally approved. <br>
Risk: The artifact invokes a local external binary and accesses YouTube through yt-dlp. <br>
Mitigation: Use only with a trusted yt-dlp installation on PATH and avoid privacy-sensitive videos or contexts when external access is inappropriate. <br>


## Reference(s): <br>
- [YouTube Transcript Contract](artifact/references/youtube-transcript-contract.md) <br>
- [ClawHub skill page](https://clawhub.ai/jwestburg/youtube-transcript-native-node) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text transcript, timestamped plain text, or JSON with URL, title, language, auto-caption status, timestamp setting, and transcript.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and yt-dlp on PATH; extracts captions only and does not transcribe audio or download audio/video.] <br>

## Skill Version(s): <br>
1.1.4 (source: evidence.json release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
