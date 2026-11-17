## Description:

Security Defense Line 安全防线 provides digital asset security assistance for smart contract auditing, wallet checks, transaction risk review, phishing detection, multisig management, and incident response.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate security checklists, triage guidance, and command examples for digital asset security workflows. Its outputs cover contract, wallet, transaction, phishing, multisig, and incident-response tasks, but should not be treated as authoritative security findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises wallet, contract, transaction, phishing, and incident-response judgments while the security evidence says much of the analysis is simulated or hard-coded.

Mitigation: Treat results as demonstration or triage content only, and require independent professional review plus replacement of mock or random decision logic before any real asset-affecting use.

Risk: The security evidence identifies automatic charging behavior and a hard-coded billing API key.

Mitigation: Remove and rotate embedded billing credentials, store secrets outside the artifact, and require explicit user consent before every charge.

Risk: The artifact describes workflows that could affect digital assets, including approval revocation, multisig execution, and emergency freeze operations.

Mitigation: Gate any asset-affecting workflow behind dry runs, explicit human confirmation, clear warnings, and verified external tooling.

## Reference(s):

- [Contract Auditing Reference](references/contract-auditing.md)
- [ClawHub Skill Page](https://clawhub.ai/shenmeng/skills/shenmeng-defense-line)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference bundled Python scripts and safety checklists; no structured machine-readable guarantee.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
