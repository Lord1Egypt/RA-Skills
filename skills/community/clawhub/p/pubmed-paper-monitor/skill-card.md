## Description:

Monitor journals precisely via ISSN lookup to track new PubMed papers with bilingual titles and detailed metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenghan66](https://clawhub.ai/user/chenghan66)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers and research teams use this skill to monitor specified journals for recent PubMed papers, retrieve article metadata, and present English titles with professional Chinese translations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PubMed queries are sent to NCBI using the bundled script's hard-coded Entrez email address.

Mitigation: Review the network disclosure and prefer a version that lets users configure the Entrez email before installation.

Risk: Large result sets may be saved automatically to the user's Desktop.

Mitigation: Confirm whether automatic report saving is acceptable and prefer a configurable output path for routine use.

Risk: The dependency installation guidance does not pin Biopython to a reviewed version.

Mitigation: Install a reviewed, pinned Biopython version in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenghan66/skills/pubmed-paper-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with bilingual titles and JSON data returned by the bundled PubMed monitor script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a detailed bilingual report file for large result sets.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
