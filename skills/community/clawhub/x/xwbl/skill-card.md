## Description:

Builds and operates an inquiry transcript generator for outlines, transcript analysis, personnel extraction, templated transcript generation, and web-tool replication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldh119](https://clawhub.ai/user/ldh119)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Chinese inquiry or interview transcript outlines, identify relevant people from source records, draft fact-anchored Q&A transcripts, and optionally produce editable documents or simple web tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive case, inquiry, or interview materials.

Mitigation: Keep source documents in trusted workspaces and avoid sending sensitive records to unrelated services.

Risk: Generated transcripts may contain factual, procedural, or legal errors if source materials are incomplete or conflicting.

Mitigation: Review every generated transcript against the original materials before use.

Risk: The workflow could be misused to fabricate statements, facts, or evidence.

Mitigation: Use only facts present in user-provided materials, mark missing information as unavailable, and reject requests to invent facts.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown, plain text, HTML, Word documents, or code depending on the user request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should remain anchored to user-provided materials and include human review reminders where appropriate.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
