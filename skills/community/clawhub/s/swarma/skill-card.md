## Description:

Agent teams that run growth experiments and build their own playbook through the GROWS loop: generate hypothesis, run experiment, observe signal, weigh verdict, and stack playbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glitch-rabin](https://clawhub.ai/user/glitch-rabin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and growth teams use this skill to set up and run swarma experiment loops for hooks, landing pages, outreach, pricing, activation, retention, and other AARRR funnel work. The skill guides agents through installation, team generation, cycle execution, metric logging, MCP integration, and playbook review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run an external CLI.

Mitigation: Review before installing, use a virtual environment, and pin or verify the swarma package or repository version.

Risk: The skill requires an OpenRouter API key and includes examples that store secrets in local configuration.

Mitigation: Store the key with owner-only permissions or a secret manager, and avoid committing it to shared files.

Risk: Experiment prompts and outputs may be sent to an external LLM provider during agent cycles.

Mitigation: Do not put real secrets, customer data, or confidential business data into prompts or generated experiments.

Risk: Generated strategies, metrics, and playbooks can become persistent local business data.

Mitigation: Treat generated artifacts as sensitive business records and apply appropriate access controls and retention practices.

## Reference(s):

- [swarma repository](https://github.com/glitch-rabin/swarma)
- [swarma website](https://swarma.dev)
- [OpenRouter API keys](https://openrouter.ai/keys)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown, Code]

**Output Format:** [Markdown with inline bash, JSON, and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands and configuration that create local swarma teams, run experiment cycles, log metrics, and update local strategy/playbook files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
