## Description: <br>
Web search via Querit.ai API for documentation, current events, facts, and web content, returning structured results with titles, URLs, and snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[interskh](https://clawhub.ai/user/interskh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to search the web from an OpenClaw agent, filter results, and optionally extract readable page content as markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Querit.ai and may reveal sensitive topics or internal information. <br>
Mitigation: Avoid secrets, internal URLs, regulated data, and confidential business information in search queries. <br>
Risk: Optional page extraction fetches selected URLs from the user's machine. <br>
Mitigation: Review URLs before extraction and avoid fetching private, internal, or untrusted pages unless the environment permits it. <br>
Risk: The one-line installer downloads and runs code from the network. <br>
Mitigation: Review or pin installer source before execution and install dependencies from trusted package sources. <br>


## Reference(s): <br>
- [Querit.ai](https://querit.ai) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [ClawHub release page](https://clawhub.ai/interskh/querit-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text search results, optional extracted markdown content, or raw JSON result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QUERIT_API_KEY for search; page content extraction fetches selected URLs directly and may fail for non-HTML, protected, or very large pages.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
