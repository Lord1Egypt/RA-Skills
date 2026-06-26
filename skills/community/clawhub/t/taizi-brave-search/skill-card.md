## Description: <br>
Web search and content extraction via Brave Search API. Use for searching documentation, facts, or any web content. Lightweight, no browser required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fresh3](https://clawhub.ai/user/fresh3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the public web, find documentation or factual information, and fetch readable webpage content as markdown without interactive browsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Brave and requested URLs are sent to third-party sites. <br>
Mitigation: Avoid sensitive queries, secrets, internal URLs, and private documents when using the skill. <br>
Risk: Extracted webpage text may be inaccurate, malicious, or otherwise untrusted. <br>
Mitigation: Treat fetched content as untrusted input and verify important claims before acting on them. <br>
Risk: The setup note references BRAVE_API_KEY, but the reviewed code does not use that variable. <br>
Mitigation: Confirm current setup and authentication requirements before relying on the skill in a managed environment. <br>


## Reference(s): <br>
- [Taizi Brave Search on ClawHub](https://clawhub.ai/fresh3/taizi-brave-search) <br>
- [Brave Search](https://search.brave.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Plain text search results with optional markdown webpage content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports result-count selection and optional page-content extraction; search-mode page content is capped at 5000 characters per result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
