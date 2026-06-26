## Description: <br>
web-search-zh searches the public web through the AISA web search API and returns structured titles, links, and summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need an agent to retrieve current public web results through AISA and return usable titles, links, summaries, answers, citations, or extracted page text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, and retrieved page content may be sent to AISA. <br>
Mitigation: Avoid confidential queries, private URLs, or sensitive page content unless sharing that data with AISA is acceptable. <br>
Risk: AISA_API_KEY is a sensitive credential required by the skill. <br>
Mitigation: Use a revocable or quota-limited key and store it only in the intended environment variable. <br>
Risk: Extraction, Sonar, and multi-source synthesis modes broaden the amount and kind of data sent for research. <br>
Mitigation: Invoke those modes only when the user specifically asks for deeper research, extraction, or synthesis. <br>


## Reference(s): <br>
- [web-search-zh on ClawHub](https://clawhub.ai/aisadocs/web-search-zh) <br>
- [AISA](https://aisa.one) <br>
- [AISA API base](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with structured search result titles, links, snippets, answers, citations, and usage or cost metadata when returned by AISA.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; search, extraction, Sonar, and multi-source modes may send query text, URLs, and retrieved page content to AISA.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
