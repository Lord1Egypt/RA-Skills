## Description: <br>
Tavily Search provides advanced web search through the AIsa API with search depth, topic, time range, domain filtering, source discovery, content extraction, and optional LLM-generated answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run web research, source discovery, content extraction, news or finance-focused searches, and optional answer summaries through AIsa-backed Tavily search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, and requested summaries are sent to AIsa-backed external services. <br>
Mitigation: Avoid entering secrets, private internal URLs, regulated data, or confidential business information unless external processing is approved for the use case. <br>
Risk: The skill requires the sensitive AISA_API_KEY credential. <br>
Mitigation: Provide the API key through the environment or approved plugin configuration and avoid hard-coding it in prompts, scripts, logs, or shared files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bibaofeng/tavily-search-aisa-api) <br>
- [AIsa](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [CLI text with titles, URLs, dates, excerpts, citations when returned, and optional answer summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and sends search queries, URLs, and requested summaries to AIsa-backed external services.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
