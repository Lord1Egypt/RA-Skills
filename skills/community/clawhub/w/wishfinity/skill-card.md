## Description:

Save a product from any store to a Wishfinity wishlist. Connects the Wishfinity +W MCP server, which returns a save link the user opens to finish saving. Free Wishfinity account (created when the link is opened).

This skill is ready for commercial/non-commercial use.

## Publisher:

[leebellon](https://clawhub.ai/user/leebellon)

### License/Terms of Use:

MIT-0

## Use Case:

External users can give an agent a product page URL and receive a Wishfinity save link, then open that link to complete saving the product to their wishlist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local setup runs an unpinned package with npx.

Mitigation: Review the package before using the local setup; the hosted MCP endpoint is available as an alternative.

## Reference(s):

- [Wishfinity integrations](https://info.wishfinity.com/integrations/overview)
- [Wishfinity +W npm package](https://www.npmjs.com/package/wishfinity-mcp-plusw)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Markdown save link followed by JSON containing the same link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a link for the user to open and complete the save on Wishfinity.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
