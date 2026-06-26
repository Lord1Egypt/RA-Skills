## Description: <br>
Control the user's real Chrome browser through Tampermonkey injection so an agent can read pages, navigate tabs, and interact with login-required content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyinghanger](https://clawhub.ai/user/flyinghanger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill when they need an agent to inspect or operate pages in their own logged-in Chrome session, including sites that require existing cookies or local browser state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a real logged-in Chrome session with access to cookies, local storage, and account state. <br>
Mitigation: Install only when that access is intended; prefer a separate Chrome profile or test accounts and review the external plugin and userscript before use. <br>
Risk: Browser actions such as clicks, form submissions, purchases, posts, deletions, or account changes can affect real accounts. <br>
Mitigation: Require explicit user approval before any state-changing browser action and prefer read-only page inspection when possible. <br>
Risk: Injected JavaScript runs in the page context and can read or modify sensitive page content. <br>
Mitigation: Review JavaScript snippets before execution, limit use to trusted pages, and avoid entering sensitive data unless the user has approved the specific action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flyinghanger/use-my-browser) <br>
- [Tampermonkey userscript](https://raw.githubusercontent.com/lsdefine/pc-agent-loop/main/assets/ljq_web_driver.user.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include browser-operation steps, page text, JavaScript snippets, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
