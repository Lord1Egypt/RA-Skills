## Description: <br>
Xby Article helps agents search academic literature, fetch article metadata and full text, retrieve references, analyze citation relationships, and assess journal quality through XiaoBenYang literature APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and AI-assistant users can use this skill to locate scholarly articles, retrieve PMCID-backed article details, manage references, inspect literature relationships, and compare journal metrics. The skill requires a XiaoBenYang API key before it can call the literature services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the XiaoBenYang API key in a local .env file. <br>
Mitigation: Install only in environments where local .env storage is acceptable, restrict file access, and delete or rotate the key when credentials change. <br>
Risk: Returned article metadata and full-text content come from external API services. <br>
Mitigation: Review retrieved literature content, citations, and journal metrics before using them in research, publication, or decision workflows. <br>


## Reference(s): <br>
- [Xby Article on ClawHub](https://clawhub.ai/cainingnk/xby-article) <br>
- [XiaoBenYang API key and service](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown summaries and structured API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return literature metadata, article full text, references, citation relationships, and journal quality metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
