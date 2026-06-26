## Description: <br>
Explores new planets and manages fleet movement in Structs. Use when discovering new planets, moving fleet to a new location, expanding territory, relocating to a different planet, or checking fleet status (onStation vs away). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Structs players and operators use this skill to check exploration eligibility, move fleets, and run safe structsd commands for first-time and subsequent planet exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subsequent planet exploration can destroy the old planet and any remaining structs. <br>
Mitigation: Before signing, verify currentOre is 0, the fleet is onStation, and all valued structs were moved or the loss is accepted. <br>
Risk: Fleet movement to unscouted or hostile space can strand the fleet in enemy range. <br>
Mitigation: Query planet and fleet state for nearby hostiles and verify the destination location ID before confirming the transaction. <br>
Risk: Using -y suppresses the CLI confirmation prompt for transactions. <br>
Mitigation: Default to interactive commands and use -y only after intentional commander approval. <br>


## Reference(s): <br>
- [Structs Safety](https://structs.ai/SAFETY) <br>
- [structsd Install Skill](https://structs.ai/skills/structsd-install/SKILL) <br>
- [Planet Mechanics](https://structs.ai/knowledge/mechanics/planet) <br>
- [Fleet Mechanics](https://structs.ai/knowledge/mechanics/fleet) <br>
- [Entity Relationships](https://structs.ai/knowledge/entities/entity-relationships) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires structsd on PATH and a configured signing key.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
