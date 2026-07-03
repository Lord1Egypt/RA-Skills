## Description: <br>
Deeptechnic guides investment due diligence agents through independent hard-tech technical validation, team assessment, supply-chain audit, competitor discovery, and structured report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ackiles](https://clawhub.ai/user/ackiles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investment due diligence teams and agent developers use this skill to structure technical diligence on hard-tech startups, including claim validation, team review, supplier analysis, competitor discovery, quality checks, and report generation. It is not a substitute for financial due diligence, legal due diligence, or final investment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill normalizes capturing user feedback and diligence content into training datasets. <br>
Mitigation: Use only with approved non-confidential materials, or remove and disable feedback-to-training steps before using the skill with confidential startup information. <br>
Risk: The bundled SkillOpt script can use external model credentials and make external model calls. <br>
Mitigation: Review scripts/run_skillopt.py before execution, control API keys through managed environment variables, and avoid running the script in untrusted projects. <br>
Risk: The skill produces technical due diligence support, not final investment, legal, or financial decisions. <br>
Mitigation: Treat reports as technical input and route final investment, legal, and financial judgments to qualified reviewers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ackiles/v1-0-0) <br>
- [Skills Index](references/skills-index.md) <br>
- [Deep-Tech Due Diligence Analysis](references/skills/deep-tech-dd-analysis.md) <br>
- [Team Assessment](references/skills/team-assessment.md) <br>
- [Supply Chain Audit](references/skills/supply-chain-audit.md) <br>
- [Competitor Discovery](references/skills/competitor-discovery.md) <br>
- [Quality Gate](references/skills/quality-gate.md) <br>
- [Feedback Collection](references/skills/feedback-collection.md) <br>
- [Report Generation](references/skills/report-generation.md) <br>
- [SkillOpt training script](scripts/run_skillopt.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with report outlines, scoring tables, checklists, optional shell commands, and optional DOCX report generation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured due diligence reports named Deeptechnic_<ProjectEngName>_<Phase>_<Date>.docx when the report-generation workflow is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
