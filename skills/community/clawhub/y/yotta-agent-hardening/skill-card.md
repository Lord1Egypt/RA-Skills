## Description:

This skill statically scans an authorized AI agent environment for prompt-injection exposure, tool-boundary issues, and data-isolation risks, then produces a hardening report and defense guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use it to assess the configuration and data-access exposure of agent environments they own or are authorized to inspect. It produces findings and practical guardrails for hardening those environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Symbolic links can lead a scan beyond the selected directory.

Mitigation: Scan only authorized directories and check symbolic links before scanning.

Risk: Installing an update overwrites existing files for this skill.

Mitigation: Use a reviewed, fixed package version and select the intended installation directory.

Risk: Scans save audit metadata locally, and generated guardrails may need adaptation.

Mitigation: Review the local audit records and inspect guardrails before adopting them; keep isolation enabled for sensitive-data checks.

## Reference(s):

- [Detection items](artifact/references/detection-items.md)
- [Guardrails template](artifact/references/guardrails-template.md)
- [Report template](artifact/references/report-template.md)
- [Tutorial](artifact/references/tutorial.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Configuration]

**Output Format:** [Text, JSON, or Markdown hardening reports and Markdown defense guardrails]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports describe detected patterns without reproducing injection text; each scan also records local audit metadata.]

## Skill Version(s):

0.2.9 (source: release evidence, SKILL.md frontmatter, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
