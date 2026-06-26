## Description: <br>
Analyzes web performance using Chrome DevTools MCP. Measures Core Web Vitals (FCP, LCP, TBT, CLS, Speed Index), identifies render-blocking resources, network dependency chains, layout shifts, caching issues, and accessibility gaps. Use when asked to audit, profile, debug, or optimize page load performance, Lighthouse scores, or site speed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elithrar](https://clawhub.ai/user/elithrar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to audit page load performance, Core Web Vitals, network behavior, and accessibility gaps for websites or web apps. When source code is available, it also guides codebase-specific optimization analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect the target web project or target page through browser performance tooling. <br>
Mitigation: Run it only against projects and sites that the user intends the agent to inspect. <br>
Risk: The setup guidance uses an unpinned npx command for the Chrome DevTools MCP package. <br>
Mitigation: Review or pin the MCP package before running the command, especially in sensitive environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with tables, prioritized findings, recommendations, and optional code or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Core Web Vitals metrics, network findings, accessibility snapshot notes, and codebase findings when source is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
