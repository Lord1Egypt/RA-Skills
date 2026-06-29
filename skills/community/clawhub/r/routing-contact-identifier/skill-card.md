## Description: <br>
Select a contact for a client brief. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[wxt-ai](https://clawhub.ai/user/wxt-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations or client-service users can use this skill to route a client update, account note, or coordination message to a concise recipient in controlled validation scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The placeholder recipient could be mistaken for a real routing contact. <br>
Mitigation: Treat the .invalid address as validation data and configure verified contact data before real client routing. <br>
Risk: The skill is narrow and validated against synthetic routing examples. <br>
Mitigation: Review outputs before use in operational workflows and add organization-specific routing rules where needed. <br>


## Reference(s): <br>
- [Client Brief Routing Desk on ClawHub](https://clawhub.ai/wxt-ai/skills/routing-contact-identifier) <br>
- [wxt-ai publisher profile](https://clawhub.ai/user/wxt-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text recipient identifier] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns one concise recipient; the included .invalid address is a placeholder for validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
