## Description:

Search the web using Baidu AI Search Engine (BDSE). Use for live information, documentation, or research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ide-rea](https://clawhub.ai/user/ide-rea)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to submit live web-search queries to Baidu and retrieve current research, documentation, or topic results. It is useful when an agent needs external search results with optional count and freshness filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Baidu's external API and may be retained or exposed according to that service's handling of requests.

Mitigation: Do not submit secrets, credentials, regulated personal data, confidential project names, or other sensitive queries through this skill.

Risk: The script prints the parsed request body to stdout, so submitted queries may appear in agent logs or terminal history.

Mitigation: Review logs and avoid using the skill for sensitive searches; remove or suppress request echoing before deployment in environments with stricter logging controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ide-rea/skills/test-01)
- [Publisher profile](https://clawhub.ai/user/ide-rea)
- [Baidu Qianfan AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON search results printed to stdout, with Markdown usage examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; accepts query, count, and freshness parameters. The script removes snippet fields from returned references.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
