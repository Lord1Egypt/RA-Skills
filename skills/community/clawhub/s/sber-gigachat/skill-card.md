## Description:

Integrate GigaChat (Sber AI) with OpenClaw via gpt2giga proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smvlx](https://clawhub.ai/user/smvlx)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run a local OpenAI-compatible proxy that lets OpenClaw agents call Sber GigaChat models with credentials supplied through environment variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The proxy uses sensitive GigaChat credentials from a local environment file.

Mitigation: Protect the environment file with restrictive permissions and avoid exposing credentials in logs, shell history, or shared workspaces.

Risk: TLS certificate verification can be disabled when the Sber CA is not installed.

Mitigation: Install and verify the Sber root CA before use, and require certificate verification for production or sensitive workflows.

Risk: The startup script can terminate any process already using local port 8443.

Mitigation: Check port 8443 before startup and change the port or stop only the intended process.

Risk: The setup flow installs the gpt2giga dependency from a package registry.

Mitigation: Pin and verify the dependency version before installation.

Risk: The configuration patch modifies the OpenClaw configuration file.

Mitigation: Review the generated backup and patch before continuing with agent use.

## Reference(s):

- [GigaChat documentation](https://developers.sber.ru/docs/ru/gigachat/overview)
- [gpt2giga package](https://pypi.org/project/gpt2giga/)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw Russian skills repository](https://github.com/smvlx/openclaw-ru-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, proxy lifecycle, status, stop, and OpenClaw configuration guidance for a local GigaChat proxy.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
