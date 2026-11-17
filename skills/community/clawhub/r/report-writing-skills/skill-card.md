## Description:

Automates collecting, filtering, and synthesizing recent research reports into customized analysis reports with progress feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meidetong](https://clawhub.ai/user/meidetong)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and report-writing agents use this skill to gather recent research-report metadata from a target site, request user preferences for the final report, and draft a customized market analysis summary. Outputs should be reviewed before use because the security evidence flags simulated research actions and an unsafe external import path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may present simulated research actions as completed work.

Mitigation: Require explicit labeling when output is based on placeholders or metadata only, and verify downloaded source reports before relying on the analysis.

Risk: An unsafe external import path can cause the agent to load code outside the packaged artifact.

Mitigation: Remove hard-coded external import paths and execute only reviewed, packaged skill code.

Risk: Research-site credentials and downloaded report contents may be sensitive.

Mitigation: Use credentials only for the active session, avoid storing secrets, and let the user confirm output paths and retention.

Risk: Generated financial or market analysis can be inaccurate or unsupported.

Mitigation: Independently verify source documents, dates, and market data before making business or investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meidetong/skills/report-writing-skills)
- [Workflow guide](artifact/references/workflow_guide.md)
- [sgpjbg.com](https://www.sgpjbg.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown report files, console progress text, and metadata notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write report and metadata files to a user-selected local directory; generated financial analysis requires review.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
