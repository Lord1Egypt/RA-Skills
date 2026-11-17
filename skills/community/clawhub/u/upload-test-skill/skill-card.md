## Description:

upload-test-skill helps agents verify that a skill upload, trigger, safety check, and fixed Markdown test-report output path work using de-identified test text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li19921117](https://clawhub.ai/user/li19921117)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill during ClawHub, QClaw, OpenClaw, or Codex integration checks to confirm that metadata is recognized, trigger routing works, and the agent can return a stable upload test report without processing real business data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may include real PII or sensitive business data while testing upload or trigger behavior.

Mitigation: Use only synthetic or de-identified test input; when suspected PII appears, provide a risk warning and avoid repeating sensitive fields.

Risk: Users may mistake a successful local trigger test for platform review or deployment approval.

Mitigation: State that the skill verifies current-agent triggering and fixed output behavior only, not ClawHub review outcomes.

Risk: Requests to call external interfaces are outside the skill's stated boundary.

Mitigation: Do not call external systems; respond that the skill only supports local upload and trigger testing.

## Reference(s):

- [Server-resolved source repository](https://github.com/li19921117/upload-test-skill)
- [ClawHub skill page](https://clawhub.ai/li19921117/skills/upload-test-skill)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown test report with a status table, input summary, risk note, and next-step suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not call external systems; avoids repeating suspected sensitive fields.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
