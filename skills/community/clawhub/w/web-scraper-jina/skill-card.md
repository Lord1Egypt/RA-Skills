## Description: <br>
Retrieves webpage content as Markdown by routing URLs through r.jina.ai, including examples for pages with access protections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itonlyforfun-AI](https://clawhub.ai/user/itonlyforfun-AI) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to prepare r.jina.ai URL patterns, curl commands, and Python snippets for extracting web page content into Markdown. Use should be limited to public content the user is authorized to access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to route arbitrary URLs through the third-party r.jina.ai service. <br>
Mitigation: Use only public URLs that the user is authorized to access, and do not send internal URLs, signed links, credentials, session-bearing URLs, proprietary pages, or protected content. <br>
Risk: The skill broadly describes bypassing website protections. <br>
Mitigation: Review intended scraping activity for authorization, site terms, and applicable policy before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itonlyforfun-AI/web-scraper-jina) <br>
- [r.jina.ai reader endpoint](https://r.jina.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown with inline URL patterns, bash commands, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated guidance relies on a third-party scraping service and should not include internal URLs, signed links, session-bearing URLs, credentials, proprietary pages, or protected content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
