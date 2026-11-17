## Description:

Run long-horizon, multi-step browser automation by delegating to the Microsoft webwright CLI, which writes and executes Playwright scripts to drive a real Chromium browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hansraj316](https://clawhub.ai/user/hansraj316)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run authorized, repeatable browser automation for multi-step web flows such as logins, forms, checkout or wizard flows, and cross-page navigation where a generated Playwright script is useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The delegated browser automation can take real actions on live websites and consume model-provider tokens.

Mitigation: Run only user-authorized, scoped tasks, avoid destructive actions, and review generated plans and artifacts before relying on results.

Risk: Credentials or tokens placed in task text can be sent to the model provider and recorded in run artifacts.

Mitigation: Provide only environment variable names or use a user-controlled browser profile; do not place literal secrets in task text or config.

Risk: Generated scripts may write artifacts or execute with an unexpected Python or Playwright installation.

Mitigation: Keep output directories inside the workspace and run Webwright from a verified virtual environment with Chromium installed.

## Reference(s):

- [Webwright project homepage](https://github.com/microsoft/webwright)
- [Webwright CLI reference](references/cli.md)
- [Webwright setup](references/setup.md)
- [ClawHub skill page](https://clawhub.ai/hansraj316/skills/webwright)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated script paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Webwright run artifacts such as generated Playwright scripts, plans, logs, screenshots, and result summaries when available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
