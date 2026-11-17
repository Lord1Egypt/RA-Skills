## Description:

Keyword research and analysis skill for any website. Performs systematic keyword discovery, competitive gap analysis, intent classification, difficulty scoring, and priority ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meikidd](https://clawhub.ai/user/meikidd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, SEO practitioners, and developers use this skill to discover keyword opportunities, compare competitor coverage, classify search intent, and produce a prioritized keyword research report for a target website.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain business context, target regions, languages, competitors, and tool-access preferences in local per-domain profile files.

Mitigation: Review the profile contents before reuse and delete local profile files when business context should not be retained.

Risk: Browser-based SEO workflows may use logged-in Google Search Console, Google Ads, Ahrefs, or Semrush sessions when access is granted.

Mitigation: Grant access only to accounts and properties intended for the analysis, and review exported or scraped SEO data before sharing it.

Risk: The release has no server-resolved import provenance for this version.

Mitigation: Install from a pinned ClawHub version or reviewed source when provenance is required for supply-chain review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meikidd/skills/seo-keyword-research)
- [Keyword research README](README.md)
- [Keyword optimization methodology](references/methodology.md)
- [Keyword research tools playbook](references/tools.md)
- [GSC web UI playbook](references/gsc-operations.md)
- [Claude Code skills documentation](https://docs.anthropic.com/en/docs/claude-code/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with tables and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save or update per-domain JSON profile files for future keyword research sessions.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
