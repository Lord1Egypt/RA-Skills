## Description: <br>
Work with the WordPress REST API for route discovery, authentication, read and write operations, core endpoint selection, and custom namespace inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site operators use this skill to inspect a WordPress site's live REST routes, choose authentication patterns, and work with core or custom endpoints before API automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated calls may send WordPress application-password credentials to an unrelated URL when a full route URL is supplied. <br>
Mitigation: Use least-privilege application passwords, prefer relative routes such as /wp/v2/posts, avoid full --route URLs when credentials are present, and verify the final URL before authenticated calls. <br>
Risk: Write-capable WordPress REST operations can change content, settings, plugins, or themes. <br>
Mitigation: Require explicit approval before content, settings, plugin, or theme changes and inspect route permissions with OPTIONS before unfamiliar write automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/matthewxmurphy/wordpress-rest-api) <br>
- [Auth And Discovery](references/auth-and-discovery.md) <br>
- [Core Endpoints](references/core-endpoints.md) <br>
- [Custom Route Rules](references/custom-route-rules.md) <br>
- [WordPress REST API reference](https://developer.wordpress.org/rest-api/reference/) <br>
- [WordPress REST API authentication](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/) <br>
- [WordPress routes and endpoints handbook](https://developer.wordpress.org/rest-api/extending-the-rest-api/routes-and-endpoints/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell commands and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include route discovery steps, authentication guidance, endpoint choices, and review notes for custom WordPress REST routes.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
