## Description:

GitHub Spec-Kit integration for Spec-Driven Development workflows, including project initialization, constitution management, feature specifications, implementation planning, task breakdowns, implementation support, clarification, analysis, extension and preset management, and Paperclip issue reassignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-code-hash](https://clawhub.ai/user/james-code-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to run a Spec-Driven Development workflow from constitution and specification through plans, tasks, implementation, review checks, and related Paperclip issue handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide state-changing Paperclip issue operations.

Mitigation: Treat reassignment and comment commands as explicit user-approved actions before execution.

Risk: The bundled Paperclip fallback script can send PAPERCLIP_API_KEY to the configured PAPERCLIP_API_URL.

Mitigation: Run the script with PAPERCLIP_API_KEY only after verifying that PAPERCLIP_API_URL is the intended HTTPS or loopback development endpoint.

Risk: Spec-Kit workflows can create or modify project files.

Mitigation: Install and use the skill only when the publisher is trusted and the agent is expected to perform Spec-Kit file-generation or file-editing workflows.

## Reference(s):

- [Spec-Kit official repository](https://github.com/github/spec-kit)
- [GitHub Spec-Driven Development blog post](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)
- [Addy Osmani's spec writing guide](https://addyosmani.com/blog/good-spec/)
- [Constitution Management Guide](references/constitution-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, CLI references, and generated project artifact descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Spec-Kit project files and may issue Paperclip reassignment or comment commands when explicitly invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
