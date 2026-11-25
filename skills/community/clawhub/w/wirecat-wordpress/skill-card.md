## Description:

Use wordpress to read and write the owner's self-hosted WordPress site, its posts and pages with every status, their text as Markdown, tags, categories and authors, synced into the local WireCat store, and write drafts, update them, publish or schedule, unpublish and trash, with the owner's profile and JSON answers. Use when a task needs what the owner published or drafted on WordPress, a draft written from notes, a post published or scheduled, or a WordPress API operation (media, comments, menus).

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

WordPress site owners use the skill to inspect their posts, pages, users, and site data, and to draft or manage content through their configured profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment was partial because two local path-like references could not be resolved; its confidence is medium.

Mitigation: Review the skill and unresolved references before installation.

Risk: Publishing makes content public immediately, and delete operations can move content to the trash or permanently remove it.

Mitigation: Confirm the profile, item, and requested action before writes; publish only when explicitly requested and avoid permanent deletion unless specifically requested.

## Reference(s):

- [Wordpress Cli on ClawHub](https://clawhub.ai/wirecat/skills/wirecat-wordpress)
- [WordPress API overview](references/api.md)
- [Posts API commands](references/api/api-posts.md)
- [Pages API commands](references/api/api-pages.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands]

**Output Format:** [JSON answers and Markdown content, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the configured WordPress profile and its permissions.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
