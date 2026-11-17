## Description:

Inspects a single EVM transaction with Skylens APIs and returns human-readable traces, balance changes, storage changes, nonce changes, and contract source files for supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[certik-ai](https://clawhub.ai/user/certik-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and investigators use this skill to inspect one supported EVM transaction at a time, including execution traces, holder balance deltas, contract storage changes, nonce changes, and related contract source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes a local Python script and makes outbound HTTPS requests to skylens.certik.com.

Mitigation: Install and run it only in environments where local script execution and outbound access to that service are permitted.

Risk: The get-source-file command can write remotely fetched contract source to a user-specified path.

Mitigation: Use --OUTPUT only with a safe workspace path and review saved files before trusting or executing them.

## Reference(s):

- [Skylens](https://skylens.certik.com/)
- [ClawHub Skill Page](https://clawhub.ai/certik-ai/skills/skylens-transaction-analysis)
- [CertiK Publisher Profile](https://clawhub.ai/user/certik-ai)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Plain text command output, readable trace lines, and optional saved source code files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on one transaction and selected chain/address parameters; trace output supports offset and size pagination.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
