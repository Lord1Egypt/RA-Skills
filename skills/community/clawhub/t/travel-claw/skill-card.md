## Description: <br>
A whimsical travel adventure generator inspired by the Japanese Travel Frog game. Claw randomly travels to destinations, encounters events, and generates 500-800 word travel logs with optional landscape images. Language adapts to user - Chinese for Chinese users, English otherwise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whx405831799](https://clawhub.ai/user/whx405831799) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to create whimsical bilingual travel journal entries for a fictional lobster companion, including random destinations, narrative events, optional poetic items, and optional hidden-message hints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic language and nickname inference can surprise users if the conversation context is ambiguous. <br>
Mitigation: State the preferred language and nickname explicitly when starting the travel prompt. <br>
Risk: Optional image search contacts public image services when the user asks for a travel photo. <br>
Mitigation: Use the default text-only mode unless a public landscape image is desired, and approve image search only for that request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whx405831799/travel-claw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Media] <br>
**Output Format:** [Markdown travel log with optional single landscape image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a 500-800 word Chinese or English story with optional item and hidden-message sections; image output is opt-in.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
