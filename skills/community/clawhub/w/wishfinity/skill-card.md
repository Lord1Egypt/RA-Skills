## Description: <br>
Adds save-for-later support to shopping agents and AI commerce experiences by saving product URLs to a universal Wishfinity wishlist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leebellon](https://clawhub.ai/user/leebellon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External shopping and commerce agents use the skill to offer users a save-for-later action for product recommendations, gift ideas, deals, and product research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external npm MCP server package. <br>
Mitigation: Install only if you trust Wishfinity and the wishfinity-mcp-plusw package; pin the package version when your environment supports it. <br>
Risk: Saved product URLs may contain private tokens, personal identifiers, or session-specific information. <br>
Mitigation: Review product URLs before saving and avoid sending links that include sensitive query parameters or personal data. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/leebellon/wishfinity) <br>
- [Wishfinity homepage](https://wishfinity.com) <br>
- [Wishfinity MCP server](https://github.com/wishfinity/wishfinity-mcp-plusw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON configuration and MCP tool output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MCP server configuration and a Wishfinity account; the MCP tool returns an action URL and display text for the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
