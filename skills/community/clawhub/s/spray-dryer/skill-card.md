## Description:

Generates spray dryer CAD drawing workflows by guiding users through product selection, parameter collection, calculation, production sheet creation, and status tracking through jixietools.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realsanyu](https://clawhub.ai/user/realsanyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and engineering teams use this skill to configure spray dryer design parameters, review calculated values, create a guest production sheet, and track CAD drawing generation through jixietools.com.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spray dryer design inputs and generated workflow identifiers are sent to jixietools.com without login.

Mitigation: Avoid confidential or proprietary engineering designs unless the external service is trusted for that data.

Risk: The documented spray dryer category ID is inconsistent with the product-list request category ID.

Mitigation: Verify the category and product selections before relying on generated CAD outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/realsanyu/skills/spray-dryer)
- [JixieTools API](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, API Calls]

**Output Format:** [Chinese-language conversational Markdown with curl commands, JSON examples, and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses guest production sheet identifiers and periodic status polling; no login is required for the documented workflow.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
