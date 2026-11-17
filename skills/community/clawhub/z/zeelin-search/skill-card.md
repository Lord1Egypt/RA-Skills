## Description:

ZeeLin Search helps an agent convert Chinese natural-language media and public-opinion queries into Zeelin API requests, call the Zeelin search API, and present results with saved JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingjiusheng](https://clawhub.ai/user/yingjiusheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to query Zeelin for news, public-opinion, trend, sentiment, and social discussion results from Chinese natural-language prompts. The agent prepares the API request, handles missing API-key configuration, summarizes returned records, and saves complete results as JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags broad activation, which can cause the skill to run for generic news, public-opinion, trend, or sentiment prompts.

Mitigation: Confirm the user intends to use Zeelin before making API calls, especially when the trigger phrase is broad or implied.

Risk: The skill stores full search results as JSON in the user directory after successful API calls.

Mitigation: Tell users the exact output path and avoid sharing transcripts, logs, or generated files that may contain sensitive search details.

Risk: The security guidance flags insufficient API credential protection around Zeelin_Api_Key configuration.

Mitigation: Configure the API key only in the intended local config file, avoid exposing it in conversation or logs, and rotate the key if it is disclosed.

Risk: The security guidance recommends verifying the Zeelin API URL remains the intended HTTPS endpoint.

Mitigation: Review templates/config.json before use and confirm Zeelin_Api_Url is the expected https://skills.zeelin.cn endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yingjiusheng/skills/zeelin-search)
- [Zeelin website](https://skills.zeelin.cn)
- [Zeelin natural-language search API endpoint](https://skills.zeelin.cn/v2/api/es/search/natural)
- [Natural language to JSON reference](references/nl2json.md)
- [Zeelin search API reference](references/zenlin_search_api.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration guidance, API calls]

**Output Format:** [Markdown status messages and result summaries, plus JSON files containing complete API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a locally configured Zeelin_Api_Key; successful searches save full API responses to a user-directory JSON file named zeelin_search_results_YYYYMMDD_HHMMSS.json.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
