## Description: <br>
Token Cockpit analyzes local OpenClaw or LLM usage logs to report token spend, project budgets, and estimate savings from model routing changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Token Cockpit to understand local agent token usage, monitor budget risk, and identify model-routing changes that may reduce LLM spend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw usage logs that may contain sensitive usage metadata. <br>
Mitigation: Analyze logs locally, prefer an explicit --logs path, and avoid sharing raw log contents unless the user asks for it. <br>
Risk: Built-in pricing may be outdated or incomplete, so dollar totals may be inaccurate. <br>
Mitigation: Treat dollar figures as estimates and use --pricing with current rates when exact billing numbers matter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chris-openclaw/token-cockpit) <br>
- [README](artifact/README.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports or JSON command output with concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dollar figures are estimates when pricing uses editable defaults; unknown model prices are flagged.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
