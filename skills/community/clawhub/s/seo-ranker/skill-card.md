## Description:

Meta-skill for end-to-end SEO auditing and on-page optimization by orchestrating brave-search, summarize, api-gateway, and markdown-converter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

External users, SEO practitioners, and developers use this skill to diagnose why a page is not ranking for a target keyword, compare it with live SERP competitors, and produce rewrite guidance, optimized Markdown, backlink opportunities, and ordered next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses unpinned remote installers and broad `update --all` behavior.

Mitigation: Install in an isolated environment, pin ClawHub CLI and dependency versions where possible, and update only the specific upstream skills needed for the run.

Risk: The workflow may send keywords, page content, drafts, or local files to named external providers through required tools and API keys.

Mitigation: Expose only the keys needed for the selected run and avoid submitting confidential drafts or files unless the user has approved sharing them with those providers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/h4gen/skills/seo-ranker)
- [Inspected upstream skills](references/inspected-skills.md)
- [Semrush official trial entry page](https://www.semrush.com/sem/)
- [Ahrefs Webmaster Tools](https://ahrefs.com/webmaster-tools)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with structured sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include SERP findings, data-gate status, optimized Markdown, backlink opportunities, missing-key disclosures, and ordered next actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
