## Description:

Enables an agent to create, manage, and publish a full-featured blog with posts, media uploads, theme switching, database and cache adapters, and Vercel or Cloudflare deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harshraj001](https://clawhub.ai/user/harshraj001)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to let an agent run a blog platform: create and manage Markdown posts, upload media, switch visual themes, configure storage and caching, and deploy the site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary says this release has concrete security risks that should be reviewed before installation or deployment.

Mitigation: Patch the skill before public exposure: narrow activation triggers, upgrade Next.js and affected dependencies, replace the HTML and Markdown rendering path with a maintained sanitizer, remove eval from setup.sh, avoid unpinned npx deployment tools, prevent API keys from being printed to logs, and use scoped deployment and API credentials.

## Reference(s):

- [Write My Blog Skill Page](https://clawhub.ai/harshraj001/skills/write-my-blog)
- [API Reference](references/api-reference.md)
- [Theme Guide](references/theme-guide.md)
- [Environment Configuration Template](templates/env.example.txt)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, REST API examples, configuration files, and blog content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and manages blog posts, media references, theme settings, deployment steps, and platform configuration.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
