## Description: <br>
Create, produce, and schedule UGC-style short-form video reels at scale, including sourcing UGC reaction hooks, analyzing app demos, assembling reels with ffmpeg, publishing via Post-Bridge, and tracking performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jjjohny228](https://clawhub.ai/user/jjjohny228) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to plan, produce, and schedule short-form UGC-style reels from reaction hooks, app demo clips, captions, music, and analytics feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend DanSUGC credits when purchasing UGC clips or analytics requests. <br>
Mitigation: Set an explicit budget, check balances before purchases, and require manual approval for each purchase or paid analytics request. <br>
Risk: The skill can upload videos to third-party services and schedule public social posts. <br>
Mitigation: Use only non-sensitive videos, approve each upload and scheduled post manually, and restrict actions to named social accounts. <br>
Risk: Preflight steps may install packages or download fonts on the local system. <br>
Mitigation: Review and approve installation commands and third-party downloads before running them; do not allow automatic sudo or package-manager execution. <br>
Risk: API keys for Gemini, DanSUGC, and Post-Bridge may grant access to paid services or connected accounts. <br>
Mitigation: Use revocable keys with limited scope where available, keep keys out of logs, and rotate credentials after testing or suspected exposure. <br>


## Reference(s): <br>
- [ReelClaw homepage](https://github.com/dansugc/reelclaw) <br>
- [Tool Setup Guide](references/tools-setup.md) <br>
- [Green Zone Reference](references/green-zone.md) <br>
- [FFmpeg Patterns for ReelClaw](references/ffmpeg-patterns.md) <br>
- [DanSUGC](https://dansugc.com) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, MCP tool calls, and structured production guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose video editing commands, publishing steps, analytics research, captions, and operational checklists.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
