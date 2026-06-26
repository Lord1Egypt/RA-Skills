## Description: <br>
Helps developers optimize Webflow sites for mainland China access with Cloudflare Worker reverse proxy guidance, R2 asset caching, blocked-resource removal, CDN mirror substitution, and optional ICP and EdgeOne architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenyeah](https://clawhub.ai/user/shenyeah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to diagnose Webflow performance problems for users in mainland China and generate Worker, R2 caching, resource rewriting, DNS, CDN, and ICP implementation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included Worker can fetch and persistently cache overly broad content. <br>
Mitigation: Review and edit the Worker before deployment, add a strict allowlist for Webflow asset hosts in /_cdn/, and use a dedicated R2 bucket. <br>
Risk: The Worker changes site branding and SEO-related files. <br>
Mitigation: Remove Webflow badge-hiding rules unless the site owner has explicit rights, and decide explicitly whether robots.txt and sitemap.xml should come from R2. <br>
Risk: Cached assets can remain stale after Worker behavior changes. <br>
Mitigation: Document how to purge cached assets and clear affected R2 objects after code updates. <br>


## Reference(s): <br>
- [Worker template](references/worker-template.js) <br>
- [ClawHub skill page](https://clawhub.ai/shenyeah/webflow-china-speed) <br>
- [Publisher profile](https://clawhub.ai/user/shenyeah) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Cloudflare Worker code, R2 and DNS configuration steps, diagnostic checklists, and deployment cautions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
