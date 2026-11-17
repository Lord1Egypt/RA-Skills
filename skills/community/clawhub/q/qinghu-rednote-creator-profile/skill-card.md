## Description:

Looks up a Xiaohongshu creator's profile by homepage link, including follower count, likes and saves, and biography.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and analysts use this skill to retrieve Xiaohongshu creator profile metrics from a supplied homepage link for creator evaluation and selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unpinned Node/npm tools can modify the host runtime and introduce unreviewed code.

Mitigation: Review the package and prefer a preinstalled, version-pinned qhkit rather than automatic installation.

Risk: Configuring a Qinghu API token on the host may expose a reusable credential.

Mitigation: Use a managed secret store and avoid placing tokens in shell history or shared configuration.

Risk: Profile lookups incur paid API credits, and charges can increase with result volume.

Mitigation: Estimate charges and obtain user consent before paid calls; limit call count and report actual credits spent.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-rednote-creator-profile)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown answer with creator metrics; tabular file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports credits spent on paid calls and may provide a data file for 10 or more records.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
