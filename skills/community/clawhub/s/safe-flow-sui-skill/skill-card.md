## Description:

Safeflow Sui Skill helps agents run owner-assisted SafeFlow workflows for Sui test payments, Publish API and Walrus end-to-end tests, and SQL package ID synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwangzil](https://clawhub.ai/user/fwangzil)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to coordinate owner-assisted SafeFlow setup, configure Sui wallet/session identifiers, execute controlled test payments, run Publish API and Walrus integration checks, and sync package IDs into SQL-backed runtime configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute blockchain payments.

Mitigation: Use a dedicated testnet wallet with limited funds and review the recipient and amount before every run.

Risk: The skill stores wallet and session capability identifiers used for payment operations.

Mitigation: Treat saved wallet/session capability files as sensitive operational data and restrict access to the local workspace.

Risk: Publish API flows may pass API keys or requests to operator-provided URLs.

Mitigation: Avoid passing API keys to untrusted URLs and verify the Publish API endpoint before running integration tests.

Risk: Npx-based flows can resolve executable dependencies at runtime.

Mitigation: Pin the tsx dependency locally before using npx-based flows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fwangzil/skills/safe-flow-sui-skill)
- [Owner Handoff Flow](references/owner-handoff-flow.md)
- [Publish API Test Flow](references/publish-api-test-flow.md)
- [Package ID SQL Sync](references/sql-sync.md)
- [Troubleshooting](references/troubleshooting.md)
- [Sui CLI Installation](https://docs.sui.io/guides/developer/getting-started/sui-install)
- [Sui CLI Reference](https://docs.sui.io/references/cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash commands and JSON configuration artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local operational files such as agent address, owner handoff, SafeFlow config, environment exports, and SQL runtime configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
