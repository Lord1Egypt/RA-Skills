## Description: <br>
Hotel search and pricing via the RollingGo CLI for destination searches, date/star/budget/tag/distance filters, hotel detail and room pricing checks, and hotel tag lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longcreat](https://clawhub.ai/user/longcreat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-assistance agents use this skill to search hotel candidates, refine results with structured filters, inspect current room pricing, and obtain hotel detail or booking links through the RollingGo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external RollingGo package and AIGOHOTEL service, so users could install or call a provider they did not intend to use. <br>
Mitigation: Before installing or executing commands, verify the rollinggo package and AIGOHOTEL service match the intended provider. <br>
Risk: API keys and hotel-search details may expose credentials or sensitive travel preferences if handled carelessly. <br>
Mitigation: Prefer the AIGOHOTEL_API_KEY environment variable over command-line API-key flags, and avoid entering unnecessary sensitive personal details in hotel searches. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/longcreat/search-hotel) <br>
- [RollingGo Hotel CLI homepage](https://mcp.agentichotel.cn) <br>
- [RollingGo NPX Reference](references/rollinggo-npx.md) <br>
- [RollingGo UV Reference](references/rollinggo-uv.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented result guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to call RollingGo commands that return JSON by default, with stderr reserved for errors and documented CLI exit codes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
