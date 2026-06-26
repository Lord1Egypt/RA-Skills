## Description: <br>
Searches the public web through the AISA web search endpoint and returns structured titles, links, and snippets for online lookup tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve recent public web results, source links, snippets, and related search output through AISA endpoints when a task requires online lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and requested URLs are sent to AISA external endpoints. <br>
Mitigation: Avoid private, internal, credential-bearing, or confidential prompts and URLs unless AISA's handling of that data is trusted. <br>
Risk: The bundled client includes extraction, deep-research/model query, and AI synthesis features beyond basic web search. <br>
Mitigation: Review the selected subcommand and data being sent before use, and limit execution to the intended lookup workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/web-search-aisa) <br>
- [AISA service](https://aisa.one) <br>
- [AISA API base endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance and CLI text output with titles, links, snippets, answers, citations, and usage metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; sends search queries and requested URLs to AISA endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
