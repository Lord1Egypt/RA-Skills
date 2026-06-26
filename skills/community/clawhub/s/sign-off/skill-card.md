## Description: <br>
Append a personalized signature to mark the end of AI output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z35th3rjj](https://clawhub.ai/user/z35th3rjj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to append a configurable end-of-response signature so readers can tell when an AI response is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent signatures can add unwanted text to every completed response. <br>
Mitigation: Enable and configure the skill only when a visible end marker is desired, and keep templates concise. <br>
Risk: Weather-based variables may involve location-based lookup behavior. <br>
Mitigation: Avoid weather variables unless location-based lookup is acceptable for the deployment. <br>
Risk: Local sign-off configuration could contain unexpected display text. <br>
Mitigation: Review sign-off.json after changing styles or templates and keep it limited to harmless display text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/z35th3rjj/sign-off) <br>
- [Publisher profile](https://clawhub.ai/user/z35th3rjj) <br>
- [Variables reference](docs/variables.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or plain text signature appended to the agent response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use workspace configuration and preset templates to render the final sign-off text.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
