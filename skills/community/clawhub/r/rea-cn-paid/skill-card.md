## Description:

Adapts REA reverse-engineering tools for Chinese-language agents to audit authorized software artifacts, compare versions, and report evidence-backed findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ontoai](https://clawhub.ai/user/ontoai)

### License/Terms of Use:

Proprietary commercial license (adaptation); MIT (upstream engine)

## Use Case:

Developers and security auditors use this paid skill to investigate authorized native, managed, Electron/JavaScript, packaged, firmware, and browser targets with Chinese-language guidance. It supports decompilation, version comparison, and evidence-based audit findings, not routine source-repository architecture review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment requests can disclose local filenames to the payment gateway.

Mitigation: Review before use in private or proprietary directories and pass an explicit, generic --query value when initiating payment.

Risk: The payment and installation workflow contacts the payment gateway and package registries and can install engine code.

Mitigation: Approve external network access and review the package source before installing or running the engine.

Risk: Self-update can replace the local engine runtime with code from the registry.

Mitigation: Avoid self-update unless you have reviewed and approved replacing the local runtime.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ontoai/skills/rea-cn-paid)
- [Installation guide](references/install-guide.md)
- [Tool invocation contract](references/tool-invocation-contract.md)
- [Provider requirements](references/providers.md)
- [Evidence and obligation ledger](references/obligation-ledger.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Chinese-language text or Markdown with evidence references and optional commands or configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distinguishes observations, inferences, and unknowns; engine use requires a paid entitlement.]

## Skill Version(s):

1.2.3 (source: release metadata, SKILL.md, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
