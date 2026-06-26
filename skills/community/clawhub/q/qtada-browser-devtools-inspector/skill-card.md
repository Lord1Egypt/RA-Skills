## Description: <br>
Inspect and analyze browser DevTools Console, Network, and Performance data to debug frontend issues like errors, failed requests, CORS, and slow loads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QtadaGM](https://clawhub.ai/user/QtadaGM) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to capture browser console, network, CORS, and performance diagnostics from real browser sessions and turn them into structured debugging evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved DevTools captures may include internal URLs, response headers, stack traces, or tokens embedded in URLs. <br>
Mitigation: Treat generated JSON as sensitive, redact it before sharing, and avoid committing captures to source control. <br>
Risk: Running browser diagnostics against hostile or sensitive internal sites can expose data from those pages to local logs and output files. <br>
Mitigation: Prefer local or trusted development URLs and run the scripts in an isolated environment when testing untrusted pages. <br>


## Reference(s): <br>
- [Common Frontend Issues & Solutions](references/common-issues.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON outputs from the bundled Node.js scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts can emit structured JSON captures for console logs, network requests, CORS issues, and performance metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
