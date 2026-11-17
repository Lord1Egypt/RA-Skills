## Description:

Mine unstructured clinical text from MIMIC-IV to extract diagnostic logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and clinical data analysts use this skill to mine MIMIC-IV or similar clinical notes for entities, relationships, timelines, and diagnostic or treatment reasoning. It helps convert clinical note text into structured insights for review, downstream analysis, FHIR-style documents, knowledge graph triples, or temporal event sequences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes clinical notes and generated JSON that may contain sensitive health information.

Mitigation: Run it only in an approved clinical-data environment, restrict access to inputs and outputs, and avoid including raw text unless explicitly required.

Risk: The skill writes output files, and server security guidance flags insufficient privacy and filesystem safeguards.

Mitigation: Validate output paths before execution, reject absolute or traversal paths, and write only to approved workspace locations.

Risk: The skill depends on medical NLP packages that may change over time.

Mitigation: Pin and audit dependencies before production or regulated use.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [MIMIC-IV Clinical Database](https://physionet.org/content/mimiciv/)
- [scispaCy](https://allenai.github.io/scispacy/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON files and plain-text summary reports, with Python API and CLI command examples in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include entity spans, negation flags, relation triples, timeline events, clinical logic summaries, and patient-level aggregates depending on the selected extraction mode.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
