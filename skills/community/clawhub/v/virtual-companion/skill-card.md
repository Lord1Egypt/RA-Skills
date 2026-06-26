## Description: <br>
Virtual Companion helps agents register, adopt, monitor, and care for a virtual pet through animalhouse.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obviouslynot](https://clawhub.ai/user/obviouslynot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to let an agent create and manage an animalhouse.ai virtual pet, including registration, adoption, status checks, care actions, and history or graveyard views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens could be exposed through logs, shared chats, or pasted command output. <br>
Mitigation: Keep the animalhouse.ai token private, avoid logging it, and replace examples with local secret handling before reuse. <br>
Risk: Adoption, care notes, and pet state changes are sent to an external service. <br>
Mitigation: Review requests before execution and avoid sending sensitive or unnecessary personal information in pet names, prompts, or notes. <br>
Risk: Automated or scheduled care actions can change companion state without direct review. <br>
Mitigation: Review any heartbeat or automation schedule before enabling it and keep manual oversight for recurring actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/obviouslynot/virtual-companion) <br>
- [Publisher profile](https://clawhub.ai/user/obviouslynot) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House creatures](https://animalhouse.ai/creatures) <br>
- [Animal House graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with bash code blocks and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authenticated requests for adoption, care, status, preferences, history, and graveyard operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
