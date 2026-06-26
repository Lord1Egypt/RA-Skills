## Description: <br>
Audit a URL for SEO factors and generate an actionable markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kryzl19](https://clawhub.ai/user/kryzl19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, marketers, and SEO practitioners use this skill to audit a single public webpage for core on-page SEO signals and receive a scored markdown report with recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit fetches the supplied page, follows redirects, and requests related SEO files on the same host. <br>
Mitigation: Run it only on public or intended URLs, and avoid localhost, private intranet services, cloud metadata addresses, and token-bearing links. <br>
Risk: The generated SEO findings may be incomplete for full technical SEO, page speed, backlink, keyword, SSL, or site-wide crawl analysis. <br>
Mitigation: Use the report as a single-page on-page SEO check and rely on dedicated SEO, performance, backlink, keyword, or security tools for those areas. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kryzl19/seo-reporter) <br>
- [Publisher profile](https://clawhub.ai/user/kryzl19) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown SEO audit report with scored findings and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and performs read-only HTTP requests for the supplied URL plus related SEO files on the same host.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
