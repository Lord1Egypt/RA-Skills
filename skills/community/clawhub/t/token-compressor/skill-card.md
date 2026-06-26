## Description: <br>
Pre-process prompts through three compression layers before sending to paid APIs, using a local Ollama model to compress messages and summarize history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to reduce paid AI API token usage by compressing user messages, summarizing older conversation turns, and checking an in-memory cache before making downstream API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and older conversation turns are sent to the configured Ollama service for compression and summarization. <br>
Mitigation: Keep Ollama bound to localhost or another trusted private endpoint, and review Ollama logging and host security before using sensitive, regulated, or secret data. <br>
Risk: Conversation summaries and cached responses are held in memory and can span interactions if reused across conversations or users. <br>
Mitigation: Call reset() between separate conversations or users, and configure cache size and TTL for the deployment context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/token-compressor) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Configuration, Guidance] <br>
**Output Format:** [JavaScript module behavior with Markdown documentation and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Compression uses a configured local Ollama service, in-memory cache settings, and configurable model, host, port, history, and TTL options.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
