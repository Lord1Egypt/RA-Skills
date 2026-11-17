## Description:

Looks up Douyin creator profile information, including account details, creator positioning, and audience size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users can look up Douyin creator profile details and audience scale from a supported account ID or profile link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI package is unpinned and automatically accepted, creating supply-chain risk while handling credentials.

Mitigation: Pin the CLI to a reviewed version and control its dependencies before use.

Risk: Authentication details are supplied to the CLI, and creator profile inputs may be sent to SocialDataX.

Mitigation: Protect the local credential store and submit only profile inputs you are authorized to share.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-douyin-creator-profile)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON containing Douyin creator profile fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only profile lookup using one supported account identifier or profile URL.]

## Skill Version(s):

0.1.24 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
