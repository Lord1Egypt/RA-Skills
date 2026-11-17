## Description:

Searches Vipshop (vip.com) promotions and summarizes current or upcoming campaign names, timing, brands, links, and images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vip](https://clawhub.ai/user/vip)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers or shopping agents use this skill to check current and upcoming Vipshop promotions and summarize campaign status, timing, brands, links, and images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Vipshop login tokens from the user's home directory.

Mitigation: Use only in a trusted environment, confirm the token file path before execution, and avoid exposing token contents in logs or chat output.

Risk: The skill sends authenticated requests to Vipshop using account cookies.

Mitigation: Require explicit user approval before authenticated network access and review the target endpoint before running the query.

Risk: The skill can install or execute a separate login skill without a clear approval boundary.

Mitigation: Review and pin the login dependency, and require user approval before installing or launching any login workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vip/skills/vip-promotion-search)
- [Vipshop promotion API endpoint](https://api.union.vip.com/vsp/common/getActListForAI)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown summary with JSON data from the promotion query script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes activity counts, status and type groupings, promotion names, times, brands, links, and image URLs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
