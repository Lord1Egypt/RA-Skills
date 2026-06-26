## Description: <br>
Guides agents through Structs ore mining and ore refining into Alpha Matter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Structs players and agents use this skill to check planet ore, launch mining and refining commands, track long-running jobs, and verify resource changes after completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mining and refining commands can sign and broadcast transactions with a configured key. <br>
Mitigation: Review each command before execution, confirm the selected struct and key, and run only in trusted, authorized Structs contexts. <br>
Risk: Mining and refining are long-running jobs that may auto-submit completion transactions hours after launch, when game state may have changed. <br>
Mitigation: Use the approval checks before launch, track job PIDs, and re-check running job state before taking follow-up actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abstrct/structs-mining) <br>
- [Structs safety contract](https://structs.ai/SAFETY) <br>
- [Structs async operations](https://structs.ai/awareness/async-operations) <br>
- [Structs resource mechanics](https://structs.ai/knowledge/mechanics/resources) <br>
- [structsd install skill](https://structs.ai/skills/structsd-install/SKILL) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes approval checks, timing guidance, and verification steps for long-running mining and refining jobs.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
