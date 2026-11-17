## Description:

Searches Xiaohongshu notes by keyword, with optional filters for note type, publication time, and sort order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers and researchers use this skill to find Xiaohongshu notes on a topic or competitor, with optional time, format, and popularity filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches consume Qinghu credits, and larger results may cost more.

Mitigation: Estimate charges and get the user's consent before the first paid call or a large retrieval.

Risk: Installing or running the required Node package can introduce supply-chain exposure.

Mitigation: In controlled environments, approve and pin the qhkit version rather than allowing unreviewed global installs or latest-version execution.

Risk: Using the service requires a Qinghu API token.

Mitigation: Configure the token through the supported configuration or environment variable and avoid disclosing it in outputs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-rednote-note-search)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise findings with optional tabular data file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected keyword, filters, and the paid Qinghu service.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
