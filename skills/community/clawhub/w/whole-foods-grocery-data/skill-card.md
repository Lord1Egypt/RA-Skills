## Description:

Whole Foods Market grocery data as structured JSON - search and browse the catalog of the store you choose with that store's shelf prices (regular, sale and Prime member price, with sale dates), list every product on sale at a store, read one product with ingredients, nutrition facts, diets and its in-store and online prices side by side, find stores near a ZIP, read one store's details, and pull its weekly sales flyer. 7 endpoints, 1 credit each.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External grocery shoppers and developers can use this skill to look up Whole Foods products, store-specific prices and deals, product details, nearby stores, and weekly sales flyers. It supports grocery research and price comparisons using live store data.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: ZIP codes and grocery searches are sent to Scavio, and each lookup consumes API credits.

Mitigation: Send only the ZIP code and search details needed for the request, and keep credit use in mind when making repeated lookups.

Risk: An exposed SCAVIO_API_KEY could allow unauthorized API use and consume account credits.

Mitigation: Store the key in an environment variable or secret store; do not place it in source code or shared configuration.

Risk: Optional SDK and MCP packages are outside the reviewed bundle; the documented MCP example enables Scavio's default platforms as well as Whole Foods.

Mitigation: Assess the packages separately before installing them and configure the MCP platform list for the tools you intend to use.

## Reference(s):

- [Whole Foods API overview](https://scavio.dev/wholefoods-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data)
- [Search endpoint documentation](https://scavio.dev/docs/wholefoods-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data)
- [Category endpoint documentation](https://scavio.dev/docs/wholefoods-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data)
- [Deals endpoint documentation](https://scavio.dev/docs/wholefoods-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data)
- [Product endpoint documentation](https://scavio.dev/docs/wholefoods-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data)
- [Stores endpoint documentation](https://scavio.dev/docs/wholefoods-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data)
- [Store endpoint documentation](https://scavio.dev/docs/wholefoods-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data)
- [Sales flyer endpoint documentation](https://scavio.dev/docs/wholefoods-sales-flyer?utm_source=agent-skills&utm_medium=skill&utm_campaign=whole-foods-grocery-data)

## Skill Output:

**Output Type(s):** [JSON, Grocery product, price, store, and promotion data]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Store-specific results; product listings are paginated.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
