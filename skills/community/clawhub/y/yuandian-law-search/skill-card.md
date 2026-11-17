## Description:

Searches the YuanDian Open Platform for Chinese statutes, regulations, cases, and enterprise records to support legal analysis and research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT

## Use Case:

Legal professionals and agents use this skill to retrieve Chinese legal authorities, compare relevant cases, check citations, and assemble traceable legal research reports. It is also used for enterprise due diligence queries when the user explicitly requests company information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends running Codex with broad filesystem and approval bypass settings.

Mitigation: Do not follow that launch posture; grant only the network and file access needed for the specific legal search.

Risk: Legal queries, citation checks, and hallucination-detection text may be sent to an external API provider.

Mitigation: Configure the API key through a protected environment variable when possible and redact sensitive client facts before submitting text.

Risk: Search archives and generated reports can contain sensitive case facts, parties, judgments, or enterprise information.

Mitigation: Treat local archive and report files as sensitive case material, avoid committing them to public repositories, and disable report copies when they are not needed.

Risk: Aggressive search modes and enterprise lookups can increase data exposure and API credit consumption.

Mitigation: Use aggressive mode or enterprise lookups only when they are explicitly needed for the matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cat-xierluo/skills/yuandian-law-search)
- [Publisher profile](https://clawhub.ai/user/cat-xierluo)
- [Project homepage](https://github.com/cat-xierluo/legal-skills)
- [YuanDian Open Platform](https://open.chineselaw.com)
- [Research middleware workflow](artifact/references/07-research-middleware.md)
- [Typical legal search workflows](artifact/references/02-typical-workflows.md)
- [Legal research report template](artifact/templates/legal-research-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured legal-research reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured YuanDian API key; API calls consume credits and may archive reports locally.]

## Skill Version(s):

1.8.8 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
