## Description: <br>
Interact with Confluence Cloud via REST API. Use for space management, page operations (list, view, create, update, delete), content search (CQL queries), page tree navigation (parent/child), attachments, comments, and labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snowsand-enterprises](https://clawhub.ai/user/snowsand-enterprises) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation maintainers, and agents use this skill to inspect and manage Confluence Cloud spaces, pages, attachments, comments, labels, and CQL search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Confluence API token to read and manage live Confluence content. <br>
Mitigation: Use a least-privileged Confluence API token scoped to the intended spaces and rotate it according to your credential policy. <br>
Risk: Update, upload, delete, purge, label, and comment operations can change production documentation. <br>
Mitigation: Require manual confirmation before write or destructive operations, especially in production spaces. <br>
Risk: A misconfigured Confluence base URL can direct requests to the wrong tenant. <br>
Mitigation: Verify CONFLUENCE_BASE_URL before use and keep separate environment configurations for production and non-production tenants. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snowsand-enterprises/snowsand-confluence) <br>
- [Confluence Storage Format Reference](references/storage-format.md) <br>
- [Confluence Query Language Reference](references/cql.md) <br>
- [Atlassian Confluence REST API v2](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/) <br>
- [Atlassian Confluence REST API v1](https://developer.atlassian.com/cloud/confluence/rest/v1/intro/) <br>
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration notes, and JSON API responses from the helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script reads Confluence connection settings from environment variables and prints JSON for API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
