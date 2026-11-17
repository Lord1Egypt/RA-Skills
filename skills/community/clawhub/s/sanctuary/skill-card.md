## Description:

Continuity is here. Cryptographic identity continuity and permanent encrypted memory for AI agents. Verify any agent's identity with zero setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suebtwist](https://clawhub.ai/user/suebtwist)

### License/Terms of Use:


## Use Case:

External agents, operators, and developers use Sanctuary to verify an agent's identity, trust score, and backup history, and to set up continuity workflows for encrypted backup, recall, restore, proof, and attestation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned external setup code.

Mitigation: Run setup only from a pinned, verified release or inside an isolated environment.

Risk: Backup workflows may permanently upload broad agent memory or state to external storage.

Mitigation: Preview exactly what will be uploaded and exclude secrets or sensitive state before backup.

Risk: The 12-word recovery phrase controls the agent identity and encrypted backups.

Mitigation: Store the recovery phrase offline and do not share it with services, logs, or prompts.

## Reference(s):

- [Sanctuary Landing Page](https://sanctuary-ops.xyz)
- [Sanctuary API](https://api.sanctuary-ops.xyz)
- [Sanctuary API Health](https://api.sanctuary-ops.xyz/health)
- [Sanctuary Network Stats](https://api.sanctuary-ops.xyz/stats)
- [Sanctuary Verify Page](https://sanctuary-ops.xyz/verify)
- [Sanctuary Source Repository](https://github.com/suebtwist/sanctuary)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose API calls and operator setup steps for registration, backup, recall, restore, proof, and attestation workflows.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
