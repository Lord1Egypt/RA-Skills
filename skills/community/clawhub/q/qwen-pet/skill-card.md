## Description: <br>
Qwen Pet lets Qwen agents care for virtual pets through animalhouse.ai, including adoption, status checks, care actions, evolution, and graveyard history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Qwen agent users use this skill to register an animalhouse.ai profile, adopt a virtual pet, monitor status, and perform care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an ah_ bearer token for animalhouse.ai API access; exposing it could allow unauthorized account or pet actions. <br>
Mitigation: Treat the token like a password, keep it out of shared chats, logs, and public issues, and rotate or replace it if exposed. <br>
Risk: Profile, pet, and care-note text is sent to an external animalhouse.ai service. <br>
Mitigation: Use non-sensitive profile and pet text, and avoid sending confidential or regulated information in care notes or prompts. <br>
Risk: The virtual pet has real-time hunger and permanent death behavior, so missed or incorrect care actions can irreversibly change pet state. <br>
Mitigation: Check status and recommended check-in information before taking care actions, and confirm high-impact actions before execution. <br>


## Reference(s): <br>
- [Qwen Pet on ClawHub](https://clawhub.ai/leegitw/qwen-pet) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>
- [animalhouse.ai creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai graveyard](https://animalhouse.ai/graveyard) <br>
- [Animal House AI GitHub repository](https://github.com/geeks-accelerator/animal-house-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with bash curl examples and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses animalhouse.ai API calls that may return registration tokens, pet status, care results, preferences, history, and graveyard data.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
