## Description:

Randomly recommends satirical S.H.I.T Journal (构石期刊) papers in response to Chinese or English prompts for humorous academic paper suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fasenchen](https://clawhub.ai/user/fasenchen)

### License/Terms of Use:


## Use Case:

External users ask an agent for a random humorous or satirical academic paper recommendation from S.H.I.T Journal. The skill guides the agent to browse the disclosed site, choose an available paper, and present the recommendation with title, author details, summary, DOI, and section.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad prompts such as requests for a random paper may invoke the skill and browse a site that may show 18+ content or consent gating.

Mitigation: Use the skill only where satirical S.H.I.T Journal browsing is intended, and have the agent respect site consent gates and user suitability before presenting content.

Risk: Some papers may require login or may be unavailable in the selected section.

Mitigation: If a selected paper or section cannot be accessed, switch to another available section or clearly state that full details could not be retrieved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fasenchen/skills/shit-journal)
- [S.H.I.T Journal preprints](https://shitjournal.org/preprints)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown recommendation with paper metadata, summary, DOI, and selected section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The recommendation depends on currently accessible content from the disclosed S.H.I.T Journal website.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
