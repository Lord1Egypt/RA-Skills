## Description: <br>
Universal web access skill: search, fetch, browser automation via CDP Proxy. Handles login-required sites, anti-scraping bypasses, and complex web interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eze-is](https://clawhub.ai/user/eze-is) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve web information and operate web pages, including pages that need login state, browser interaction, or CDP-based automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can give an agent broad control over a logged-in Chrome session. <br>
Mitigation: Install only when that access is intended, avoid sensitive accounts and private documents, and require explicit approval before uploads, screenshots, purchases, account changes, or use of tokenized URLs. <br>
Risk: A localhost browser-control proxy may remain running after the task is complete. <br>
Mitigation: Stop the proxy when finished if ongoing browser-control access is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eze-is/web-access) <br>
- [Project homepage](https://github.com/eze-is/web-access) <br>
- [CDP Proxy API reference](references/cdp-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and browser automation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a localhost CDP proxy and the user's existing Chrome session when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
