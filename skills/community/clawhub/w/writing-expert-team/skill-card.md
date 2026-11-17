## Description:

Writing Expert Team is a Chinese-language, multi-role writing workflow for planning, researching, drafting, fact-checking, editing, compliance review, formatting, and optional publishing preparation for high-quality articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lawer-liu](https://clawhub.ai/user/lawer-liu)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and professionals use this skill to produce Chinese self-media, legal/science explainer, and platform-ready articles through a structured team-style workflow. It supports full-pipeline execution as well as single-role help for topic planning, style profiling, research, review, compliance checks, and layout export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated publishable content can include a hardcoded Real Estate Legal Eye slogan or other brand-specific phrasing.

Mitigation: Review final copy before publication and remove or replace brand lines that do not belong to the user's account or publication.

Risk: The redline checker can modify Markdown or text files when run with --fix.

Mitigation: Run the checker without --fix first, inspect reported issues, and keep backups before allowing automatic fixes.

Risk: Publishing and draft-push features can affect external accounts if enabled with API credentials.

Mitigation: Enable WeChat or other publishing API flows only for a reviewed final draft, the intended account, and an explicit user confirmation.

Risk: Legal, tax, medical, or other compliance-sensitive article outputs may contain outdated or incorrect claims.

Mitigation: Require source attribution, fact-check current authoritative sources, and obtain qualified review before publishing sensitive content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lawer-liu/skills/writing-expert-team)
- [Publisher Profile](https://clawhub.ai/user/lawer-liu)
- [README](README.md)
- [Role Definitions](references/roles.md)
- [Pipeline Flow](references/pipeline-flow.md)
- [Publishing Redlines](references/redlines.md)
- [Viral Formula](references/viral_formula.md)
- [Metadata Schema](references/metadata-schema.md)
- [Redline Checker](scripts/redline_check.py)
- [Sample Article](examples/sample_difayan_article.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown articles, YAML metadata blocks, review reports, layout instructions, optional shell commands, and publishing configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are primarily Chinese-language writing artifacts and review guidance; final publication remains subject to user review and confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
