## Description: <br>
Sister.skill helps an agent build local profiles from a user's descriptions and memories, then generate personality-style responses or group chat simulations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realteamprinz](https://clawhub.ai/user/realteamprinz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to organize their own memories and descriptions of sisters, best friends, and creators into local profiles. They can ask an agent to respond in a captured communication style or simulate a group chat while keeping the files local. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plain-text local profiles and logs about real people may retain sensitive personal details. <br>
Mitigation: Use explicit consent where possible, prefer pseudonyms, avoid sensitive categories, and regularly review or delete ~/.sister-skill/sisters/. <br>
Risk: Generated responses may be mistaken for the real person's actual views. <br>
Mitigation: Present outputs as simulations based on the user's memories and do not claim they are the profiled person's real statements. <br>


## Reference(s): <br>
- [Sister Archetypes Reference Guide](references/sister-archetypes.md) <br>
- [ClawHub skill page](https://clawhub.ai/realteamprinz/sister) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown profiles, JSONL interaction logs, and plain text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill stores profile and log files locally under ~/.sister-skill/sisters/ when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
