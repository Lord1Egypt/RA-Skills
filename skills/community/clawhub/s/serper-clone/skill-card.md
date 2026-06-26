## Description: <br>
Provides web search through a self-hosted Serper-compatible API powered by SearXNG for web, news, image, video, shopping, scholar, and patent searches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulscode](https://clawhub.ai/user/paulscode) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route search tasks to a self-hosted Serper-compatible API instead of a hosted Serper account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search privacy depends on the configured backend and any upstream engines it uses. <br>
Mitigation: Use only a Serper Clone or SearXNG server you control or trust, and verify its logging and upstream-engine configuration before sensitive searches. <br>
Risk: The required API key file can expose access to the search service if it is readable by other users. <br>
Mitigation: Store the key file at ~/.openclaw/workspace/.serper-clone-api-key and restrict it with chmod 600. <br>
Risk: Plain HTTP or unsafe shell JSON construction can expose or alter search requests. <br>
Mitigation: Use HTTPS where possible and encode JSON safely when adapting the shell helper. <br>


## Reference(s): <br>
- [Serper Clone server](https://github.com/paulscode/serper-startos) <br>
- [SearXNG](https://github.com/searxng/searxng) <br>
- [OpenClaw](https://github.com/openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/paulscode/serper-clone) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local API key and base URL file for a trusted Serper Clone or SearXNG-backed server.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
