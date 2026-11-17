## Description:

Inspect and analyze browser DevTools Console, Network, and Performance data to debug frontend issues such as JavaScript errors, failed requests, CORS problems, and slow page loads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qtadagm](https://clawhub.ai/user/qtadagm)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to capture browser console logs, network requests, CORS diagnostics, and performance metrics from real pages while debugging frontend applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser inspection can expose sensitive console and network data from arbitrary sites.

Mitigation: Use local or staging targets where possible, capture production data only with authorization, and redact headers, tokens, cookies, and PII before sharing output.

Risk: The bundled scripts launch browser automation with sandbox-disabling flags.

Mitigation: Run the scripts in an isolated container or VM and enable Chromium sandboxing where possible.

Risk: Performance and network captures can be misread as complete diagnosis without application context.

Mitigation: Treat script output as diagnostic evidence and verify findings against application logs, backend metrics, and source code before making changes.

## Reference(s):

- [Common Frontend Issues & Solutions](references/common-issues.md)
- [ClawHub skill page](https://clawhub.ai/qtadagm/skills/qtada-browser-devtools-inspector)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; bundled scripts emit structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 14+, Puppeteer, and Chrome/Chromium; outputs may include sensitive browser console, network, header, token, cookie, or PII data.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
