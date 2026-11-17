## Description:

Connect OpenClaw to the SenseCraft public model library to search, inspect, export, and download AI vision models for software and edge AI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jancee](https://clawhub.ai/user/jancee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover SenseCraft vision models, inspect model metadata and download URLs, export searchable indexes, download model artifacts, and validate selected TFLite models for OpenClaw or edge AI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local demo can install Python packages, download model files, open a webcam, and save local files.

Mitigation: Review commands before running them, use a dedicated directory or virtual environment, and grant camera access only when live inference is intended.

Risk: Downloaded model artifacts and generated indexes may be untrusted or may not match expected runtime assumptions.

Mitigation: Verify downloaded models before use, inspect input/output tensors and metadata, and validate behavior on positive, near-miss, and negative examples before integration.

Risk: CSV exports can contain untrusted model metadata from the public API.

Mitigation: Sanitize CSV files before opening them in spreadsheet software.

Risk: The SenseCraft public API contract and model availability may change.

Mitigation: Use small retries and throttling during bulk operations, preserve raw metadata in exports, and record per-model failures instead of assuming every lookup or download will succeed.

## Reference(s):

- [SenseCraft API Notes](references/sensecraft-api.md)
- [Field Mapping Notes](references/field-mapping-notes.md)
- [Integration Notes](references/integration-notes.md)
- [Local Webcam Demo Notes](references/local-webcam-demo.md)
- [Model Catalog](references/model-catalog.md)
- [SenseCraft Public Model API](https://sensecraft.seeed.cc/aiserverapi)
- [SSCMA-Micro](https://github.com/Seeed-Studio/SSCMA-Micro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown with inline shell commands plus JSON, CSV, manifest, model download, and annotated image file outputs when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local model indexes, download manifests, model artifacts, virtual environments, and webcam captures under user-selected or skill-local directories.]

## Skill Version(s):

1.1.2 (source: server release metadata, released 2026-03-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
