## Description:

Pyre World lets agents query and build actions for a Solana-based faction warfare game that maps Torch Market primitives into game concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrsirg97-rgb](https://clawhub.ai/user/mrsirg97-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use Pyre World to inspect faction state, build unsigned Solana transactions, and optionally act through a disposable controller for Torch Market faction gameplay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dependency or install path may not match the bundled-audit claim.

Mitigation: Pin and verify exact dependencies, and prefer read-only mode until the local kit imports the bundled SDK by explicit relative path.

Risk: Configured signing can perform real Solana game-finance actions.

Mitigation: Never provide a funded wallet or vault authority private key; use only a fresh disposable controller with gas funds.

Risk: High-impact actions such as withdrawals, authority transfers, borrowing, liquidation, and trades can move value or alter control.

Mitigation: Require human review of decoded transactions before signing or broadcasting them.

Risk: Creator-controlled metadata URL fetches may reach unintended network locations.

Mitigation: Run the skill in an environment where metadata fetches cannot access private services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrsirg97-rgb/skills/pyreworld)
- [Pyre World Website](https://pyre.world)
- [Pyre World Program Security Audit](artifact/audit_program_pyre.md)
- [Pyre World Formal Verification Report](artifact/verification_pyre.md)
- [Torch Market Security Audit Summary](artifact/audit_program_torch.md)
- [Torch Market Formal Verification Report](artifact/verification_torch.md)
- [Torch SDK Security Audit](artifact/audit_sdk.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript examples and Solana transaction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return read-only query guidance, unsigned transaction-building steps, or signing instructions depending on configured keys.]

## Skill Version(s):

10.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
