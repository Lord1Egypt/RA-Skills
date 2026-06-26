## Description: <br>
Manages economic operations in Structs, including reactor staking, energy providers, agreements, allocations, generator infusion, and token transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Structs players and operators use this skill to prepare and verify wallet-based economy commands for staking, energy markets, agreements, allocations, generator infusion, and token transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prepared transaction commands can move tokens, lock stake, delete infrastructure, or consume Alpha Matter irreversibly if approved with wrong values. <br>
Mitigation: Before signing, manually verify wallet or key name, recipient or validator address, entity IDs, amounts, denominations, and the action's permanence. <br>
Risk: Suppressing interactive prompts with approved flags can bypass the final user confirmation for Tier 1 or Tier 2 Structs actions. <br>
Mitigation: Keep transaction commands interactive by default and use prompt-suppressing approval flags only after explicit commander approval. <br>
Risk: The skill requires wallet access and sensitive signing credentials through a configured Structs key. <br>
Mitigation: Use least-privileged keys where possible and do not expose private keys or seed phrases to the agent. <br>


## Reference(s): <br>
- [Structs Economy skill page](https://clawhub.ai/abstrct/structs-economy) <br>
- [Structs safety guidance](https://structs.ai/SAFETY) <br>
- [structsd install skill](https://structs.ai/skills/structsd-install/SKILL) <br>
- [structs-energy skill](https://structs.ai/skills/structs-energy/SKILL) <br>
- [Energy market knowledge](https://structs.ai/knowledge/economy/energy-market) <br>
- [Guild banking knowledge](https://structs.ai/knowledge/economy/guild-banking) <br>
- [Resources mechanics](https://structs.ai/knowledge/mechanics/resources) <br>
- [Power mechanics](https://structs.ai/knowledge/mechanics/power) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline shell commands and verification checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires structsd on PATH and a configured signing key; transaction commands should remain interactive unless explicitly approved.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
