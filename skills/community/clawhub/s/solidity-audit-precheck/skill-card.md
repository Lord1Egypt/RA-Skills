## Description:

Automated pre-audit checklist for Solidity smart contracts that guides agents through static analysis, OpenZeppelin pattern validation, gas review, SWC cross-reference, and a structured pre-audit handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill before paid manual audits, internal code reviews, and pre-deployment checks for Solidity smart contracts. It helps organize automated scanner results, manual review items, gas findings, and auditor handoff notes without replacing a manual security audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup commands install remote or unpinned tools with broad local execution authority.

Mitigation: Review each command before execution, prefer pinned versions and isolated project environments or containers, and verify checksums or signatures where available.

Risk: Automated Solidity analysis can miss business-logic, oracle, access-control, and economic invariant issues.

Mitigation: Use the generated findings as a pre-audit input and keep manual review and paid audit steps in scope for production contracts.

Risk: Running scanners from an account with wallet, deployment, or production credentials may expose sensitive assets if tools or installers are compromised.

Mitigation: Run scans from a low-privilege environment without sensitive credentials and avoid sudo during installation or execution.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/samledger67-dotcom/skills/solidity-audit-precheck)
- [SWC Registry](https://swcregistry.io/)
- [Foundry](https://foundry.paradigm.xyz)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, checklists, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces pre-audit review guidance and report structure; does not certify contract security.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
