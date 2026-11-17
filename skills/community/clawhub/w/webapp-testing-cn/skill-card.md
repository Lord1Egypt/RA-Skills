## Description:

Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to test local static or dynamic web applications with Playwright, including browser automation, UI behavior checks, screenshots, console-log capture, and local server lifecycle management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server-launch helper can run local commands supplied by the user, such as development server or backend startup scripts.

Mitigation: Review each server command before execution, use the skill only in trusted workspaces, and check for leftover server processes after runs.

Risk: Browser automation results can be misleading if dynamic pages are inspected before client-side JavaScript finishes loading.

Mitigation: Wait for network idle or the relevant selector before inspecting DOM state, taking screenshots, or executing follow-up actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/webapp-testing-cn)
- [Artifact license terms](artifact/LICENSE.txt)
- [Element discovery example](artifact/examples/element_discovery.py)
- [Static HTML automation example](artifact/examples/static_html_automation.py)
- [Console logging example](artifact/examples/console_logging.py)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Playwright scripts, selector-inspection steps, screenshots, console logs, and local server startup commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
