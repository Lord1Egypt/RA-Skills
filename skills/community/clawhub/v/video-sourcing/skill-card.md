## Description: <br>
Run the Video Sourcing Agent with deterministic, concise chat UX for /video_sourcing using a pinned self-bootstrap runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SamuelZ12](https://clawhub.ai/user/SamuelZ12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to find, compare, and analyze social videos across YouTube, TikTok, Instagram, and Twitter/X. It returns concise video references, relevance notes, progress updates, and actionable fallback guidance through /video_sourcing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download and run an external video-sourcing runtime on the host. <br>
Mitigation: Install only when the external runtime is trusted, review the linked repository before use, and prefer explicit /video_sourcing invocation. <br>
Risk: The runtime uses Google and YouTube API keys and may consume quota or expose broad credentials. <br>
Mitigation: Use restricted API keys, monitor quota usage, and scope environment variables to the runtime that needs them. <br>
Risk: First-use network bootstrapping depends on git, uv, network access, and the pinned release remaining available. <br>
Mitigation: Verify git and uv are installed, confirm the pinned runtime before granting host access, and use VIDEO_SOURCING_AGENT_ROOT for a reviewed local runtime when appropriate. <br>


## Reference(s): <br>
- [Video Sourcing Agent repository](https://github.com/Memories-ai-labs/video-sourcing-agent) <br>
- [ClawHub skill page](https://clawhub.ai/SamuelZ12/video-sourcing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise status updates, a short conclusion, up to three video reference links, and compact tool status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git, uv, GOOGLE_API_KEY, and YOUTUBE_API_KEY; uses a pinned v0.2.5 runtime unless VIDEO_SOURCING_AGENT_ROOT is set.] <br>

## Skill Version(s): <br>
0.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
