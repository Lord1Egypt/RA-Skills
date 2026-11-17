## Description:

Super Deep Coding coordinates orchestrator, builder, and reviewer agents to decompose complex software projects, implement modules, review results, and run end-to-end checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[molexazwo](https://clawhub.ai/user/molexazwo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate large, multi-file software builds through requirements capture, module decomposition, independent implementation, review, logging, and end-to-end validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local dashboard can expose project files and agent logs within the workspace.

Mitigation: Use a dedicated workspace without secrets or unrelated source, keep the dashboard bound to localhost, and stop it when work is complete.

Risk: Builder and reviewer workflows may execute generated or project code during implementation and end-to-end testing.

Mitigation: Run the skill only where executing generated code is acceptable, and use containers or virtual machines for untrusted projects.

Risk: Frontend or npx-based test dependencies may change between runs.

Mitigation: Pin or vendor frontend and npx dependencies before using the workflow on sensitive or production-adjacent projects.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/molexazwo/skills/super-deep-coding)
- [Deep Coding Harness Architecture](references/architecture.md)
- [Orchestrator Rules](references/orchestrator-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON snippets, shell commands, generated project files, logs, and review records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project workspace files, project-state JSON, agent logs, and test artifacts when used by an enabled coding environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
