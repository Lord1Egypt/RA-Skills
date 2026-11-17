## Description:

Queries Uniqlo discounted products for men, women, kids, and baby clothing and generates a Markdown report with product images, prices, discount rates, and purchase links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpyangyoujun](https://clawhub.ai/user/gpyangyoujun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find discounted Uniqlo China products by category and optional size, then review a generated Markdown product report with images, prices, discount rates, and purchase links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Uniqlo China's API during normal use.

Mitigation: Run it in an environment where external network access to Uniqlo China is expected and allowed.

Risk: The skill creates timestamped Markdown files in a unique/ folder under the current working directory.

Mitigation: Run it from an intended working directory and review generated files before sharing them.

Risk: The only declared dependency is unpinned.

Mitigation: Install in an isolated environment and pin dependencies for reproducible or security-reviewed deployments.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Files, API Calls]

**Output Format:** [Plain-text response plus a timestamped Markdown file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates files in a unique/ directory under the current working directory.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
