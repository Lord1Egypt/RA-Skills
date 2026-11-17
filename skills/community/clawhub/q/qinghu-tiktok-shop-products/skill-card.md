## Description:

Looks up indexed TikTok Shop products by seller ID through Qinghu's data service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shop operators and market researchers use this skill to review the products indexed for a TikTok Shop seller and compare competitors' assortments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing Node or qhkit can change the local environment.

Mitigation: Review the package before installation, prefer a pinned version, and install only with explicit user approval.

Risk: Persistent qhkit configuration can expose a token to later calls.

Mitigation: Let the user control token setup; avoid persistent storage unless they accept reuse of that credential.

Risk: Product lookups can incur Qinghu credits, with higher charges for larger results.

Mitigation: Estimate costs and obtain consent before paid calls or large result sets.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-tiktok-shop-products)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise product summary with optional tabular file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports credit usage for paid queries.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
