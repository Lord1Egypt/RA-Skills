## Description:

Helps agents advise on accelerating Webflow sites for users in mainland China with Cloudflare Worker reverse proxying, R2 asset caching, resource rewriting, and ICP/EdgeOne deployment options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenyeah](https://clawhub.ai/user/shenyeah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and Webflow site operators use this skill to diagnose slow or blocked Webflow resources for mainland China users and generate implementation guidance for Cloudflare Worker, R2 caching, resource rewriting, and optional ICP/EdgeOne architectures.

### Deployment Geography for Use:

China mainland-focused, with global Webflow and CDN edge deployments as part of the architecture.

## Known Risks and Mitigations:

Risk: Broad public proxying and caching could expose private pages or cache responses that should not be shared.

Mitigation: Add an exact allowlist for Webflow asset hosts, disable public caching for requests with cookies or authorization headers, and honor private or no-store origin headers.

Risk: Unbounded R2 writes through the Worker could be abused or create unexpected storage costs.

Mitigation: Limit R2 writes by content type, response status, object size, and approved upstream hosts before deployment.

Risk: The Worker template removes or hides the Webflow badge, which may change expected site attribution or terms-related behavior.

Mitigation: Remove the badge-hiding behavior unless the site owner has explicitly reviewed and accepted that change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenyeah/skills/webflow-china-speed)
- [Worker template](artifact/references/worker-template.js)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript Cloudflare Worker code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment prerequisites, diagnostic checks, caching and rewriting guidance, and a reusable Worker template.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
