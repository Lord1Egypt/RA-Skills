## Description:

Run document processing workflows using Upstage Document Agent API (v2) for Studio-configured agents and API-defined agents/configs, including file upload, workflow setup, job execution, and result polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upstage-deployment](https://clawhub.ai/user/upstage-deployment)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-automation teams use this skill to run Upstage Studio and Document Agent workflows for document parsing, classification, extraction, and follow-on analysis. It helps agents create or select workflows, submit documents, poll jobs, and save JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents may be uploaded to Upstage's cloud API.

Mitigation: Use the skill only for documents allowed under the user's Upstage account, retention settings, and data-handling obligations.

Risk: Agent, config, file, job, publishing, and delete actions can alter remote Upstage resources.

Mitigation: Confirm exact resource IDs and intended visibility before create, publish, update, delete, like, or unlike operations.

Risk: Document outputs may contain sensitive extracted text or structured data.

Mitigation: Prefer a private output directory with restricted permissions and avoid predictable temporary paths for confidential results.

## Reference(s):

- [Upstage Studio](https://console.upstage.ai/studio)
- [Agents & Configs API](references/agents-and-configs.md)
- [Files API](references/files.md)
- [Responses & Jobs API](references/jobs.md)
- [Step Types and Data Parameters](references/step-types.md)
- [Preset Agents](references/preset-agents.md)
- [End-to-End Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, json]

**Output Format:** [Markdown guidance with Python or shell examples and JSON job/result artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write full job results and per-step result JSON files to a resolved output path.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
