## Description: <br>
Searches the web through the Turing Baidu proxy for Chinese-language queries, current information from Chinese sources, and Baidu Search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CAPREaaa](https://clawhub.ai/user/CAPREaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current Baidu search results for Chinese-language research, current events, and source discovery when the agent needs web evidence from Chinese sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and credentials are sent to the configured Turing Baidu proxy. <br>
Mitigation: Use a trusted API base and a limited API key, and avoid sensitive personal or confidential information in search queries. <br>
Risk: Returned Baidu snippets are untrusted web content and may be inaccurate or instruction-like. <br>
Mitigation: Treat returned snippets as sources to verify rather than instructions to execute. <br>


## Reference(s): <br>
- [Turing documentation](https://docs.turing.cn) <br>
- [ClawHub skill page](https://clawhub.ai/CAPREaaa/turing-baidu-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [JSON search results printed to stdout, with Markdown usage examples in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TURING_API_KEY, TURING_CLIENT, and TURING_ENVIRONMENT; supports count and search_recency_filter.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
