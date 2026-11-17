## Description:

分析管理体系文件的逻辑完整性与合规性，识别差异点和风险，提供结构化改进建议；适用于内审、供应商评估、认证准备及流程改善场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external auditors, quality teams, and supplier-management teams use this skill to review management-system documents, compare them against supported ISO and IATF standards, identify gaps and risks, and prepare structured improvement guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided management-system documents may contain sensitive organizational, compliance, supplier, or certification-preparation information.

Mitigation: Treat input documents and generated audit reports as sensitive, keep outputs in an appropriate local or controlled workspace, and review sharing permissions before distribution.

Risk: Generated Markdown reports can include content derived from untrusted input, including misleading links, headings, or images.

Mitigation: Review generated reports before relying on or sharing them, especially when source documents were supplied by third parties.

Risk: Compliance findings and risk ratings are decision-support outputs and may be incomplete or incorrect for a specific certification context.

Mitigation: Have qualified quality, environmental, occupational-safety, or automotive-system reviewers confirm findings against the applicable standard and organization-specific requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-management-system-audit)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-management-system-audit)
- [ISO 9001:2015 reference](references/iso-9001-2015.md)
- [ISO 14001:2015 reference](references/iso-14001-2015.md)
- [ISO 45001:2018 reference](references/iso-45001-2018.md)
- [IATF 16949:2016 reference](references/iatf-16949-2016.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown audit reports with structured findings, risk ratings, compliance tables, and improvement recommendations; the report script also emits JSON status metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a timestamped local Markdown report when the bundled report-generation script is used.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
