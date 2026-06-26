## Description: <br>
Search academic papers and scholarly sources through the AISA scholar endpoint. Use when: the user asks for papers, authors, recent research, citations, or year-filtered academic evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research-focused agents use this skill to retrieve academic papers, author evidence, citations, and year-filtered scholarly search results through the AISA API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AISA API key and sends user queries to api.aisa.one. <br>
Mitigation: Install only when the operator is comfortable sharing the configured research queries with AISA, and use a scoped or revocable key where available. <br>
Risk: The bundled client exposes broader web search, URL extraction, and AI synthesis commands beyond the scholar-search description. <br>
Mitigation: Before deployment, either restrict usage to the scholar command or update operator-facing documentation and review procedures to disclose the broader client behavior. <br>
Risk: Search and synthesis results can be incomplete, stale, or misleading. <br>
Mitigation: Require users or downstream agents to verify important claims against cited papers or primary sources before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/scholar-search-aisa) <br>
- [Publisher profile](https://clawhub.ai/user/bibaofeng) <br>
- [AISA API base endpoint](https://api.aisa.one/apis/v1) <br>
- [AISA](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and text search results from the bundled Python client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; API responses may include result titles, URLs, dates, snippets, citations, answers, usage cost, and credits remaining.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
