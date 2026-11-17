## Description:

A modern text-based browser that renders web pages in the terminal using headless Firefox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fresh3](https://clawhub.ai/user/fresh3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and terminal users use this skill to run Browsh, a text-based browser backed by headless Firefox, including launching the browser and opening a specific URL from a terminal session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on local browsh and Firefox binaries resolved from PATH.

Mitigation: Install browsh and Firefox from trusted sources and confirm PATH resolves to the intended binaries before use.

Risk: Browsing through Browsh contacts the websites the user opens.

Mitigation: Open only intended URLs and apply the same privacy, network, and content policies used for other web browsing tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fresh3/skills/taizi-browsh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local browsh and firefox binaries in PATH; Browsh runs as a TUI and should be launched in a PTY session.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
