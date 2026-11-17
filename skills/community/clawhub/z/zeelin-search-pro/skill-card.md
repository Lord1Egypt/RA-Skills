## Description:

Converts Chinese natural-language search requests into Zeelin API queries, calls the Zeelin Search API with configured credentials, and returns human-readable search results plus exported JSON data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urhd528](https://clawhub.ai/user/urhd528)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query public opinion, news, trend, and media-report data through Zeelin Search from Chinese natural-language prompts. The skill is intended for assisted search workflows that need structured API parameters, readable result summaries, and saved JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Zeelin API key for request signing.

Mitigation: Configure the key outside the chat, avoid exposing it in prompts or shared logs, and rotate it if disclosure is suspected.

Risk: Search queries and returned results are sent to and received from the Zeelin service.

Mitigation: Avoid sensitive searches unless the user accepts sending those queries and results to the service.

Risk: The skill saves complete search responses as timestamped JSON files.

Mitigation: Store exported files in an appropriate location, limit access to them, and periodically delete results that are no longer needed.

Risk: The skill relies on configured Zeelin API and website URLs without requiring the agent to validate them.

Mitigation: Verify the configured Zeelin API URL before use and review configuration changes before running searches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/urhd528/skills/zeelin-search-pro)
- [Natural language to JSON module](references/nl2json.md)
- [Zeelin Search API module](references/zenlin_search_api.md)
- [Zeelin service website](https://skills.zeelin.cn)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration guidance]

**Output Format:** [Markdown-style result summaries with timestamped JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Zeelin API key; successful calls save complete API responses as timestamped JSON files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
