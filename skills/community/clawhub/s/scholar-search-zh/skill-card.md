## Description: <br>
Searches academic papers and research materials through the AISA Scholar API, including author, recency, citation, and publication-year queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when academic evidence is the primary goal, especially for paper search, author lookup, recent research, citation information, and publication-year filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, prompts, and supplied URLs may be sent to AISA and related backend services. <br>
Mitigation: Do not submit private URLs, credentials, unpublished research, or sensitive internal material unless the provider's data handling has been independently approved. <br>
Risk: The bundled client exposes broader web search, URL extraction, and model-query commands beyond the scholar-focused instructions. <br>
Mitigation: Review intended command usage before deployment and restrict use to the academic search paths needed for the release. <br>
Risk: The skill requires the sensitive AISA_API_KEY credential. <br>
Mitigation: Provide the key through the environment, avoid logging or sharing it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/scholar-search-zh) <br>
- [AISA service](https://aisa.one) <br>
- [AISA API endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and CLI search-result text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
