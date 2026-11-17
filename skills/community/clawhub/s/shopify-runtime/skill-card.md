## Description:

Use when the user wants direct Shopify runtime access through one configured store: inspect setup status, search Shopify docs, or execute JavaScript against the configured store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ypyf](https://clawhub.ai/user/ypyf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Shopify Runtime to inspect a single configured Shopify store, search Shopify API guidance, and run narrow JavaScript scripts for Admin API reads or approved writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses live Shopify credentials and can access store data.

Mitigation: Install only in a tightly controlled environment with least-privilege Shopify app scopes and a verified *.myshopify.com store domain.

Risk: Autonomous or untrusted prompts could supply scripts that attempt unintended store operations.

Mitigation: Use read mode by default, require clear user authorization before write mode, and review execution scripts before running them.

Risk: Raw response output may include sensitive customer, order, or store data.

Mitigation: Treat request summaries, raw responses, logs, and returned data as sensitive evidence and summarize them instead of copying large payloads.

## Reference(s):

- [Runtime Contract](references/runtime-contract.md)
- [Shopify Provider Notes](references/shopify-provider.md)
- [Shopify Admin GraphQL API](https://shopify.dev/docs/api/admin-graphql)
- [GraphQL Queries Basics](https://shopify.dev/docs/apps/build/graphql/basics/queries)
- [GraphQL Mutations Basics](https://shopify.dev/docs/apps/build/graphql/basics/mutations)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript snippets, and JSON runtime output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime execution can return status, result, logs, warnings, request summaries, raw responses, and errors; raw outputs may contain sensitive Shopify data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
