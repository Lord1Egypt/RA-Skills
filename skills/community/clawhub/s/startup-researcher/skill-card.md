## Description: <br>
Research AI startups, funding, and product announcements. Generates a structured intelligence report as a PDF. Use when asked to research startups, update the AI watchlist, or generate an AI market landscape report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hxy9243](https://clawhub.ai/user/hxy9243) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and analysts use this skill to research AI startups from a watchlist, synthesize company profiles and category-level market analysis, and produce a styled briefing report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run brew, apt-get, dnf, or pip commands to install report-rendering dependencies. <br>
Mitigation: Review and approve dependency installation commands before execution. <br>
Risk: The skill writes local research and report artifacts that may contain sensitive analysis. <br>
Mitigation: Run it in a dedicated workspace and review generated files before sharing. <br>


## Reference(s): <br>
- [Startup Researcher README](README.md) <br>
- [Skill Definition](SKILL.md) <br>
- [Company Research Prompt](prompts/company_research.md) <br>
- [Market Analysis Prompt](prompts/market_analysis.md) <br>
- [Report Compiler Prompt](prompts/report_compiler.md) <br>
- [Startup Watchlist](watchlist.yaml) <br>
- [ClawHub Skill Page](https://clawhub.ai/hxy9243/startup-researcher) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and local PDF briefing artifacts, with shell commands for Markdown-to-PDF rendering] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces company profiles, category analysis, a final Markdown draft, HTML conversion output, and a styled PDF report.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
