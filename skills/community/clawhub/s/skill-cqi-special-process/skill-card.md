## Description:

Assists process engineers, quality engineers, and auditors with evidence-based CQI-9, CQI-11, CQI-12, and CQI-15 special process assessments, producing closed-loop assessment materials from standard selection through re-evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Process engineers, quality engineers, and auditors use this skill to guide CQI special process evaluations for heat treating, plating, coating, and welding. It helps collect real process evidence, support scoring, identify gaps, draft corrective action plans, and prepare re-evaluation materials for audit and process improvement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run scripts/build_report.py, but that script is not included in the artifact.

Mitigation: Review any report-generation script before execution and confirm the exact file path before allowing the agent to run it.

Risk: The workflow and output filenames are Chinese-language CQI audit materials that may not match every organization's audit process.

Mitigation: Confirm the report language, filenames, and CQI assessment workflow against the applicable audit process before use.

## Reference(s):

- [Server-resolved source repository](https://github.com/duding-engicool/skill-cqi-special-process)
- [ClawHub skill listing](https://clawhub.ai/duding-engicool/skills/skill-cqi-special-process)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown and plain text CQI assessment reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report filenames vary by CQI standard and assessment date.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
