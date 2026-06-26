## Description: <br>
Run the Video Sourcing Agent with deterministic, concise chat UX for /video_sourcing using a pinned self-bootstrap runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[memories-ai-official](https://clawhub.ai/user/memories-ai-official) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, analysts, and developers use this skill to source, compare, and analyze social videos from services such as YouTube, TikTok, Instagram, and X, then receive concise results with concrete video references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs an external video-sourcing runtime locally. <br>
Mitigation: Install only when the Memories.ai Labs publisher and the pinned runtime are trusted. <br>
Risk: The runtime uses Google and YouTube API keys, which can expose quota, billing, or data-access risk. <br>
Mitigation: Use restricted API keys and monitor quota and billing while the skill is enabled. <br>
Risk: Automatic invocation may run local host execution when users ask for video sourcing or trend analysis. <br>
Mitigation: Prefer explicit /video_sourcing invocations when tighter control over execution is required. <br>


## Reference(s): <br>
- [ClawHub Video Sourcing Agent page](https://clawhub.ai/memories-ai-official/video-sourcing-agent) <br>
- [Video Sourcing Agent repository](https://github.com/Memories-ai-labs/video-sourcing-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Markdown responses with progress updates, top video references, and actionable error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Shows the top three video references by default and can use compact or verbose event detail.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
