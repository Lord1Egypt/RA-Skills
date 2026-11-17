## Description:

Functional testing of web products using Playwright MCP, browser-use CLI, and the OpenClaw built-in browser, covering planning, execution, screenshot-based bug logging, reporting, and optional filing into Coding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyin717](https://clawhub.ai/user/wangyin717)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to plan and run functional tests against a provided web URL or feature, collect screenshots for defects, and produce a structured test report. With user confirmation, it can also file discovered bugs into Coding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require persistent browser security changes such as host allowlists or no-sandbox browser settings.

Mitigation: Approve each browser configuration change explicitly, use a dedicated test configuration, and restore browser settings after testing.

Risk: Authenticated browser testing can expose accounts, sessions, or private product data to automated browsing tools.

Mitigation: Use least-privilege test accounts and avoid personal browser profiles unless the user has explicitly approved that path.

Risk: Cloud browsers, tunnels, proxies, CAPTCHA, or anti-bot tooling can expand the network and browsing surface used during testing.

Mitigation: Limit these tools to authorized test targets, avoid sensitive internal services unless required, and disable external routing after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyin717/skills/testagent-browser-testing)
- [Browser Testing Reference](artifact/REFERENCE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown test plans and reports with inline commands, screenshot file references, and optional issue-filing details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include PNG screenshot paths and Coding issue numbers after user confirmation.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter states 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
