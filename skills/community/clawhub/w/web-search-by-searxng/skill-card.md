## Description: <br>
Search using a custom SearXNG instance via HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyijun](https://clawhub.ai/user/cyijun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query a configured SearXNG instance, collect web results, and narrow searches by language, time range, category, engine, pagination, or safe-search level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to the configured SearXNG instance and may also be sent to selected upstream search engines. <br>
Mitigation: Use a trusted or self-hosted HTTPS SearXNG instance, avoid secrets or confidential terms in queries, and choose engines appropriate for the data being searched. <br>
Risk: Some public SearXNG instances disable JSON, CSV, or RSS output or apply rate limits. <br>
Mitigation: Check instance settings before relying on structured formats, add delays between requests, and self-host for predictable API access. <br>


## Reference(s): <br>
- [SearXNG Engines and Categories Reference](references/engines_and_categories.md) <br>
- [ClawHub skill page](https://clawhub.ai/cyijun/web-search-by-searxng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON, CSV, or RSS search responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided SearXNG instance URL or SEARXNG_URL environment variable.] <br>

## Skill Version(s): <br>
0.1.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
