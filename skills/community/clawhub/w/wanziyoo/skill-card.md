## Description:

Automates drafting and publishing Markdown posts for an Astro Koharu blog, including frontmatter, descriptions, tags, categories, and the site build.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctf010300-commits](https://clawhub.ai/user/ctf010300-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to create new Markdown blog posts for a specific Astro Koharu deployment, choose tags and categories, and run the production build after formal posts are created.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A successful build can update the pages served by the blog.

Mitigation: Review publish requests before invoking the skill and confirm the title, body, draft setting, category, and tags before accepting the build result.

Risk: File or command actions outside the intended blog workflow could modify sensitive or unrelated server content.

Mitigation: Limit use to creating new Markdown posts under the configured blog content directory and running the documented production build command.

## Reference(s):

- [Astro Koharu Blog Publish Rules](references/blog-publish-rules.md)
- [ClawHub skill page](https://clawhub.ai/ctf010300-commits/skills/wanziyoo)
- [ClawHub publisher profile](https://clawhub.ai/user/ctf010300-commits)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown response with generated blog files, YAML frontmatter, and build status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns title, file path, category, tags, build result, and publish status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
