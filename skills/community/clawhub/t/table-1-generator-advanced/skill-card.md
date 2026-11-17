## Description:

Automated generation of baseline characteristics tables (Table 1) for clinical research papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical researchers, analysts, and developers use this skill to generate reproducible baseline characteristics tables from patient CSV datasets, with optional group comparisons and publication-oriented summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical research datasets may contain sensitive patient information in input or generated output files.

Mitigation: Run the skill in an appropriate protected workspace and keep input and output files within approved data-handling boundaries.

Risk: Unpinned dependencies can change behavior or introduce supply-chain risk over time.

Mitigation: Install in a virtual environment and pin dependency versions before operational use.

Risk: Opening generated CSV files from untrusted datasets in spreadsheet software can expose users to formula-like cell behavior.

Mitigation: Review or neutralize formula-like cell values before opening generated CSV outputs in spreadsheet applications.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/table-1-generator-advanced)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated CSV or Excel table files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces baseline summaries, statistical test results, missing-data reporting, and publication-oriented Table 1 output from local datasets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
