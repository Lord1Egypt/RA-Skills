## Description:

Sellersprite Skills gives agents Amazon marketplace research workflows and tactical product-selection playbooks that use SellerSprite MCP tools for category, keyword, competitor, listing, traffic, review, pricing, and ad analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opensellersprite](https://clawhub.ai/user/opensellersprite)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace operators, ecommerce teams, and agents use this skill to structure Amazon product research, competitor review, keyword discovery, listing optimization, pricing analysis, and advertising recommendations from SellerSprite data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SellerSprite client requires access to a SellerSprite API key and marketplace research queries.

Mitigation: Install only in an environment where that access is acceptable, use a virtual environment, and protect API keys from logs or shared outputs.

Risk: The skill defaults many workflows to the US marketplace, which can produce misleading recommendations for other target markets.

Mitigation: Confirm the intended marketplace explicitly before running analysis instead of relying on the default.

Risk: Review analysis can involve reviewer-identifying or sensitive customer feedback data.

Mitigation: Avoid storing or sharing reviewer-identifying data unless it is necessary for the task.

Risk: The skill depends on the external `sellersprite-cli` package and MCP tool behavior.

Mitigation: Pin and verify the package version where possible before use in a managed environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/opensellersprite/skills/sellersprite-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, action checklists, command-oriented workflows, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on SellerSprite MCP tool responses, user-provided marketplace or ASIN inputs, and the configured SellerSprite client.]

## Skill Version(s):

0.1.16 (source: server release metadata; artifact frontmatter reports 0.1.17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
