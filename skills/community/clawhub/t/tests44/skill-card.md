## Description:

Guides agents through creating a CI/CD update pipeline on the Frontline platform for already deployed workloads, covering code cloning, dependency build steps, image build, and rollout deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyzauh](https://clawhub.ai/user/wyzauh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform operators use this skill to collect confirmed tenant, project, repository, build, registry, and deployment details, then create a Jenkins-based update pipeline for an existing workload. It is not intended for first-time workload creation or infrastructure initialization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Jenkins jobs may receive high-impact host Docker access through the required Jenkins template.

Mitigation: Review the template before installation and prefer a revised version that removes the host Docker socket mount or uses an isolated image builder.

Risk: Credential handling is ambiguous and could lead to raw passwords being placed in generated pipeline content.

Mitigation: Use credential IDs or platform-managed secrets only, and verify that tokens or passwords are not written to Jenkinsfiles, repositories, or user-visible responses.

Risk: Unvalidated Jenkinsfile inputs could create incorrect or unsafe pipeline behavior.

Mitigation: Validate and safely render all placeholders, and require explicit user confirmation for tenant, project, repository, build, registry, and deployment selections before creating the pipeline.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Jenkinsfile/Groovy code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires step-by-step user confirmation before generating or creating the pipeline.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
