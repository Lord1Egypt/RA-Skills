## Description: <br>
Fetch real-time social media data from X (Twitter) and Reddit by keyword, username, date range, and filters with engagement metrics via the Macrocosmos SN13 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Arrmlet](https://clawhub.ai/user/Arrmlet) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to construct REST or Python SDK requests that retrieve X and Reddit posts, filter by source, usernames, keywords, date ranges, and limits, and inspect returned engagement metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys can be exposed if real credentials are placed in prompts, logs, shared transcripts, or generated examples. <br>
Mitigation: Use a dedicated, revocable MC_API key stored as an environment variable, and avoid including real keys in prompts or logs. <br>
Risk: Bulk collection or redistribution of social-media data may create platform terms, privacy, retention, or redistribution obligations. <br>
Mitigation: Review applicable platform terms and privacy obligations before collection, and minimize retention and redistribution of downloaded datasets. <br>
Risk: Narrow username-only or low-volume queries can timeout or return incomplete data. <br>
Mitigation: Set explicit wider date ranges, prefer keyword searches when possible, and handle timeouts by retrying broader queries. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Arrmlet/social-data) <br>
- [Macrocosmos MCP project](https://github.com/macrocosm-os/macrocosmos-mcp) <br>
- [Macrocosmos MCP on PyPI](https://pypi.org/project/macrocosmos-mcp) <br>
- [Macrocosmos API keys](https://app.macrocosmos.ai/account?tab=api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, bash, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dedicated, revocable MC_API key for live API calls.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact metadata lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
