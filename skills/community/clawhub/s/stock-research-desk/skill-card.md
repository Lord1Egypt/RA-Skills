## Description:

Claude Code skill for multi-agent equity research that produces buy-side memos with debate, scenario projection, and bilingual DOCX delivery for stock research, sector screening, and watchlist maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research teams use this skill to run multi-factor equity research workflows for single-name deep dives, sector or theme screens, and recurring watchlist reviews. It is intended to support research memos, not trading execution or personalized portfolio management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial research output may be mistaken for trading execution or personalized portfolio management.

Mitigation: Use outputs as research support only and require human review before investment decisions.

Risk: The skill may search external financial sources and rely on an OLLAMA_API_KEY from the environment.

Mitigation: Review configured credentials and external-source access before installation or execution.

Risk: The skill writes bilingual DOCX reports to the desktop.

Mitigation: Confirm the output location is appropriate for the workspace and does not expose sensitive research material.

## Reference(s):

- [Stock Research Desk homepage](https://github.com/wd041216-bit/stock-research-desk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell command examples and bilingual DOCX report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OLLAMA_API_KEY from the environment, may search external financial sources, and writes bilingual DOCX reports to the desktop.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
