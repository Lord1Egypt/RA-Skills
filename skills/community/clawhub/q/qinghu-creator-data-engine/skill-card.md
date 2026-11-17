## Description:

Collects public creator-profile metrics from Douyin, Xiaohongshu, and Bilibili and exports an Excel table for monitoring creators and competitor accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers and creator-management teams use the skill to collect account and playback metrics for up to five public creator profiles per run, track partner performance, and export competitor-account data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running a third-party CLI requires supplying a Qinghu API token.

Mitigation: Use a reviewed or pinned qhkit installation where required and handle the token as a secret.

Risk: Submitting creator profile URLs may incur charges or require a subscription.

Mitigation: Check the live estimate and subscription status, and obtain user confirmation before submission.

Risk: Commercial use of creator material without permission may raise rights concerns.

Mitigation: Use only material the user owns or is authorized to process.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-creator-data-engine)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance and commands with an XLSX download link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One-time export for up to five creator-profile URLs; scheduled updates require separate setup.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
