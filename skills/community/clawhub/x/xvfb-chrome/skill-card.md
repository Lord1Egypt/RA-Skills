## Description:

Guides agents through running Chrome on Linux servers with headless mode or Xvfb, including Chrome DevTools MCP automation setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codinglink](https://clawhub.ai/user/codinglink)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to configure Chrome for scraping, screenshots, browser debugging, and Chrome DevTools MCP workflows on Linux servers without a GUI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chrome automation guidance includes unsafe browser and process-management defaults, including --no-sandbox examples and broad killall/pkill cleanup patterns.

Mitigation: Run under a dedicated unprivileged account, use unique temporary browser profiles, avoid --no-sandbox unless isolation requires it, and replace broad cleanup commands with PID-scoped cleanup.

Risk: A Chrome DevTools debugging endpoint can allow browser control if exposed beyond the local host.

Mitigation: Bind DevTools explicitly to 127.0.0.1 and avoid using personal or production-authenticated browser profiles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codinglink/skills/xvfb-chrome)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and command tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides operational command examples for Chrome, Xvfb, and Chrome DevTools MCP; does not generate executable files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
