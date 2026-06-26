## Description: <br>
Search and analyze videos across YouTube, TikTok, Instagram, and X/Twitter via the Memories.ai Video Searching API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[memories-ai-official](https://clawhub.ai/user/memories-ai-official) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find, compare, and analyze social videos with concrete links and metrics across supported platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video-search queries are sent to Memories.ai under the configured MEMORIES_API_KEY. <br>
Mitigation: Avoid confidential or regulated search terms and use a scoped or dedicated API key when available. <br>
Risk: The documented script path may not match the packaged root script location. <br>
Mitigation: Confirm the runner path before deployment and adjust packaging or invocation if needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/memories-ai-official/video-searching) <br>
- [Memories.ai Video Searching API](https://api-tools.memories.ai/agents/video-searching-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown response summarizing video-search results, with structured video references and run metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEMORIES_API_KEY plus curl and jq; emits user-facing summaries from structured API events.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
