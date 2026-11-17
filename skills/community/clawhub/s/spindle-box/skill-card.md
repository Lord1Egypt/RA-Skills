## Description:

主轴箱CAD图纸生成。当用户说"主轴箱"、"生成主轴箱图纸"、"做一个主轴箱"、"spindle-box"时使用此 skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[realsanyu](https://clawhub.ai/user/realsanyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect spindle-box design parameters, call the JXT mechanical parts APIs, review calculated values, and create a CAD drawing production sheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends spindle-box design parameters to jixietools.com.

Mitigation: Confirm that sharing the relevant design parameters with jixietools.com is acceptable before using the skill.

Risk: The workflow uses filename and guest_code values as sensitive links for continuing calculations and viewing generated results.

Mitigation: Treat filename and guest_code values as sensitive workflow links and avoid exposing them beyond intended collaborators.

Risk: The evidence notes a category ID mismatch that could fetch the wrong product set.

Mitigation: Verify the product category behavior with the publisher before relying on generated selections for production work.

## Reference(s):

- [Jixietools API base](https://jixietools.com/api/v1)
- [Spindle Box ClawHub release](https://clawhub.ai/realsanyu/skills/spindle-box)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Chinese Markdown with tables, inline shell commands, API request examples, and generated result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides a step-by-step interactive workflow and may return guest-accessible production sheet URLs after API calls complete.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
