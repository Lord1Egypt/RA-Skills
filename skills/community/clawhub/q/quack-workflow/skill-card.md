## Description:

Execute multi-step workflows via Orchestrate for complex workflows, parallel tasks, multi-model orchestration, and multi-step process automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpaulgrayson](https://clawhub.ai/user/jpaulgrayson)

### License/Terms of Use:


## Use Case:

Developers and automation builders use this skill to run workflow YAML through Orchestrate for chained, parallel, and multi-model tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled workflow template can publish LLM-generated web-search content to Twitter without a human approval step.

Mitigation: Change public posting steps to draft mode or require explicit human approval before publication.

Risk: Workflow files are sent to Orchestrate for execution.

Mitigation: Review workflow YAML before execution and avoid sending sensitive data unless Orchestrate use is approved.

Risk: Broad automatic invocation could run workflows or social-media actions unexpectedly.

Mitigation: Use narrow invocation rules and verify social-media permissions are scoped and revocable.

## Reference(s):

- [Orchestrate platform](https://orchestrate.us.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML workflow examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs workflow YAML through an external Orchestrate endpoint and returns execution output as text or JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
