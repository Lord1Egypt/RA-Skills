## Description: <br>
Routes agents to Yingmi financial data tools and remote workflows for fund research, portfolio diagnostics, risk analysis, financial planning, charting, HTML reports, and PDF generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yingmi-soc](https://clawhub.ai/user/yingmi-soc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to access Yingmi financial data workflows, including fund lookup, strategy research, portfolio diagnosis, risk backtesting, cash-flow analysis, and report generation. It acts as a local entry point that checks CLI readiness, chooses between atomic MCP tools and remote scenario skills, and applies the shared HTML report template when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or update an unpinned CLI and can route execution into remote child-skill instructions. <br>
Mitigation: Install only if you trust Yingmi and the yingmi-skill-cli supply chain; manually approve npm, sudo, and remote-skill commands, and verify the CLI source and version before use. <br>
Risk: Financial workflows may involve phone codes, API keys, household details, or detailed financial data. <br>
Mitigation: Enter sensitive values only when you intend to use this provider for the task, and avoid sharing unnecessary personal or financial information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yingmi-soc/yingmi-skill) <br>
- [CLI precheck workflow](artifact/references/CLI前置检查.md) <br>
- [MCP data authenticity requirements](artifact/references/MCP数据真实性零容忍.md) <br>
- [HTML report visual template](artifact/references/HTML视觉模板.md) <br>
- [Demo report template](artifact/references/demo-report.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, markdown, HTML, PDF, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON tool inputs, and optional HTML or PDF report artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an initialized yingmi-skill-cli environment and may route the agent to remote child skills for multi-step financial workflows.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
