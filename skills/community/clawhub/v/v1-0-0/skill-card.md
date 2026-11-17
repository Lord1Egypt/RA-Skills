## Description:

Deeptechnic guides investment due-diligence agents through independent technical validation, team assessment, supply-chain audit, competitor discovery, and structured hard-tech risk reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ackiles](https://clawhub.ai/user/ackiles)

### License/Terms of Use:

MIT-0

## Use Case:

Investment analysts, technical reviewers, and due-diligence teams use this skill to evaluate hard-tech startup claims, identify engineering, team, supply-chain, and competitive risks, and produce structured pre-investment technical reports. It is not a substitute for financial due diligence, legal due diligence, or final investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to retain user feedback and project metadata as local training data.

Mitigation: Use only with explicit approval for non-confidential or redacted projects, and disable or remove feedback-data writes for sensitive due-diligence work.

Risk: The bundled SkillOpt runner can persist API credentials in plaintext and depends on endpoint configuration.

Mitigation: Do not run the script with real API keys until credential persistence and endpoint-validation issues are fixed; use reviewed endpoints and environment-scoped secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ackiles/skills/v1-0-0)
- [Skills index](artifact/references/skills-index.md)
- [Deep-tech due diligence analysis](artifact/references/skills/deep-tech-dd-analysis.md)
- [Team assessment](artifact/references/skills/team-assessment.md)
- [Supply-chain audit](artifact/references/skills/supply-chain-audit.md)
- [Competitor discovery](artifact/references/skills/competitor-discovery.md)
- [Quality gate](artifact/references/skills/quality-gate.md)
- [Feedback collection](artifact/references/skills/feedback-collection.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Structured Markdown reports and optional DOCX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scoring tables, prioritized questions, cited findings, next-round recommendations, and optional local training-data records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
