## Description: <br>
Extract YouTube video transcripts from existing manual or auto-generated captions using yt-dlp, with optional timestamps and local SQLite caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mpbshhx](https://clawhub.ai/user/mpbshhx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when a user asks to extract captions, subtitles, or transcript text from a YouTube URL or video ID for reading, summarization, or search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes yt-dlp and contacts YouTube to retrieve available caption data. <br>
Mitigation: Install and run it only in environments where local yt-dlp execution and YouTube network access are acceptable. <br>
Risk: Cookies for restricted videos can act like login secrets. <br>
Mitigation: Keep cookies under ~/.config/yt-transcript/, restrict file access, and remove them when they are no longer needed. <br>
Risk: Cached transcripts may contain private or members-only content. <br>
Mitigation: Protect or delete the local transcript cache when handling sensitive videos. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mpbshhx/yt-transcript-yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON transcript segments by default, or newline-separated text when text mode is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcript entries may include timestamps, language, caption source, segment duration, and cached results.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
