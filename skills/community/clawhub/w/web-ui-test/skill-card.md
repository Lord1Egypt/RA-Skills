## Description: <br>
Environment-aware browser operations for UI verification, closed shadow DOM diagnosis, and browser-login-assisted credential issuance or refresh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform visible browser-based UI checks, diagnose styling issues in closed shadow DOM, and guide controlled credential issuance or refresh workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help manage real credentials, including token discovery, issuance, refresh, persistence, and handoff. <br>
Mitigation: Install only when credential automation is intended, and review each run before it reads secret stores, issues or refreshes tokens, persists credentials, or changes GitHub, Vault, or cloud CLI state. <br>
Risk: Browser workflows may operate in logged-in sessions and affect real service state. <br>
Mitigation: Use a narrower UI-only browser skill when credential handling is unnecessary, and require user-visible browser sessions plus explicit confirmation before account or service changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/web-browser) <br>
- [UI Test topic](artifact/ui-test.md) <br>
- [CDP Trace topic](artifact/cdp-trace.md) <br>
- [Credential Issue topic](artifact/credential-issue.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline shell and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser actions, page-state observations, screenshots, credential handoff steps, and persistence guidance depending on the requested topic.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence; changelog released 2026-06-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
