## Description: <br>
Use when the user wants direct Shopify runtime access through one configured store: inspect setup status, search Shopify docs, or execute JavaScript against the configured store. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ypyf](https://clawhub.ai/user/ypyf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check Shopify runtime configuration, search Shopify provider and official documentation, and run narrow scripts against one configured Shopify store. It is intended for store-specific troubleshooting and controlled Admin API reads or writes through an installed Shopify app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can give an agent direct Shopify Admin API access to the configured store. <br>
Mitigation: Use a dedicated least-privilege Shopify app, configure only the required scopes, and keep the read-only mode as the default. <br>
Risk: Write-mode scripts can change Shopify store data when the app token has matching permissions. <br>
Mitigation: Review write scripts before execution and use write mode only for clearly requested store changes. <br>
Risk: Order and customer queries may expose sensitive or protected data. <br>
Mitigation: Avoid broad customer or order payloads unless necessary, and return concise structured summaries where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ypyf/shopify-runtime) <br>
- [Runtime Contract](references/runtime-contract.md) <br>
- [Shopify Provider Notes](references/shopify-provider.md) <br>
- [Shopify Admin GraphQL API](https://shopify.dev/docs/api/admin-graphql) <br>
- [Shopify GraphQL queries basics](https://shopify.dev/docs/apps/build/graphql/basics/queries) <br>
- [Shopify GraphQL mutations basics](https://shopify.dev/docs/apps/build/graphql/basics/mutations) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON runtime output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Execution results can include request summaries, raw response excerpts, warnings, logs, and errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
