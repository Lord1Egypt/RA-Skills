## Description: <br>
xbird lets agents read, search, and act on Twitter/X through a local MCP server with metered x402 calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[checkra1neth](https://clawhub.ai/user/checkra1neth) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use xbird to connect Claude Code to a local Twitter/X MCP server for reading timelines and search results, then performing account actions such as posting, replying, following, profile updates, and media uploads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Twitter/X session credentials and can make live public account changes. <br>
Mitigation: Use a dedicated low-risk account and require manual confirmation for posts, replies, retweets, follows, media uploads, and profile changes. <br>
Risk: The skill can use a wallet private key for x402 payments through an unpinned third-party npx package. <br>
Mitigation: Pin and inspect the npm package before use, avoid supplying the wallet private key unless necessary, and use a limited-funded wallet. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/checkra1neth/xbird) <br>
- [Publisher profile](https://clawhub.ai/user/checkra1neth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger live Twitter/X account actions and x402 payments through a local MCP server when configured.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
