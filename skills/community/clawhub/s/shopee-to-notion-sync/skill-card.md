## Description:

Sync Shopee products into Notion using the local Node.js workflow only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cbbathaglini](https://clawhub.ai/user/cbbathaglini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to search Shopee products by keyword and sync selected product fields into a configured Notion database through a local Node.js workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sync flow writes Shopee product data to Notion and the security evidence recommends review before installing.

Mitigation: Run it only with an isolated Notion integration token scoped to the intended database, and add a preview or confirmation step before writes.

Risk: The security evidence reports unsafe command/input handling for keyword, limit, and target values.

Mitigation: Validate allowed targets, constrain limit to an expected numeric range, and safely pass keyword input before invoking the workflow.

Risk: The security evidence reports credentials are read from a fixed external workspace path.

Mitigation: Replace the hardcoded environment file path with an operator-controlled local configuration path and document the required variables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cbbathaglini/skills/shopee-to-notion-sync)
- [Publisher profile](https://clawhub.ai/user/cbbathaglini)
- [Shopee affiliate GraphQL endpoint](https://open-api.affiliate.shopee.com.br/graphql)
- [Notion API pages endpoint](https://api.notion.com/v1/pages)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Plain text execution summary with a local Node.js command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summary reports keyword, target, created count, updated count, and failed count.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
