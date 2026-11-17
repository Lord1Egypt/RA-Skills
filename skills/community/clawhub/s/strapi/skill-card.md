## Description:

Manage Strapi CMS content through the official @strapi/client SDK, including CRUD for collection and single types, media uploads, schema introspection, i18n localization, draft/publish workflows, edit form layout, users, roles, authentication, and raw Strapi API requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilya-ryzhov](https://clawhub.ai/user/ilya-ryzhov)

### License/Terms of Use:

MIT

## Use Case:

Developers and content operators use this skill to inspect and manage a Strapi v5 headless CMS from an agent workflow, including content entries, media, localization, publishing state, schema information, and selected administrative resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad authenticated CMS, user, file, and raw API operations.

Mitigation: Install it only for a trusted Strapi instance and use a narrowly scoped API token rather than a full-access token.

Risk: Destructive content, schema, user, locale, and media operations can change or delete data.

Mitigation: Manually confirm destructive operations before execution, and restrict schema and layout changes to local or development Strapi instances.

Risk: Account authentication, registration, password reset, and user management can expose sensitive credentials or account state.

Mitigation: Avoid using the skill for account authentication, registration, password reset, or password handling unless secret redaction and operational controls are in place.

Risk: Media upload supports local file paths and URL-based downloads.

Mitigation: Use only approved local paths and trusted HTTPS URLs; avoid arbitrary local file paths or remote media URLs until source constraints are enforced.

## Reference(s):

- [Strapi CMS on ClawHub](https://clawhub.ai/ilya-ryzhov/skills/strapi)
- [ClawHub publisher profile: ilya-ryzhov](https://clawhub.ai/user/ilya-ryzhov)
- [@strapi/client SDK](https://github.com/strapi/client)
- [OpenClaw](https://github.com/open-claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON arguments, and structured command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, STRAPI_API_TOKEN, and STRAPI_BASE_URL; operations act on the configured Strapi instance.]

## Skill Version(s):

1.0.0 (source: package.json, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
