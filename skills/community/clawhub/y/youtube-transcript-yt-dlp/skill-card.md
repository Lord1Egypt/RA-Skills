## Description: <br>
Extract YouTube video transcripts from existing captions (manual or auto-generated) using yt-dlp, with optional timestamps and local SQLite caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ItzSubhadip](https://clawhub.ai/user/ItzSubhadip) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to turn a YouTube URL or video ID into transcript text or JSON segments for summarization, search, or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports dormant third-party transcript-provider code despite the skill describing YouTube-only network behavior. <br>
Mitigation: Review before installing when YouTube-only network behavior is required; the publisher should remove or clearly disclose dormant provider code. <br>
Risk: Optional YouTube cookies are sensitive credentials, and the local SQLite cache can retain transcript history. <br>
Mitigation: Provide cookies only when necessary, keep them outside the skill directory, restrict file permissions, and treat the cache as user activity history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ItzSubhadip/youtube-transcript-yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON transcript segments or newline-separated plain text, with optional timestamps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and yt-dlp; supports optional Netscape cookies.txt input and local SQLite transcript caching.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
