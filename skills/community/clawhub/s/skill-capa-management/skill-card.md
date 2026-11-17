## Description:

This Chinese-language CAPA skill guides users through maturity-tailored corrective and preventive action reporting for audit response and practical execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality managers, auditors, and operations teams use this skill to collect issue facts, assess organization maturity, and draft CAPA reports that separate immediate correction from longer-term corrective action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised helper files such as scripts/build_report.py and references/capa_knowledge.md were not present in the inspected artifact, so automated report generation or knowledge-base behavior may fail unless those files are supplied elsewhere.

Mitigation: Deploy with the missing helper files supplied, or use the skill as an interactive drafting guide and test the advertised report-generation path before relying on it.

Risk: CAPA reports may be used for audit or corrective-action decisions and can be misleading if issue facts, evidence, or root-cause details are incomplete.

Mitigation: Have a responsible quality owner review the final report, confirm supporting evidence, and preserve uncertain items as pending business input before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-capa-management)
- [Server-resolved source repository](https://github.com/duding-engicool/skill-capa-management)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text, Shell commands]

**Output Format:** [Chinese-language Markdown and plain-text CAPA report content, with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The inspected artifact advertises Markdown and txt report outputs; referenced report-generation helper files were not present in the inspected package.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
