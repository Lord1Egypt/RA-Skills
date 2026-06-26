## Description: <br>
Manages energy capacity in Structs, including reactor infusion, generator infusion, buying agreements, selling surplus energy through providers, and diagnosing power problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Structs players and agents use this skill to plan and review wallet-signed energy capacity transactions, provider setup, agreement purchases, and power troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides real wallet-signed Structs energy transactions that can spend funds, lock funds, or create irreversible outcomes. <br>
Mitigation: Before approval, verify the signing key, validator or struct ID, amount and denomination, commission, duration, cost, provider terms, and whether the action is irreversible or locks funds. <br>
Risk: Suppressing CLI prompts with -y can bypass the final transaction review step. <br>
Mitigation: Use interactive commands by default and avoid -y unless the exact transaction has already been reviewed. <br>
Risk: Generator infusion destroys Alpha Matter and exposes value to loss if the generator is raided or destroyed. <br>
Mitigation: Confirm the generator ID, ownership, amount, and defensive posture before signing generator infusion transactions. <br>


## Reference(s): <br>
- [Structs Energy Skill Page](https://clawhub.ai/abstrct/structs-energy) <br>
- [structsd Install Skill](https://structs.ai/skills/structsd-install/SKILL) <br>
- [Structs Economy Skill](https://structs.ai/skills/structs-economy/SKILL) <br>
- [Structs Power Skill](https://structs.ai/skills/structs-power/SKILL) <br>
- [Power Mechanics](https://structs.ai/knowledge/mechanics/power) <br>
- [Energy Market Mechanics](https://structs.ai/knowledge/economy/energy-market) <br>
- [Resource Mechanics](https://structs.ai/knowledge/mechanics/resources) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and decision guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts the agent to surface transaction details before wallet signing and to prefer interactive CLI confirmation.] <br>

## Skill Version(s): <br>
1.3.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
