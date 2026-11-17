## Description:

SEO Autopilot Pro automates SEO content freshness by monitoring keyword research reports, generating landing pages and blog posts, running SEO audits, and pushing site updates for Next.js, Astro, Nuxt, and static site projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennyzir](https://clawhub.ai/user/kennyzir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and SEO teams use this skill to convert keyword research reports into deployed landing pages and blog posts. It is intended for projects that want automated content freshness across supported web frameworks while preserving project style, sitemap registration, and basic SEO checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can automatically edit content, commit changes, push to main, and trigger production deployment from newly created report files without a clear review gate.

Mitigation: Use a dedicated branch or isolated clone, disable direct push to main, require diff review before commit, push, and deploy, stage only an explicit allowlist of generated files, and treat incoming report Markdown as untrusted data.

## Reference(s):

- [SEO Autopilot Pro on ClawHub](https://clawhub.ai/kennyzir/skills/seo-autopilot-pro)
- [Setup Checklist](references/setup-checklist.md)
- [Steering Template](references/steering-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets, code changes, and shell command proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project files, state tracking, navigation, sitemap entries, and git commits when run in an appropriately configured repository.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
