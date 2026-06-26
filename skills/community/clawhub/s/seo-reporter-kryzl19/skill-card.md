## Description: <br>
Audit a URL for SEO factors and generate an actionable markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and site operators use this skill to run quick, read-only SEO checks on a single public or authorized webpage and receive a scored markdown report with recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes read-only web requests to URLs provided by the user. <br>
Mitigation: Use it only for public or authorized pages, and avoid internal services, localhost, private network addresses, and URLs containing secrets. <br>
Risk: SEO findings are quick checks and may not replace full technical SEO crawls, page-speed analysis, backlink analysis, or keyword research. <br>
Mitigation: Treat the report as a focused triage output and use dedicated SEO tools for broader audits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kryzl19/seo-reporter-kryzl19) <br>
- [Publisher profile](https://clawhub.ai/user/kryzl19) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown SEO audit report with score tables, findings, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and fetches the user-provided URL plus related robots.txt and sitemap.xml URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
