## Description: <br>
Deploy and manage multi-signature smart accounts on supported EVM chains, including smart wallet creation, owner changes, signing-threshold changes, and wallet overview checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and wallet operators use this skill to deploy EVM smart accounts, inspect wallet details, and manage multi-signature account ownership and thresholds through approved fdx commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated smart-wallet commands can change account control or access. <br>
Mitigation: Before approving execution, verify the chain, smart account address, owner addresses, requested action, and signing threshold with the human operator. <br>
Risk: Removing too many owners or setting a threshold above the available owner count can lock the account. <br>
Mitigation: Confirm the resulting owner set and ensure the threshold remains valid before running ownership-management commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires human confirmation before authenticated smart-wallet operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
