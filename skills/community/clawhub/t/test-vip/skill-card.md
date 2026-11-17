## Description:

Helps an agent search for products, compare top results, and summarize price, satisfaction, and recommendation details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miketobusy](https://clawhub.ai/user/miketobusy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to search for products in categories such as apparel, beauty, and mother-and-baby goods. It summarizes top product candidates, compares pricing and satisfaction, and produces purchase recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented command pattern passes user-supplied search text to a helper script.

Mitigation: Review and package the helper script, pass search terms as safely quoted arguments, and avoid shell interpolation when invoking it.

Risk: The skill is not clearly packaged or narrowly scoped and relies on external product search behavior.

Mitigation: Disclose external search behavior, narrow activation to explicit product-search requests, and audit the installed artifact before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miketobusy/skills/test-vip)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with product comparison tables, summaries, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches up to five top product results and may coordinate product consultation for each result.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
