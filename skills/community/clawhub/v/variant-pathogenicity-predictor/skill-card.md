## Description:

Integrates REVEL, CADD, and PolyPhen scores to produce a simplified variant pathogenicity classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ec-cyber258](https://clawhub.ai/user/ec-cyber258)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bioinformatics practitioners use this skill to run a local helper that combines variant scores and reports a simplified classification with score breakdown. Outputs require independent validated interpretation before clinical, reporting, or research-triage use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simplified genetic variant scoring may be mistaken for clinically validated pathogenicity or ACMG interpretation.

Mitigation: Do not use classifications for diagnosis, patient care, reporting, or authoritative triage without independent validated interpretation by qualified reviewers.

Risk: Local script execution can read input files and may save output reports in the workspace.

Mitigation: Run in a controlled workspace, review file paths before execution, and avoid processing sensitive patient data unless approved safeguards are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ec-cyber258/skills/variant-pathogenicity-predictor)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Plain text console output and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports composite score, pathogenicity classification, and individual score values; no external API calls are indicated by the evidence.]

## Skill Version(s):

0.1.0 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
