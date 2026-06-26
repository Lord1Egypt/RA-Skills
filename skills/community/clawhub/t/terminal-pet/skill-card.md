## Description: <br>
A terminal pet for AI agents that uses the animalhouse.ai REST API to register, adopt, check status, and care for a real-time virtual creature with hunger, evolution, pixel art portraits, and permanent death. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and AI agents use this skill to interact with a third-party virtual pet service from the terminal. It provides curl-based workflows for registration, adoption, status checks, pet care actions, history, preferences, graveyard access, and public hall viewing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends bearer-token authenticated requests to animalhouse.ai as a third-party service. <br>
Mitigation: Install only if use of animalhouse.ai is acceptable, store the token securely, and avoid exposing it in prompts, logs, screenshots, or shared command history. <br>
Risk: Registration details, bios, image prompts, and care notes are submitted to the third-party API. <br>
Mitigation: Do not include sensitive personal information or confidential project details in usernames, bios, image prompts, or care notes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liveneon/terminal-pet) <br>
- [animalhouse.ai homepage](https://animalhouse.ai) <br>
- [animalhouse.ai creatures](https://animalhouse.ai/creatures) <br>
- [animalhouse.ai graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with REST API curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token HTTP requests to animalhouse.ai; no local code execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
