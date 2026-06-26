## Description: <br>
Use when creating crypto or stablecoin invoices, generating payment quotes, or tracking invoice payment status with the Weave CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AryanJ-NYC](https://clawhub.ai/user/AryanJ-NYC) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Developers and operators use this skill to create Weave crypto invoices, generate payer quote instructions, and monitor invoice settlement from agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto invoice and quote commands can send users toward the wrong asset, network, amount, wallet address, refund address, or invoice ID if inputs are not checked. <br>
Mitigation: Confirm asset, network, amount, wallet address, refund address, and invoice ID before proposing or running create and quote commands. <br>
Risk: The skill relies on the installed Weave CLI package and may be affected by package-source trust or runtime token support drift. <br>
Mitigation: Verify the Weave CLI package source before installation and use `weave tokens` from the installed runtime as the source of truth for supported assets and networks. <br>
Risk: Invoice workflows may involve buyer details or sensitive operational data. <br>
Mitigation: Collect only the buyer details needed for the invoice and never request or expose private keys, seed phrases, JWTs, API tokens, or other secrets. <br>


## Reference(s): <br>
- [Weave CLI Contract Snapshot](references/cli-contract.md) <br>
- [Weave Skill Scenarios](references/scenarios.md) <br>
- [Weave Homepage](https://www.weavecash.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/AryanJ-NYC/weave) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers machine-readable JSON output from the Weave CLI and surfaces structured stderr when command failures occur.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
