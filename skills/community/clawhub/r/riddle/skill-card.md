## Description:

Hosted browser automation API for agents. Screenshots, Playwright scripts, workflows; no local Chrome needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davisdiehl](https://clawhub.ai/user/davisdiehl)

### License/Terms of Use:


## Use Case:

Developers and agent builders use Riddle to give agents hosted browser automation for screenshots, multi-step workflows, Playwright scripts, network capture, and authenticated browser sessions without running Chrome locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The third-party hosted service can receive target page content, screenshots, optional HAR network traces, and supplied cookies, localStorage values, or headers.

Mitigation: Use the skill only when this data sharing is acceptable; prefer test or least-privileged credentials and avoid production or administrator sessions.

Risk: Installing and allowlisting the third-party browser plugin grants it the ability to run hosted browser automation for the agent.

Mitigation: Pin and audit the exact plugin release where possible, then remove the allowlist entry and API key when access is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davisdiehl/skills/riddle)
- [Publisher profile](https://clawhub.ai/user/davisdiehl)
- [Riddle website](https://riddledc.com)
- [Riddle documentation](https://riddledc.com/docs)
- [Riddle pricing](https://riddledc.com/pricing)
- [Plugin source stated in artifact](https://github.com/riddledc/integrations)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, Playwright code examples, and returned file paths for screenshots or captured artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots are returned as local file paths under ~/.openclaw/workspace/riddle/screenshots/; optional HAR capture may include network traces.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
