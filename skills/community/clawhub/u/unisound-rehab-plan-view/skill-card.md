## Description:

Patient-facing postoperative rehabilitation plan viewer that organizes an existing care plan by phase, goal, tasks, and precautions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External patient-facing agents use this skill to present an existing postoperative rehabilitation plan in a clearer form, including the current phase, phase goal, task summary, and precautions. It is not intended to create new rehabilitation prescriptions or replace clinician guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive rehabilitation data may be sent to a remote medical model.

Mitigation: Use only with explicit authorization, follow applicable privacy review, and avoid real patient identifiers where possible.

Risk: Production API keys can be exposed if passed directly on the command line.

Mitigation: Use platform secret handling or scoped runtime credentials instead of command-line secrets.

Risk: Untrusted PDFs, Office files, or images may increase parsing and sandbox escape risk.

Mitigation: Process only trusted files or run document conversion and OCR in a sandboxed runtime.

Risk: The external _shared/doc-preprocess fallback can execute Python code outside the reviewed package.

Mitigation: Remove the fallback or enforce integrity checks before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-rehab-plan-view)
- [CareKit care plan framework](https://github.com/carekit-apple/CareKit)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [UTF-8 JSON containing structured plan data and patient-facing Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes plan identifiers, current phase, phase goal, task summary, precautions, status, and generated explanatory text.]

## Skill Version(s):

1.0.2 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
