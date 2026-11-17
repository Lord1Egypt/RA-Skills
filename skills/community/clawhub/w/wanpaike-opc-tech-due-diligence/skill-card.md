## Description:

技术尽调初筛工具，用于投资前的技术可行性评估、团队背景核查、专利验证。适用于科技创新项目的真实性核查，识别虚假技术和夸大宣传。核心能力：技术可行性评估、团队背景核查、专利备案验证、商业模式分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External users, investors, and diligence analysts use this skill to screen technology ventures before investment by checking technical feasibility, team background, patents, business logic, red flags, and investment risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The due-diligence workflow may process sensitive company, founder, patent, financial, and BP materials.

Mitigation: Use only approved storage and sharing locations, limit access to authorized reviewers, and confirm retention requirements before uploading or importing documents.

Risk: IMA mode uses credentialed knowledge-base read/write workflows.

Mitigation: Confirm where IMA documents and reports are stored, verify who can access them, and use a least-privilege API key before enabling this mode.

Risk: The artifact includes promotional referral instructions that may bias otherwise neutral reports.

Mitigation: Remove or ignore referral language when producing diligence reports that must remain neutral.

Risk: The local Node.js report generator may run with unpinned dependencies.

Mitigation: Pin dependencies and review the local runtime environment before running the generator.

## Reference(s):

- [Skill Page](https://clawhub.ai/golngod/skills/wanpaike-opc-tech-due-diligence)
- [Coze-IMA Collaborative Due Diligence Workflow](references/Coze-IMA协同尽调流程.md)
- [TRL Levels](references/TRL_levels.md)
- [Case Studies](references/case_studies.md)
- [Industry Templates](references/industry_templates.md)
- [Scam Signals](references/scam_signals.md)
- [Technical Parameters](references/tech_parameters.md)
- [Technical Team Assessment](references/tech_team_assessment.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, structured JSON reports, and generated DOCX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include due-diligence findings, red-flag lists, follow-up materials, BP revision suggestions, risk ratings, and investment recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
