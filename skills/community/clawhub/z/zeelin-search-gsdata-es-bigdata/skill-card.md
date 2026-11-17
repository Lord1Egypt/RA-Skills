## Description:

智灵大数据搜索 turns Chinese natural-language search requests into JSON parameters, calls the configured Zeelin natural-language search API, and returns human-readable results plus a full JSON result file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urhd528](https://clawhub.ai/user/urhd528)

### License/Terms of Use:


## Use Case:

External users and analysts use this skill to query Zeelin for public-opinion, news, comments, hotspot, trend, and related reporting data from Chinese-language prompts. It helps convert a request into the required API payload, call the configured service, summarize returned records, and save complete results as JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default configuration sends API credentials and search queries to Zeelin endpoints over HTTP.

Mitigation: Verify the destination host before use and switch the API and website URLs to HTTPS if the Zeelin service supports it.

Risk: Broad trigger phrases can cause the skill to run on generic public-opinion, news, or trend requests.

Mitigation: Review the prompt before execution and avoid including sensitive search terms in broad or follow-up prompts.

Risk: Successful searches save full result JSON files in the user directory.

Mitigation: Treat saved result files as potentially sensitive and remove or protect them according to the user's data-handling needs.

## Reference(s):

- [Natural language to JSON reference](artifact/references/nl2json.md)
- [Zeelin search API reference](artifact/references/zenlin_search_api.md)
- [Zeelin service website](http://search-skill.zeelin.cn)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration guidance, API calls]

**Output Format:** [Markdown-style conversational summaries with JSON payloads and saved JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows a concise subset of successful results in chat and saves the complete API response to a timestamped JSON file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
