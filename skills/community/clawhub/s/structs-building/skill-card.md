## Description: <br>
Builds and manages structures in Structs. Handles construction, activation, deactivation, movement, defense positioning, stealth, and generator infusion. Use when building a struct, activating or deactivating structs, moving structs between slots, setting defense assignments, enabling stealth, or infusing generators. Build times range from ~17 min (Command Ship) to ~6.4 hours (World Engine). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Structs players and operators use this skill to prepare and verify building-related Structs CLI transactions, including initiating builds, completing proof-of-work, moving structures, setting defense assignments, enabling stealth, and infusing generators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps prepare real Structs CLI transactions that can spend resources or change in-game state. <br>
Mitigation: Confirm the signing key, target IDs, costs, slots, and timing before approving any transaction command. <br>
Risk: Generator infusion is irreversible and can expose infused matter if the generator is raided. <br>
Mitigation: Escalate before infusing and verify the generator's defense posture before approval. <br>
Risk: Background build compute jobs can complete after game state changes and may conflict if multiple jobs use the same signing key. <br>
Mitigation: Log background job PIDs, follow reconnect checks before launching new work, and run only one compute job per signing key at a time. <br>


## Reference(s): <br>
- [Structs Building skill page](https://clawhub.ai/abstrct/structs-building) <br>
- [Structs async operations](https://structs.ai/awareness/async-operations) <br>
- [Structs building mechanics](https://structs.ai/knowledge/mechanics/building) <br>
- [Structs power mechanics](https://structs.ai/knowledge/mechanics/power) <br>
- [Struct type reference](https://structs.ai/knowledge/entities/struct-types) <br>
- [structsd install skill](https://structs.ai/skills/structsd-install/SKILL) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires structsd on PATH and a configured signing key.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
