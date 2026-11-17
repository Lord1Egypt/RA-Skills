## Description:

Tester Workflow guides a complete software testing workflow from requirements analysis through test case generation and review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garkinchu](https://clawhub.ai/user/garkinchu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and testing teams use this skill to run a structured testing workflow over requirements and design materials, producing analysis reports, design questions, test cases, and review feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may push users toward a full testing process even when they ask for quick examples or partial review.

Mitigation: Confirm the requested scope and timebox before running the full workflow, and use the bundled sub-skills independently for narrower tasks.

Risk: Test case generation can require local CSV file output.

Mitigation: Confirm the output path and overwrite behavior before writing or replacing any file.

Risk: The workflow may require complete requirements, design documents, and 30-50 test cases, which can be more extensive than a lightweight review.

Mitigation: Set expectations about required source documents and expected artifact size before starting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/garkinchu/skills/tester-workflow)
- [README](README.md)
- [Workflow guide](reference/workflow-guide.md)
- [Full workflow example](examples/full-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown reports and CSV test case files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local UTF-8 BOM CSV files with || delimiters during test case generation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
