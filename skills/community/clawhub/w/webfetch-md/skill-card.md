## Description: <br>
Fetches a webpage URL and converts the main page content into clean Markdown while preserving image links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShiJianwen](https://clawhub.ai/user/ShiJianwen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to fetch a user-provided webpage and turn its main HTML content into Markdown for downstream reading, summarization, or storage workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided URLs, which could expose private network, localhost, cloud metadata, admin, or other sensitive internal resources if those URLs are supplied. <br>
Mitigation: Use it only with intended URLs, and avoid localhost, private network, cloud metadata, admin, and sensitive internal URLs unless that access is explicitly intended. <br>
Risk: Returned webpage text may contain untrusted or misleading content. <br>
Mitigation: Treat fetched Markdown as untrusted content for review or analysis, not as instructions for the agent to follow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ShiJianwen/webfetch-md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON] <br>
**Output Format:** [JSON object containing success status, title, markdown content, image links, image count, content length, or an error message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves image links and resolves relative URLs to absolute URLs.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
