## Description:

Evaluates semantic consistency between AI-generated clinical notes and expert gold standards using BERTScore and COMET.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, clinical AI evaluators, and academic writing reviewers use this skill to compare AI-generated clinical text with expert references and produce scored JSON summaries or detailed case-level findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical text may be processed and included in detailed JSON output or console logs.

Mitigation: Use de-identified or compliance-approved inputs, write outputs only to controlled paths, and avoid shared logs for raw clinical notes.

Risk: Dependency and model downloads may affect integrity, reproducibility, and runtime behavior.

Mitigation: Pin and verify Python dependencies and model artifacts before use in a controlled environment.

Risk: Running the skill in a privileged or shared environment could expose clinical text or generated results.

Mitigation: Install and execute the skill in an isolated, non-privileged environment with appropriate access controls.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/semantic-consistency-auditor)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with command snippets and JSON result files or console JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write detailed or summary JSON to an output path; first execution may require model downloads.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and artifact changelog, released 2026-02-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
