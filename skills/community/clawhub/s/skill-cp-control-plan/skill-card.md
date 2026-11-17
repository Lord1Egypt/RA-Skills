## Description:

Chinese-language skill for creating and improving CP (Control Plan) documents, analyzing CSV or Excel quality data, flagging FMEA and SPC risks, generating charts, and guiding version management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers and manufacturing teams use this skill to draft or review CP control plans, analyze process capability from local quality data, identify quality risks, and prepare reports or charts for follow-up review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts read user-selected CSV, Excel, or JSON files and create or overwrite selected local output files or directories.

Mitigation: Review input and output paths before running scripts, and direct outputs to an intended workspace location.

Risk: Generated quality analyses, warnings, and charts may be used in operational control-plan decisions.

Mitigation: Have a qualified quality engineer review generated reports, thresholds, and recommendations before using them in controlled manufacturing processes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/duding-engicool/skills/skill-cp-control-plan)
- [Source repository (server-resolved provenance)](https://github.com/duding-engicool/skill-cp-control-plan)
- [CP template guide](references/cp_template_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Chinese markdown guidance with inline bash commands; local JSON reports and PNG chart files when scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+ and pandas, openpyxl, numpy, and matplotlib for script execution.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
