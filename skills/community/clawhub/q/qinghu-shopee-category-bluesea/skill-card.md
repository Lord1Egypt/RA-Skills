## Description:

Helps agents analyze Shopee category opportunities by drilling from level-1 to level-3 categories and comparing market capacity, growth, competition, trend snapshots, rankings, and price distribution to identify high-growth, lower-competition niches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and agent users use this skill to evaluate Shopee market-entry categories, compare category size and growth, find lower-competition level-3 niches, and produce concise category recommendations with price-band guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Qinghu API calls require a bearer token and may consume Qinghu credits.

Mitigation: Confirm intended calls before execution, use the available Qinghu token only for this workflow, and report credit usage from the API response envelope when calls are made.

Risk: Category recommendations can be misleading if an API response is failed, incomplete, or parsed at the wrong response layer.

Mitigation: Check protocol errors, result.isError, and the parsed inner code and success fields before using returned data; stop and explain credential, permission, or parameter blockers instead of substituting another source.

Risk: The skill only supports category-level opportunity analysis and does not cover Shopee tax, certification, or local warehouse policy.

Mitigation: Present those areas as out of scope and require separate business or compliance review before acting on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-shopee-category-bluesea)
- [Qinghu Shopee data API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown recommendations with optional exported table files and inline JSON or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create table exports for larger record arrays; Qinghu API calls require user confirmation and may consume Qinghu credits.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
