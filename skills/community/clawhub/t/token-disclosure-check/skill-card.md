## Description:

Checks token whitepapers and disclosure copy for total supply, allocation, lockup, team information, risk warnings, and language promising returns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and token-project reviewers use this skill to pre-screen disclosure text for missing required topics and promises of returns. Its results are not legal or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Declared agent tools include writing, web access, and broad shell use despite the skill's stated local-only permissions.

Mitigation: Review the skill before installation and limit agent permissions to reading inputs and running the local checker.

Risk: Simple Chinese keyword matching can miss disclosures or promises expressed differently and can produce misleading compliance results.

Mitigation: Treat results as a preliminary screen and have a qualified reviewer assess the full disclosure before making decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/token-disclosure-check)
- [LGD theory background (linked in README; not release provenance)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain-text checklist or JSON report when --json is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports missing disclosure topics and return-promise matches; exits 0 on pass and 1 on fail.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
