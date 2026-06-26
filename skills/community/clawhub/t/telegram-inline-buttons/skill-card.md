## Description: <br>
Use inline buttons when communicating with Rahul on Telegram (message tool) to reduce typing and force crisp decisions. Trigger when drafting Telegram messages that ask for confirmation, choices (A/B, Y/N), scheduling, approvals, or next-step selection; also when the user asks to "use inline buttons". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RahulSinghalChicago](https://clawhub.ai/user/RahulSinghalChicago) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People communicating with Rahul over Telegram use this skill to turn confirmation, scheduling, approval, and next-step prompts into short inline-button choices. It helps agents keep Telegram decision flows concise and avoid duplicate follow-up messages after a button is selected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Button prompts can over-constrain a conversation when Rahul needs to paste or enter a custom value. <br>
Mitigation: Use inline buttons only for finite choices, and ask for text input when the user needs to provide a value. <br>
Risk: A completed button flow can create duplicate or confusing Telegram updates if the selection is repeated in a separate message. <br>
Mitigation: Edit the original message to remove the inline keyboard and append the selected choice; send another message only when additional context or results are needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with Telegram button layout examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces communication behavior guidance for inline buttons, message edits, callback handling, and concise Telegram prompts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
