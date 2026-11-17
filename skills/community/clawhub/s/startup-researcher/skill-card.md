## Description:

Researches AI startups, funding, and product announcements, then generates a structured intelligence report as a PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hxy9243](https://clawhub.ai/user/hxy9243)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to research AI startup watchlists, synthesize company and category intelligence, and produce styled market briefing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to install unpinned Python or system dependencies.

Mitigation: Review dependency commands before execution, install packages manually in an isolated virtual environment or container, and pin dependency versions for production use.

Risk: Generated reports may include a developer-controlled external attribution link.

Mitigation: Review the generated report header and footer before publication and remove or override attribution links that are not appropriate for the deployment.

Risk: Startup funding, valuation, product, and hiring details can be stale or incorrect if research sources are weak.

Mitigation: Require citations from current primary or trusted sources and have a reviewer confirm high-impact claims before business use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hxy9243/skills/startup-researcher)
- [README](artifact/README.md)
- [Company Research Prompt](artifact/prompts/company_research.md)
- [Market Analysis Prompt](artifact/prompts/market_analysis.md)
- [Report Compiler Prompt](artifact/prompts/report_compiler.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report and PDF generation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write intermediate company profiles, final Markdown, HTML, and PDF files in the workspace.]

## Skill Version(s):

1.3.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
