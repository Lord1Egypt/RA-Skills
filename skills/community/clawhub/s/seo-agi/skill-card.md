## Description:

SEO AGI helps agents research search results, analyze content gaps, write SEO and GEO pages, validate quality, and prepare publish-ready content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbessoni](https://clawhub.ai/user/gbessoni)

### License/Terms of Use:

MIT-0

## Use Case:

SEO practitioners, content teams, and developers use this skill to turn a target keyword or existing page into research-backed SEO content with competitive gap analysis, structured tables, schema markup, source-verification tags, and final quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup handles API credentials and may expose plaintext secrets in local configuration or terminal output.

Mitigation: Use environment variables or a credential manager where possible, avoid printing credential files, and do not enter passwords in shared or recorded terminals.

Risk: Installation commands may affect the user's system Python environment.

Mitigation: Review setup steps before running them and install dependencies in a virtual environment.

Risk: Generated SEO claims, prices, schedules, or operational details may be inaccurate if not checked before publishing.

Mitigation: Keep the skill's verification tags in draft output and have a human reviewer confirm source-backed claims before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gbessoni/skills/seo-agi)
- [Publisher profile](https://clawhub.ai/user/gbessoni)
- [Page templates reference](artifact/references/page-templates.md)
- [Quality checklist](artifact/references/quality-checklist.md)
- [Schema markup patterns](artifact/references/schema-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown pages and briefs with inline code blocks, HTML tables, schema markup, verification tags, and supporting shell commands or configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce research summaries, gap reports, rewritten page drafts, change summaries, and schema blocks; some workflows depend on user-provided API credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
