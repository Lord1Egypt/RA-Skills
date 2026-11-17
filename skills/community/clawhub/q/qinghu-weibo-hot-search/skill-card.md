## Description:

Retrieves Weibo's current hot-search rankings through Qinghu's data tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

People tracking current Weibo trends use this skill to retrieve the hot-search ranking and summarize relevant topics, with consent before paid queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation or upgrade of unpinned qhkit and Node tooling may change local software unexpectedly.

Mitigation: Preinstall a reviewed, pinned qhkit version and approve tooling changes before use.

Risk: Local PATH changes and Qinghu API-token configuration affect the user's environment and credentials.

Mitigation: Review local configuration, avoid persistent PATH changes unless needed, and handle the token privately.

Risk: Hot-search queries are paid and charges can increase with the number of results.

Mitigation: Estimate the charge and obtain user consent before paid calls; report actual credits afterward.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-weibo-hot-search)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise trend summaries and ranking previews; tabular files for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid queries consume Qinghu credits; report the actual credits used.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
