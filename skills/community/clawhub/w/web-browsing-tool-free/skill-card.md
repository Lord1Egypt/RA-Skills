## Description: <br>
网页浏览助手免费版 helps personal users access webpages, summarize content, extract information from URLs, and search the web for current information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for everyday web information gathering, including visiting URLs, summarizing webpages, collecting research material, searching current information, and extracting structured data from pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web fetch and search activity can expose prompts, URLs, page content, callback URLs, or other browsing context to external services. <br>
Mitigation: Do not use the skill with confidential URLs, private logged-in pages, secrets, or sensitive business data unless the destination services and callback handling are explicitly trusted. <br>
Risk: Fetched webpages and search results can be incomplete, stale, misleading, or unavailable. <br>
Mitigation: Verify important findings against original sources before using them for decisions, publications, or operational work. <br>
Risk: The skill may guide an agent to run web-related shell commands or configure search credentials. <br>
Mitigation: Review proposed commands and configuration before execution, and avoid exposing API keys or environment secrets to fetched pages or untrusted callbacks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/web-browsing-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and structured text, JSON, or CSV results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use internet fetch and search tools; advanced search quality may depend on optional search API configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
