## Description: <br>
Command-line tool for searching, reading, and interacting with Zhihu (知乎). Supports hot topics, content search, article reading, user info, and Browser Relay-based voting/following. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lightislost](https://clawhub.ai/user/lightislost) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to run Zhihu CLI commands for reading Zhihu content, checking login status, searching topics, and preparing browser-assisted account actions such as voting, following, or posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live Zhihu session cookies and stores them in ~/.zhihu-cookie. <br>
Mitigation: Treat the cookie like a password, restrict or delete the cookie file after use, and log out or revoke sessions if exposure is suspected. <br>
Risk: The CLI can access a logged-in Zhihu session. <br>
Mitigation: Verify the npm package and publisher before running it, and use a dedicated browser profile when possible. <br>
Risk: Browser Relay actions such as voting, following, and posting can perform account-changing operations. <br>
Mitigation: Review generated instructions before execution and confirm account actions manually in the browser. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and short browser-action guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some workflows depend on a local Zhihu session cookie and Browser Relay for account-changing actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
