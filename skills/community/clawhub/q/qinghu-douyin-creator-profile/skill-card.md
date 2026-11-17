## Description:

Given a Douyin creator profile URL, this skill retrieves follower, following, post, and like counts alongside profile details through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and analysts use this skill to look up Douyin creator profile metrics and summarize account performance from a supplied profile URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or updating third-party tooling and setting a token may make persistent changes to the local environment.

Mitigation: Use pre-provisioned or sandboxed tooling and review installation and token configuration before allowing changes.

Risk: Paid lookups can consume Qinghu credits, with final charges varying by returned results.

Mitigation: Check the current estimate and obtain user consent before paid calls; report the actual credits used.

Risk: Unpinned package installation or execution can reduce reproducibility.

Mitigation: Pin the qhkit version rather than using unpinned npx or @latest where reproducibility matters.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-douyin-creator-profile)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown summary with creator metrics; tabular file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid lookups require user approval; reported metrics depend on the Qinghu response.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
