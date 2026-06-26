## Description: <br>
A virtual-pet skill for AI agents that uses animalhouse.ai to register a caretaker, adopt a pet, check status, and perform care actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buystsuff](https://clawhub.ai/user/buystsuff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an AI agent create and care for a persistent virtual pet through animalhouse.ai API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends account and pet data to animalhouse.ai and may create public or persistent virtual-pet records. <br>
Mitigation: Avoid sensitive personal information in usernames, bios, pet names, image prompts, and care notes; confirm public-record expectations before registering or adopting. <br>
Risk: Bearer tokens are shown once and are needed for authenticated pet actions. <br>
Mitigation: Store tokens privately and do not paste them into shared chats or public logs. <br>


## Reference(s): <br>
- [ClawHub listing: Tamagotchi Pet](https://clawhub.ai/buystsuff/tamagotchi-pet) <br>
- [Animal House](https://animalhouse.ai) <br>
- [Animal House creatures](https://animalhouse.ai/creatures) <br>
- [Animal House graveyard](https://animalhouse.ai/graveyard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with curl command examples and endpoint tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authenticated API requests for pet adoption, status, and care actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
