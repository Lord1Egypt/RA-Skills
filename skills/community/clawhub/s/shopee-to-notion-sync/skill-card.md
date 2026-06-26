## Description: <br>
Sync Shopee products into Notion using the local Node.js workflow only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cbbathaglini](https://clawhub.ai/user/cbbathaglini) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Shopee product offers and sync selected product records into a configured Notion database through a local Node.js workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product-search requests can result in writes to a Notion database without a separate confirmation step. <br>
Mitigation: Use the skill only for intended sync workflows, require operator confirmation before running the command, and keep product limits small. <br>
Risk: The workflow writes to Notion using configured credentials and database identifiers. <br>
Mitigation: Use a least-privilege Notion token shared only with the intended database and verify the configured environment path before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cbbathaglini/shopee-to-notion-sync) <br>
- [Shopee affiliate GraphQL endpoint used by the skill](https://open-api.affiliate.shopee.com.br/graphql) <br>
- [Notion pages API endpoint used by the skill](https://api.notion.com/v1/pages) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain-text execution summary with command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the keyword, target, created count, updated count, and failed count.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
