## Description:

Automates distributing products from the 跨睿 curated product catalog to the Ozon ecommerce platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[famechyu](https://clawhub.ai/user/famechyu)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce operators use this skill to list products from the 跨睿 product catalog on Ozon. The agent collects category, store, and price range inputs, then runs browser automation to perform the distribution workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use embedded account credentials and an unencrypted HTTP connection during product distribution automation.

Mitigation: Remove embedded credentials, use per-user secrets, and require HTTPS before using the skill with real stores.

Risk: The workflow can submit commerce-related changes without reliable validation of category, store, and price selections or explicit final approval.

Mitigation: Gate submission on validated selections and require explicit user approval immediately before sending changes.

Risk: The artifact references a script path that differs from the included script filename, which can prevent the intended automation from running.

Mitigation: Align the documented script path with the packaged file and test the invocation before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/famechyu/skills/test-publish)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text task result with optional screenshot file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires category, store, and price range inputs; the automation script may save a screenshot file after execution.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
