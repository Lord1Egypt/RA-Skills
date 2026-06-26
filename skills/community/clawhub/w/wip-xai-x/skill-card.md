## Description: <br>
X Platform API. Read posts, search tweets, get bookmarks, post tweets, upload media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to interact with the X Platform API for reading posts, recent search results, bookmarks, and user profiles. With OAuth credentials, it can also post, delete, bookmark, and upload media on the authenticated X account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can post, delete, bookmark, and upload media on a live X account when OAuth credentials are configured. <br>
Mitigation: Prefer read-only bearer-token configuration unless write actions are needed, and require explicit human confirmation before posting, deleting, bookmarking, or uploading media. <br>
Risk: The security summary reports that top-level metadata under-discloses deletion capability. <br>
Mitigation: Review the exposed tools before deployment and disclose that x_delete_tweet can delete posts from the authenticated X account. <br>
Risk: Media upload can read a local file path supplied to the tool. <br>
Mitigation: Limit the paths available to the agent and confirm the intended file before uploading media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parkertoddbrooks/wip-xai-x) <br>
- [Skill homepage](https://github.com/wipcomputer/wip-xai-x) <br>
- [X API base](https://api.x.com/2) <br>
- [X API documentation](https://docs.x.com/x-api) <br>
- [X API authentication documentation](https://docs.x.com/resources/authentication) <br>
- [X TypeScript SDK](https://github.com/xdevplatform/xdk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, API calls] <br>
**Output Format:** [JSON API responses and text output from MCP tools, module calls, or CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X API credentials; bearer tokens support read operations, while OAuth credentials enable write, delete, bookmark, and media upload actions.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release, SKILL.md frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
