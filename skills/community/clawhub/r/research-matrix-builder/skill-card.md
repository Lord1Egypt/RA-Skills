## Description:

Build literature matrices from papers, notes, and abstracts to compare methods, data, findings, and research gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and writing agents use this skill to turn paper lists, notes, abstracts, and a research question into a structured literature matrix, thematic clusters, gap summary, and review outline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CSV cells may be interpreted as formulas by spreadsheet tools.

Mitigation: Review or sanitize cells beginning with =, +, -, or @ before opening CSV output in spreadsheet software.

Risk: The skill structures user-provided literature notes and may preserve incomplete or uncertain fields.

Mitigation: Keep missing fields explicit, cite source material where possible, and review the matrix before using it in external-facing research outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/research-matrix-builder)
- [README](artifact/README.md)
- [Matrix Schema](artifact/resources/matrix_schema.csv)
- [Build Matrix Helper](artifact/scripts/build_matrix.py)
- [Smoke Test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, CSV, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional CSV files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an explicit matrix schema with citation, problem, method, data, metric, key_result, limitation, and gap fields.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
