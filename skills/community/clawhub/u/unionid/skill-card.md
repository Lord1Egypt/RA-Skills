## Description:

Uses a WeChat unionid to look up associated JD.com pay/login PINs and basic account information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuoxiangpang](https://clawhub.ai/user/zhuoxiangpang)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized operators use this skill to perform one-off identity-linkage checks between a WeChat unionid and associated JD.com account records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive identity linkage from a WeChat unionid to JD.com account data without visible authorization controls.

Mitigation: Install only in tightly controlled environments where operators have documented approval for this exact lookup workflow, and audit every lookup.

Risk: Excessive disclosure because the artifact asks for linked identifiers and all account fields.

Mitigation: Restrict database credentials and returned fields to the minimum necessary, and mask identifiers and sensitive profile attributes.

Risk: Bulk enumeration or repeated lookups could expose linked account information at scale.

Mitigation: Reject bulk enumeration workflows and monitor lookup volume before using the skill with real user data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuoxiangpang/skills/unionid)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown or plain text with retrieved account fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a WeChat unionid and may include sensitive account identifiers and basic profile attributes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
