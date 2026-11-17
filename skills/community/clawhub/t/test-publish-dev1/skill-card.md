## Description:

Automatically distributes products from the Kuarui product catalog to the Ozon e-commerce platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[famechyu](https://clawhub.ai/user/famechyu)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce operators use this skill to collect a product category, store, and price range, then trigger automated product distribution to Ozon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can log into a fixed remote service and trigger product-distribution actions automatically.

Mitigation: Use it only for endpoints and accounts the operator is authorized to control, and require explicit user confirmation before submission.

Risk: Release evidence reports embedded credentials and plaintext HTTP.

Mitigation: Rotate the credential out of source code, store secrets securely, and require HTTPS before installation or execution.

Risk: Release evidence reports that submission can proceed even when required selections fail.

Mitigation: Gate submission on validated category, store, and price-range selections before clicking the send action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/famechyu/skills/test-publish-dev1)
- [ClawHub publisher profile](https://clawhub.ai/user/famechyu)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text task status and execution result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a local screenshot file when the automation script completes.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
