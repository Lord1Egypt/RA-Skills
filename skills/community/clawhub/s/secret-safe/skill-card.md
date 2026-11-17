## Description:

Secure API key and secrets management guidance for agent skills, covering environment injection, secrets managers, setup flows, and credential leak audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brycexbt](https://clawhub.ai/user/brycexbt)

### License/Terms of Use:


## Use Case:

Developers and skill reviewers use this skill to design, audit, and document agent skills that handle API keys, tokens, passwords, or other credentials without exposing secrets in prompts, logs, outputs, or generated files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example credential-handling commands may be copied into environments where host-level process, shell history, or tool logging protections differ from the documented pattern.

Mitigation: Treat examples as guidance for avoiding LLM and artifact exposure; prefer official CLIs or client libraries that read credentials directly from environment variables and use narrowly scoped, short-lived keys.

Risk: Incorrectly adapting the guidance could still place secrets in prompts, logs, generated files, or user-visible error messages.

Mitigation: Use environment injection gates, subprocess-level secrets manager access, and the bundled audit checklist before enabling or publishing a skill.

## Reference(s):

- [Env Injection Examples](references/env-injection-examples.md)
- [Skill Security Audit Checklist](references/audit-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline YAML, JSON, shell, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid including secret values and should frame command snippets as credential-handling patterns.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
