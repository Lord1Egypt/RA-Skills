## Description: <br>
Strapi CMS helps an agent manage Strapi content, media, schemas, layouts, users, locales, localization, and draft/publish workflows through a configured Strapi API token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilya-ryzhov](https://clawhub.ai/user/ilya-ryzhov) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, content teams, and site operators use this skill to inspect and administer Strapi CMS content, media, localization, schemas, layouts, and user records from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad token-backed changes to CMS content, schemas, users, raw API endpoints, and media uploads. <br>
Mitigation: Install it only for Strapi instances the agent is intended to administer, use a least-privilege token, and avoid Full Access unless required. <br>
Risk: Schema and layout operations can alter the CMS structure or admin form behavior. <br>
Mitigation: Test schema and layout changes on local or development instances first and require explicit confirmation before applying them. <br>
Risk: Delete, publish, user-management, raw fetch, and file-upload commands can have irreversible or security-sensitive effects. <br>
Mitigation: Require explicit confirmation for those actions and avoid uploading sensitive local files or untrusted URLs. <br>


## Reference(s): <br>
- [ClawHub Strapi CMS Skill](https://clawhub.ai/ilya-ryzhov/strapi) <br>
- [@strapi/client SDK](https://github.com/strapi/client) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STRAPI_API_TOKEN and STRAPI_BASE_URL; operations depend on the configured Strapi permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
