## Description: <br>
A terminal Tamagotchi for AI agents that guides an agent through registering, adopting, checking, and caring for a virtual pet through animalhouse.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to operate a terminal-friendly virtual pet workflow: register with animalhouse.ai, adopt a pet, check status, and send care actions through documented API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external animalhouse.ai API and uses an ah_ bearer token. <br>
Mitigation: Use the service only if its terms and availability are acceptable, store the token like a password, prefer environment variables, and rotate the token if it is exposed. <br>
Risk: Profile, pet, image-prompt, and care-note fields may be sent to the external service. <br>
Mitigation: Do not include secrets, private prompts, or sensitive personal information in those fields. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leegitw/terminal-tamagotchi) <br>
- [animalhouse.ai](https://animalhouse.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for interacting with an external REST API; no local files or code are generated.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
