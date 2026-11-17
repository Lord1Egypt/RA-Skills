## Description:

Zhiyan Smart Research helps an agent search Crossref and PubMed, synthesize literature findings, identify research gaps, and produce structured citation-backed research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users can use this skill to ask academic research questions and receive a structured Markdown report with references, literature review, research gaps, recommendations, and follow-up questions. The skill is designed for literature-search and synthesis workflows that rely on public Crossref and PubMed data plus the user's configured OpenClaw LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted input may affect command execution if an agent or host shell interpolates user-provided research topics into commands.

Mitigation: Review generated commands before execution and pass user queries as direct arguments with proper quoting instead of shell interpolation.

Risk: Session-file handling may allow unexpected writes if a supplied session id is not constrained.

Mitigation: Validate session ids and keep all saved reports within the skill-local research/sessions directory.

Risk: Research queries are sent to public Crossref and PubMed endpoints, and generated reports are stored locally.

Mitigation: Avoid submitting sensitive research topics to public APIs and review local session files before sharing or publishing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/caoling7878-arch/skills/zhiyan-smart-research)
- [Usage Guide](artifact/USAGE.md)
- [Report Template](artifact/templates/report-template.md)
- [Examples](artifact/examples.md)
- [Crossref Works API](https://api.crossref.org/works)
- [PubMed E-utilities Search API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi)
- [PubMed E-utilities Summary API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown research reports with citation markers, JSON paper search results, shell commands for search and save operations, and local Markdown session files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports follow a six-section template and saved sessions are stored under the skill-local research directory.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and changelog describe v1.1.0 behavior)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
