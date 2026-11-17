## Description:

Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to test local static and dynamic web applications with Playwright, including UI verification, rendered DOM inspection, screenshots, browser log capture, and server lifecycle management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server helper can run local dev-server commands supplied from project context.

Mitigation: Review commands passed to --server and run the helper only for trusted projects and expected local ports.

Risk: Screenshots and browser logs captured during testing can contain sensitive page content.

Mitigation: Avoid using the skill on pages containing secrets unless necessary, and treat saved screenshots or logs as sensitive artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pupuking723/skills/webapp-testing-anthropic)
- [Publisher profile](https://clawhub.ai/user/pupuking723)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Playwright scripts, helper command invocations, browser screenshots, and browser console logs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
