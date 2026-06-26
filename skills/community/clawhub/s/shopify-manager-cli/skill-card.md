## Description: <br>
Manage Shopify store products, metafields, metaobjects, blogs, articles, and files through the Shopify Admin GraphQL API using a Python CLI wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Asenwang](https://clawhub.ai/user/Asenwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators and developers use this skill to let an agent run Shopify Admin GraphQL commands for catalog, content, metadata, and file-management tasks. It is intended for authenticated Shopify stores configured with the required Admin API scopes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, upload, or delete Shopify store data. <br>
Mitigation: Use a dedicated least-privilege Admin API token and confirm destructive requests before execution. <br>
Risk: Commands may target the wrong Shopify store if environment variables are misconfigured. <br>
Mitigation: Verify SHOPIFY_STORE_URL before running commands and keep SHOPIFY_ACCESS_TOKEN in environment variables or a secret manager. <br>
Risk: Upload commands can send local files to Shopify. <br>
Mitigation: Review local file paths and file contents before allowing upload commands to run. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Asenwang/shopify-manager-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with shell commands, tables, and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Shopify environment variables for store URL, Admin API token, and API version.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
