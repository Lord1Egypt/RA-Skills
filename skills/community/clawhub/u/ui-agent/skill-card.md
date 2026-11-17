## Description:

Universal UI automation for browsers and desktops. Chrome DevTools Protocol + native APIs. 15/15 verified tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimaansari](https://clawhub.ai/user/nimaansari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use UI-Agent to automate browser and desktop workflows with CDP, native UI control, screenshots, DOM checks, file checks, and session-handling helpers for testing or RPA tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control browsers and desktops, including interactions with sensitive sessions and local UI data.

Mitigation: Run it only in an isolated VM or container with disposable test accounts, not a personal browser profile or production login.

Risk: The skill can capture screenshots, log typed values, manipulate cookies, and upload local files if directed.

Mitigation: Add approval gates for screenshot capture, cookie handling, file upload, and typed-value workflows before real use.

Risk: The skill can terminate Chrome or Xvfb processes and drive broad UI actions with weak guardrails.

Mitigation: Restrict allowed domains, file paths, process targets, and command execution scope in the deployment wrapper.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nimaansari/skills/ui-agent)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [API Reference](./docs/SKILL.md)
- [Test Evidence](./docs/VERIFICATION_FINAL.md)
- [Production Guide](./docs/FINAL_PRODUCTION_STATUS.md)
- [Session Persistence](./docs/SP1_CONCLUSION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can propose commands and code that control local browsers, desktops, files, screenshots, cookies, and processes.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
