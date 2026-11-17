## Description:

Generates, previews, validates, and diagnoses Volcengine TOS tosutil commands for bucket, object, transfer, metadata, and connectivity workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and storage operators use this skill to plan and preview tosutil configuration, bucket/object operations, uploads, downloads, deletes, metadata updates, capacity checks, and troubleshooting steps for Volcengine TOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials can be exposed when AK, SK, or token values are passed as command-line arguments.

Mitigation: Prefer restricted configuration profiles or temporary credentials, use a verified version-pinned tosutil binary, and review redacted command previews before execution.

Risk: Destructive delete workflows can bypass interactive confirmation when force or yes-style options are used.

Mitigation: List the exact target first, keep default preview and confirmation behavior, and use force or yes options only after backups, retention, or recovery controls are in place.

## Reference(s):

- [tosutil documentation survey](artifact/references/doc-survey.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command previews redact AK, SK, and token values; execution results include status, summaries, diagnostics, and suggested next actions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
