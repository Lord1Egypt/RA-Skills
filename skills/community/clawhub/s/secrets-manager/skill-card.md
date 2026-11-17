## Description:

Encrypted local secret store for OpenClaw agents that stores, retrieves, lists, rotates, audits, and deletes secrets using AES-256-GCM authenticated encryption with a local master key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep local agent secrets encrypted at rest, retrieve masked values by default, rotate stored secrets, and audit rotation or exposure issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext secrets can be exposed through command arguments, raw stdout, temp files, CI logs, or agent transcripts.

Mitigation: Use masked retrieval by default, avoid real secrets in command arguments or logged environments, and reserve raw output for private local piping only.

Risk: Audit output may contain sensitive material until the plaintext-prefix issue is fixed.

Mitigation: Treat audit output as sensitive and avoid sharing it in logs, transcripts, or public issue reports.

Risk: Local permissions metadata is not a complete access-control boundary.

Mitigation: Use the skill only in a local, single-user environment and do not rely on permissions.json for security isolation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlacroix82/skills/secrets-manager)
- [README.md](artifact/README.md)
- [CHANGELOG.txt](artifact/CHANGELOG.txt)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [CLI text output with masked secret values by default and optional raw stdout for explicit retrieval]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes encrypted local secret data and a local master-key file under the configured secrets directory.]

## Skill Version(s):

1.1.15 (source: server release evidence and artifact/clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
