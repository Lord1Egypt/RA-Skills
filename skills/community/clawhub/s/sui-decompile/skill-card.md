## Description:

Fetch on-chain Sui Move contract source code and let your agent explain how smart contracts work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easonc13](https://clawhub.ai/user/easonc13)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to retrieve and inspect Sui Move package source from block explorers when studying deployed contracts, DeFi protocols, or multiple-module packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server automation may run Chromium against remote block explorer content with sandbox protections weakened.

Mitigation: Use a sandboxed browser configuration where possible, run automation as an unprivileged user, and isolate it in a disposable environment without secrets.

Risk: Using the Puppeteer/server workflow on CI or shared servers can expose sensitive environments to browser automation risk.

Mitigation: Prefer the simple browser-based source lookup workflow, and avoid running the server automation workflow on systems that contain credentials or production access.

Risk: Explorer-provided or decompiled Move code may be incomplete, misleading, or not directly compilable.

Mitigation: Treat fetched code as analysis material, compare sources when available, and verify behavior against on-chain package data before reusing patterns.

## Reference(s):

- [Sui Decompile ClawHub page](https://clawhub.ai/easonc13/skills/sui-decompile)
- [SuiVision package code explorer](https://suivision.xyz/package/{package_id}?tab=Code)
- [Suiscan contracts explorer](https://suiscan.xyz/mainnet/object/{package_id}/contracts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with browser workflow steps and extracted Move code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce separate .move file contents for packages with multiple modules.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
