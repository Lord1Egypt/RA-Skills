## Description:

SEVO is an AI-agent software delivery pipeline that guides work from requirements and gated reviews through implementation, audit, regression, release, verification, and delivery ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuchangxu1989-openclaw](https://clawhub.ai/user/yuchangxu1989-openclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent teams use SEVO to coordinate AI coding work through a structured delivery lifecycle with specification, review gates, implementation, audit, regression, release, verification, and ledgered evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package has broad automation authority over OpenClaw configuration, agent prompts, pipeline state, work routing, probes, and release-related actions.

Mitigation: Review before installing, test in a disposable workspace first, pin the package and version, and prepare rollback or disable steps before use in an important environment.

Risk: The security evidence flags unsafe or unverifiable installation behavior around documented npm/npx usage.

Mitigation: Do not run the documented install commands in an important environment until the package name, version, and postinstall behavior are clarified and auditable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuchangxu1989-openclaw/skills/sevo)
- [SEVO homepage](https://agentos.site/sevo.html)
- [README](README.md)
- [Architecture overview](docs/architecture.md)
- [Product requirements](docs/product-requirements.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, code-oriented task outputs, and JSON configuration or pipeline-state artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local pipeline state and OpenClaw plugin configuration when the documented commands are run.]

## Skill Version(s):

1.13.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
