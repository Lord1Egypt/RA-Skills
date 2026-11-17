## Description:

Score the novelty of biological targets through literature mining and trend analysis.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[lyla0921](https://clawhub.ai/user/lyla0921)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bioinformatics users can run the skill as a Python CLI to produce synthetic target novelty scores and text, JSON, or CSV reports for exploratory evaluation of a scoring workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scores and reports may be synthetic demonstration output rather than real PubMed or PMC evidence.

Mitigation: Treat generated reports as illustrative only and verify findings against authoritative biomedical literature before research decisions.

Risk: Report writing accepts user-provided output paths.

Mitigation: Use reviewed relative output paths inside the workspace and avoid arbitrary or absolute paths.

Risk: CSV exports from untrusted target inputs may be unsafe to open in spreadsheet software.

Mitigation: Inspect or sanitize CSV output before opening it in spreadsheet software.

Risk: The dependency set should be reviewed before use in a research environment.

Mitigation: Use a fixed, reviewed dependency set in a controlled environment before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyla0921/skills/target-novelty-scorer)
- [NCBI E-utilities API endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)

## Skill Output:

**Output Type(s):** [text, JSON, CSV]

**Output Format:** [Text, JSON, or CSV report from a CLI command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes target-level novelty score, confidence, score breakdown, metadata, and interpretation; output may be printed to stdout or written to a user-provided file path.]

## Skill Version(s):

0.1.0 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
