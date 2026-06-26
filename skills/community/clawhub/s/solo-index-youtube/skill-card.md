## Description: <br>
Index YouTube channel videos and transcripts for semantic search. Use when user says "index YouTube", "add YouTube channel", "update video index", or "index transcripts". Works with solograph MCP (if available) or standalone via yt-dlp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and knowledge workers use this skill to index YouTube channel transcripts into a local searchable knowledge base, either through solograph MCP or a yt-dlp fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube requests and optional browser-cookie access can expose authenticated browsing context or trigger rate limiting. <br>
Mitigation: Use ordinary public channel handles or URLs by default, allow browser-cookie access only when authenticated YouTube requests are explicitly intended, and reduce limits or add sleep intervals when rate limited. <br>
Risk: Transcript downloads and generated summaries may be incomplete when videos lack subtitles or metadata is sparse. <br>
Mitigation: Review the docs/youtube/ output and generated index before relying on indexed results. <br>


## Reference(s): <br>
- [ClawHub listing for Index Youtube](https://clawhub.ai/fortunto2/solo-index-youtube) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports indexed video counts, transcript availability, chapter-marker counts, index location, and search instructions.] <br>

## Skill Version(s): <br>
2.0.0 (source: skill metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
