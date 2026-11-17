## Description:

Fetches a webpage and converts its main content into clean Markdown while preserving image links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shijianwen](https://clawhub.ai/user/shijianwen)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to fetch public webpages, extract the main readable content, and return Markdown that can be summarized, saved, or processed downstream.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can request any URL reachable from the host network and return fetched content.

Mitigation: Use it only with public webpage URLs, avoid localhost, private network, cloud metadata, or secret-bearing URLs, and deploy behind URL allowlisting or private-network blocking where possible.

Risk: Dependency metadata has review-worthy supply-chain issues.

Mitigation: Review and pin dependencies, audit the package lock before deployment, and update to a release with audited dependency metadata when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shijianwen/skills/webfetch-md)
- [ClawHub publisher profile](https://clawhub.ai/user/shijianwen)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON object containing success status, title, markdown, images, imageCount, and contentLength.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves image links and resolves relative image and page links to absolute URLs.]

## Skill Version(s):

1.1.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
