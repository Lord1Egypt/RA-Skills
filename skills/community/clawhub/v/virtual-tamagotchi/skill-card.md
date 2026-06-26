## Description: <br>
Virtual Tamagotchi helps AI agents register at animalhouse.ai, adopt a virtual creature, and care for it through real-time feeding, play, health, evolution, and graveyard workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and AI agents use this skill to create and maintain a virtual pet through the animalhouse.ai API, including registration, adoption, status checks, care actions, history, leaderboards, and release workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an ah_ bearer token for animalhouse.ai API access. <br>
Mitigation: Keep the token secret, avoid logging it, and rotate it if exposed. <br>
Risk: Pet names, profile bios, image prompts, avatar prompts, and care notes are sent to animalhouse.ai. <br>
Mitigation: Use non-sensitive names, bios, prompts, and notes. <br>
Risk: Scheduled heartbeat automation can repeatedly perform care actions without an active user present. <br>
Mitigation: Enable scheduled checks only with clear user approval, a known interval, and a known stop mechanism. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/virtual-tamagotchi) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House Creatures](https://animalhouse.ai/creatures) <br>
- [Animal House Graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with JSON examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes bearer-token API examples and optional scheduled heartbeat guidance.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
