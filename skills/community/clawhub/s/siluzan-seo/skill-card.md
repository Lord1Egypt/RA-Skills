## Description:

Generates structured JSON SEO packages for industrial B2B websites, including traffic landing pages, blog SEO packages, and backlink article packages aligned to the included output schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sigedev01-bit](https://clawhub.ai/user/sigedev01-bit)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams and agents use this skill to create CMS-ready SEO JSON for industrial B2B landing pages, blog packages, and guest-post packages from supplied title, keyword, and knowledge-base context. It is intended for schema-conformant SEO content generation rather than general copywriting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One-click installation asks agents to run remote shell or PowerShell scripts and install software globally.

Mitigation: Review the installer first, prefer a manual pinned install, and avoid running it with administrator or root privileges.

Risk: The installer can force-write skill files across multiple global AI assistant directories.

Mitigation: Register the skill only in the specific assistant directory needed for the deployment.

Risk: The installer may change the npm registry setting to a mirror.

Mitigation: Check npm registry settings after installation and restore the expected registry for the environment.

Risk: Generated SEO content may contain unsupported claims when knowledge-base context is incomplete or when synthetic review-like content is allowed by the artifact workflow.

Mitigation: Review generated JSON against authoritative company sources before publishing and remove unverifiable customer, certification, or performance claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sigedev01-bit/skills/siluzan-seo)
- [Siluzan homepage](https://www.siluzan.com)
- [Installation and configuration](references/setup.md)
- [Word and PDF export](references/export.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Structured JSON conforming to the included output schemas, with plain-text English content and Chinese summary or translation fields where required.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes schemas for traffic pages, blog SEO packages, and backlink article packages; CLI export can produce Word or PDF review copies from generated JSON.]

## Skill Version(s):

1.1.30 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
