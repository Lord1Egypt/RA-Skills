## Description:

Staking is presented as a staking analysis helper, but the security evidence identifies it as a local plaintext note and configuration utility with persistent write, delete, and export behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this only as a local plaintext note utility for staking-related notes. It should not be relied on for staking analysis, protocol security evaluation, wallet operations, validator operations, or sensitive protocol records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may rely on the skill as staking or protocol security analysis even though security evidence says it behaves as a local note and configuration manager.

Mitigation: Use it only for non-sensitive plaintext notes and require separate trusted tooling or expert review for staking, protocol security, wallet, or validator decisions.

Risk: The script creates, modifies, deletes, and exports local files, including plaintext JSONL data and config values.

Mitigation: Run it in a controlled directory with a deliberate STAKING_DIR value, review file changes before and after use, and avoid storing credentials, wallet details, validator secrets, or sensitive protocol notes.

Risk: Unsafe shell handling may make config or export operations unsuitable for untrusted input.

Mitigation: Do not pass untrusted values to config, search, remove, or export commands; inspect generated files before sharing or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/staking)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Plain text CLI output with JSONL or CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and modifies local plaintext data under STAKING_DIR or ~/.staking and may export files into the current working directory.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
