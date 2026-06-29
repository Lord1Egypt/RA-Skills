## Description: <br>
Fetches YouTube video transcripts by URL or video ID through AgentPMT-hosted remote tool calls, returning transcript JSON with optional timestamps and language selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to retrieve YouTube transcripts for summarization, searchable text, accessibility workflows, timestamped citation, and content analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube video URLs, IDs, and transcript content are processed by AgentPMT and returned through a temporary signed cloud file. <br>
Mitigation: Avoid private, confidential, or regulated video content unless AgentPMT's storage and retention terms are acceptable. <br>
Risk: Temporary signed transcript URLs can expose transcript files to anyone who receives the URL before it expires. <br>
Mitigation: Treat signed URLs as sensitive, download only in trusted contexts, and avoid logging or broadly sharing them. <br>
Risk: The skill may require AgentPMT account setup, wallet/payment flow, or sensitive credentials before remote calls can be made. <br>
Mitigation: Use the setup skills for credential handling and keep secrets, wallet private keys, mnemonics, signatures, and payment headers out of prompts and logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/youtube-transcript-fetcher-newest) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/youtube-transcript-fetcher) <br>
- [Generated action schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Files, Text] <br>
**Output Format:** [Markdown instructions and JSON tool-call examples; runtime responses return transcript JSON through a temporary signed cloud file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports URL or video ID input, optional language selection, optional timestamped segments, and optional raw provider response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
