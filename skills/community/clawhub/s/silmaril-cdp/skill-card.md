## Description:

Browser automation, DOM inspection, page mutation, wait orchestration, flow execution, and local proxy override work through the Silmaril Chrome DevTools Protocol toolkit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[malac12](https://clawhub.ai/user/malac12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect and automate local Chrome-family browser pages through CDP, including DOM extraction, selector validation, page actions, waits, repeatable flow execution, and local proxy override workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct agents to install and run an unpinned external browser automation toolkit.

Mitigation: Require explicit user approval before fetching remote code, install from a pinned and reviewed revision, and prefer the expected local toolkit path over PATH fallback.

Risk: Page-script execution can alter or inspect sensitive browser state.

Mitigation: Use eval-js only in trusted local sessions, require the documented unsafe-JavaScript acknowledgement, and avoid authenticated or sensitive pages unless the user explicitly requests that work.

Risk: MITM proxy workflows can intercept or override local browser traffic.

Mitigation: Require the documented MITM acknowledgement, keep listeners on loopback, use narrow temporary override rules, and avoid sensitive sessions unless explicitly needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/malac12/skills/silmaril-cdp)
- [Command Patterns](references/command-patterns.md)
- [Flow Runner](references/flows.md)
- [Proxy Workflow](references/proxy.md)
- [Silmaril CDP Toolkit Repository](https://github.com/Malac12/CDP-tools.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell command examples, JSON flow snippets, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers JSON-producing browser automation commands and may direct creation of flow files or proxy override configuration.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
