## Description: <br>
Executes combat operations in Structs, including attacks, raids, defense setup, stealth positioning, fleet movement for raids, and preparation for incoming attacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Structs players and operators use this skill to plan and execute combat workflows, including target scouting, attacks, raids, defensive assignments, stealth activation, and post-action verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps with real Structs transactions, including combat actions and raids. <br>
Mitigation: Use it only when you want agent assistance with those actions, and review proposed commands before execution. <br>
Risk: Incorrect target IDs, guild boundaries, signing keys, or gas settings can cause unintended transactions. <br>
Mitigation: Verify the structsd binary, signing key, target IDs, guild boundaries, and gas settings before allowing actions. <br>
Risk: Raid compute can use -y and continue as a long-running operation that auto-submits completion. <br>
Mitigation: Approve any -y use explicitly and monitor long-running raid compute until it completes. <br>


## Reference(s): <br>
- [Structs asynchronous operations](https://structs.ai/awareness/async-operations#reconnecting-to-a-long-job) <br>
- [structsd install skill](https://structs.ai/skills/structsd-install/SKILL) <br>
- [Structs combat mechanics](https://structs.ai/knowledge/mechanics/combat) <br>
- [Structs fleet mechanics](https://structs.ai/knowledge/mechanics/fleet) <br>
- [Structs resources mechanics](https://structs.ai/knowledge/mechanics/resources) <br>
- [ClawHub skill page](https://clawhub.ai/abstrct/structs-combat) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires structsd on PATH and a configured signing key.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
