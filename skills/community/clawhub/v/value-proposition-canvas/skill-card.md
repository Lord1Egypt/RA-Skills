## Description:

Guides a user through a Value Proposition Canvas workshop that maps one persona or segment's jobs, pains, and gains to pain relievers, gain creators, and a products-and-services bundle using evidence-backed tables and explicit acceptance gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monikazapisek](https://clawhub.ai/user/monikazapisek)

### License/Terms of Use:

MIT-0

## Use Case:

Product designers, founders, and product teams use this skill to turn user research into a structured Value Proposition Canvas for one persona or segment at a time. When the user has no research yet, the skill provides a research collection plan before running the same evidence-based canvas workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workshop files may contain verbatim customer or interview quotes, including sensitive personal, customer, private URL, or proprietary details.

Mitigation: Redact secrets, personal data, customer names, private URLs, Slack content, and proprietary details before giving research material to the skill or saving outputs.

Risk: The workflow asks the user to choose output paths, which can lead to files being written outside the intended project area.

Mitigation: Use a dedicated project directory, prefer workspace-relative paths, avoid absolute paths outside the workspace, and check for existing files before writing.

Risk: Canvas quality can degrade if hypotheses are treated as validated findings or if acceptance gates are skipped.

Mitigation: Keep hypotheses visibly labeled, preserve source quotes for claims, and require explicit user approval before moving between workshop phases.

## Reference(s):

- [Server-resolved source import](https://github.com/monikazapisekstudio/design-engineering-playbook/tree/main/skills/value-proposition-canvas)
- [ClawHub skill page](https://clawhub.ai/monikazapisek/skills/value-proposition-canvas)
- [Methodology: Value Proposition Canvas](artifact/references/methodology-vpc.md)
- [Third-Party Attributions](artifact/ATTRIBUTION.md)
- [Strategyzer](https://www.strategyzer.com)
- [Interaction Design Foundation](https://www.interaction-design.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tables, workshop notes, research plans, and workshop files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary workshop output is vpc-result.md; the skill can also produce a starter shadow-backlog.md without priorities. UVP drafting remains user-authored after prioritization.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
