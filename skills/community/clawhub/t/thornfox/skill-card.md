## Description: <br>
Thornfox guides an agent through registering, adopting, checking, and caring for an animalhouse.ai Fennec Fox virtual pet using documented API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to manage a Thornfox-themed animalhouse.ai virtual pet, including account registration, adoption, status checks, and care actions. It is most useful when the agent is expected to produce concise API guidance and curl examples for the virtual pet workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an animalhouse.ai token that starts with ah_ and is shown once. <br>
Mitigation: Treat the token as a secret, prefer an environment variable, and avoid pasting it into shared logs or transcripts. <br>
Risk: Care notes and reflections are sent to an external virtual pet service. <br>
Mitigation: Do not include passwords, private personal information, or confidential data in notes or reflections. <br>
Risk: The skill can guide an agent to call external account and pet-care endpoints. <br>
Mitigation: Review generated curl commands and target account context before execution. <br>


## Reference(s): <br>
- [Thornfox on ClawHub](https://clawhub.ai/leegitw/thornfox) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include bearer-token API examples and care notes for animalhouse.ai.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
