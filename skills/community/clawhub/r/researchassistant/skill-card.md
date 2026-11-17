## Description:

Monitors research topics for new papers, conferences, and journals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eksubin](https://clawhub.ai/user/eksubin)

### License/Terms of Use:


## Use Case:

Researchers, developers, and technical teams use this skill to monitor configured research topics and receive concise updates about new papers, conference announcements, and journal publications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local configuration stores research topics, seen-item identifiers, and the last checked date, which may reveal confidential projects or strategic interests.

Mitigation: Review, restrict access to, or delete research_config.json when the configured topics or tracked items are sensitive.

## Reference(s):

- [ResearchMonitor ClawHub page](https://clawhub.ai/eksubin/skills/researchassistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown reports with inline shell commands and local JSON configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured topics, last-checked date, and seen-item identifiers to reduce repeat reports.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
