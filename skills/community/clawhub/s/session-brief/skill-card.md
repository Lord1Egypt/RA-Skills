## Description: <br>
Produce a compact, complete context dump of the current session directly in chat. Use when the user wants the current conversation summarized for reference, asks for a context dump, says the chat is bloated or slow, or wants a concise session state without creating files or migrating to a new chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vyctorbrzezowski](https://clawhub.ai/user/vyctorbrzezowski) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other agent users use this skill to produce a concise Markdown summary of the current conversation state for handoff, reference, or reducing chat context noise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A session summary could include sensitive conversation details if the user asks for them or if they were present in context. <br>
Mitigation: Review the generated brief before sharing it and avoid including secrets, credentials, or sensitive personal details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vyctorbrzezowski/session-brief) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown block in chat] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not create files unless the user explicitly asks; excludes secrets, credentials, and unnecessary personal data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
