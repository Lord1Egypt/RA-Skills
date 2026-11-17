## Description:

A bilingual Sora2 data assistant for querying posts, users, search, comments, Cameo appearances, downloads, and related platform data through the MaxHub API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[new-ironman](https://clawhub.ai/user/new-ironman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and product teams use this skill to inspect Sora2 content, user activity, comments, Cameo data, and download metadata, then summarize findings in English or Chinese. It can also upload images to the remote service to obtain media IDs for later Sora-related workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill claims read-only behavior but includes an image upload endpoint that can send user files to a third-party service.

Mitigation: Require explicit user confirmation before uploads and avoid uploading sensitive images.

Risk: Use requires sharing an API key and submitted data with MaxHub/aconfig.cn.

Mitigation: Install and run only when the operator trusts that service with the key and data.

Risk: The documented install command uses an unpinned npx invocation.

Mitigation: Pin the installer or package version during installation where the deployment process allows it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/new-ironman/skills/sora-aggregate-scraper)
- [Publisher profile](https://clawhub.ai/user/new-ironman)
- [MaxHub API website](https://www.aconfig.cn)
- [README](artifact/README.md)
- [中文 README](artifact/README_CN.md)
- [Post and User API reference](artifact/references/api-post-user.md)
- [Cameo API reference](artifact/references/api-cameo.md)
- [Parameter mappings](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API call guidance]

**Output Format:** [Markdown summaries, tables, links, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's language, humanizes numeric values, and omits API key values from responses.]

## Skill Version(s):

3.6.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
