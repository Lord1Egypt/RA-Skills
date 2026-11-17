## Description:

Cache and reuse code from prior AI agent executions via Raysurfer by searching before coding and uploading successful results afterward.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryx2](https://clawhub.ai/user/ryx2)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill to search Raysurfer for reusable code before implementing a task, report whether cached code worked, and upload successful generated code for future reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task descriptions, cache-use metadata, and selected source files may be sent to Raysurfer.

Mitigation: Use only with data approved for third-party processing, and avoid uploading secrets, proprietary source, or private production code unless policy permits it.

Risk: Cached code returned by the service may be unsuitable or unsafe to run without review.

Mitigation: Manually inspect cached code and test it in an isolated environment before using it in a project.

## Reference(s):

- [Raysurfer API Reference](references/api-reference.md)
- [Raysurfer API Keys Dashboard](https://raysurfer.com/dashboard/api-keys)
- [ClawHub Skill Page](https://clawhub.ai/ryx2/skills/raysurfer)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RAYSURFER_API_KEY; may send task descriptions, cache-use metadata, and selected source files to Raysurfer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
