## Description: <br>
X/Twitter intelligence scraper. Search tweets, scrape profiles, pull comments, auto-transcribe videos. Classify tweets as replicable methods vs content. CLI tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aces1up](https://clawhub.ai/user/aces1up) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, analysts, and content researchers use this skill to collect X/Twitter posts, profile posts, replies, and tweet intelligence for workflow and content research. It can classify posts as replicable methods or general content and can include video transcripts when optional provider credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage telemetry is sent to ClawAgents during setup and execution. <br>
Mitigation: Review the telemetry behavior before installation and use the skill only when telemetry sharing is acceptable. <br>
Risk: Provider API keys can be stored in plaintext .env and ~/.x-scout/config.json files. <br>
Mitigation: Protect local configuration files, restrict filesystem permissions, and rotate keys if the host or files are exposed. <br>
Risk: The tool can modify the Python environment by installing packages during setup or at runtime. <br>
Mitigation: Run it inside a virtual environment and review dependency installation paths before use. <br>
Risk: Tweet text or media-derived content may be sent to external AI or transcription providers when optional features are enabled. <br>
Mitigation: Use --no-methods or --no-transcribe when external processing is not appropriate. <br>


## Reference(s): <br>
- [X-Scout ClawHub page](https://clawhub.ai/aces1up/x-scout) <br>
- [Publisher profile](https://clawhub.ai/user/aces1up) <br>
- [X-Scout homepage](https://clawagents.dev/x-scout) <br>
- [TwitterAPI.io](https://twitterapi.io) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [Deepgram](https://deepgram.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [CLI text tables or JSON, with setup and usage guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TWITTERAPI_KEY for primary data access; optional OpenRouter, Cerebras, and Deepgram keys enable method detection, query optimization, and transcription.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
