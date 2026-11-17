## Description:

Collects comments on a RedNote post from its link, with optional sorting and inclusion of replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

People analyzing RedNote audience feedback use this skill to retrieve comments for a post, optionally sorted or including replies, and summarize what commenters are saying.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or update unpinned Node and qhkit tooling on the user's machine.

Mitigation: Review and trust the tooling before installation; prefer a platform-managed or pinned qhkit version, and avoid automatic Node/npm bootstrapping unless approved.

Risk: Paid-service credentials may be persisted locally.

Mitigation: Use short-lived tokens or temporary environment configuration where possible; avoid storing long-lived credentials unless acceptable for the environment.

Risk: Comment collection may consume variable paid Qinghu credits.

Mitigation: Check the current estimate, disclose expected charges, and obtain user approval before paid calls or larger batches.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-rednote-comments)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include collected comments, a summary of feedback, and paid-service credit usage.]

## Skill Version(s):

0.1.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
