## Description: <br>
Environment-aware web UI testing that detects wmux, cmux, or plain/tmux sessions and routes browser verification through the appropriate visible workflow, including SSO flow checks and CDP-based closed-shadow DOM cascade diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to inspect web pages, perform visible browser interactions, summarize UI verification results, verify Authentik SSO flows, and diagnose closed-shadow DOM styling issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through visible browser sessions and SSO or login testing that may expose sensitive credentials. <br>
Mitigation: Use only approved test accounts or explicitly approved credentials, and do not allow the agent to handle real passwords, 2FA codes, or generated tokens unless the exact action has been reviewed and approved. <br>
Risk: The skill includes workflows around admin, deployment, and database-change operations that could affect a target environment. <br>
Mitigation: Verify the target environment, review each proposed command before execution, prefer dry runs where available, and keep a rollback path for any deployment or database change. <br>
Risk: Browser automation can interact with the wrong site or session if the target URL or environment is incorrect. <br>
Mitigation: Confirm the tested URL, active session, and intended environment before entering credentials or taking actions that change state. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/drumrobot/web-ui-test) <br>
- [CDP Trace documentation](cdp-trace.md) <br>
- [SSO Verification documentation](sso-verify.md) <br>
- [Chrome DevTools Protocol - DOM domain](https://chromedevtools.github.io/devtools-protocol/tot/DOM/) <br>
- [Chrome DevTools Protocol - CSS.getMatchedStylesForNode](https://chromedevtools.github.io/devtools-protocol/tot/CSS/#method-getMatchedStylesForNode) <br>
- [Playwright - browserContext.newCDPSession](https://playwright.dev/docs/api/class-browsercontext#browser-context-new-cdp-session) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes browser snapshots and verification results; should not return raw snapshot data.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and CHANGELOG, released 2026-06-03; frontmatter metadata lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
