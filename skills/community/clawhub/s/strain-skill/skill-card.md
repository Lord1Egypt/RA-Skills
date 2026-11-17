## Description:

Automates strain identification workflows by parsing SEQ or FASTA files, submitting sequences to NCBI BLAST, preparing DingTalk table data, and generating a Word identification report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meta-men](https://clawhub.ai/user/meta-men)

### License/Terms of Use:

MIT-0

## Use Case:

Laboratory users and developers can use this skill to automate sequence-file parsing, BLAST submission, DingTalk-ready result formatting, and Word report generation for strain identification workflows. Security evidence states the current implementation should not be relied on for real strain identification without remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Strain-identification results may be misleading because security evidence says the output appears hard-coded rather than based on completed BLAST result parsing.

Mitigation: Do not use the skill for real strain identification until BLAST result polling, parsing, and validation are implemented and reviewed.

Risk: Sequence data is uploaded to NCBI.

Mitigation: Require explicit user consent before submitting sequence data to NCBI and confirm the data may be shared with that external service.

Risk: Local input paths, file sizes, and report output paths are not clearly constrained.

Mitigation: Add input path validation, file-size limits, and user-controlled report output handling before deployment.

Risk: Dependencies are version-ranged rather than pinned to reviewed package versions.

Mitigation: Pin and review dependencies before installation in managed or production environments.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/meta-men/skills/strain-skill)
- [NCBI BLAST service used by the artifact](https://blast.ncbi.nlm.nih.gov/Blast.cgi)

## Skill Output:

**Output Type(s):** [text, files]

**Output Format:** [JSON-style status object with DingTalk table data and a generated .docx report path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a Word report file using the provided template path.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
