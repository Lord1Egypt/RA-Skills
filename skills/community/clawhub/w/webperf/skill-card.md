## Description: <br>
Web performance measurement and debugging toolkit for auditing pages, analyzing Core Web Vitals, and investigating loading, interaction, media, and network quality issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nucliweb](https://clawhub.ai/user/nucliweb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and performance engineers use this skill to choose Chrome DevTools workflows for page audits, Core Web Vitals debugging, loading investigations, interaction analysis, media optimization, and network quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to run JavaScript in a browser page context, which can expose sensitive page state on logged-in or private sites. <br>
Mitigation: Use it only on pages intended for audit, avoid sensitive authenticated sessions when possible, and review external snippets before execution. <br>


## Reference(s): <br>
- [Webperf snippets repository](https://github.com/nucliweb/webperf-snippets) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, markdown] <br>
**Output Format:** [Markdown guidance with Chrome DevTools tool calls and JavaScript snippet recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to run JavaScript in a browser page context and summarize performance findings with actionable recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
