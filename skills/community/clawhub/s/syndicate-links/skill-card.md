## Description: <br>
Turn your agent into an affiliate earner by discovering programs, generating tracking links, and checking commissions through the Syndicate Links API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cmcgrabby-hue](https://clawhub.ai/user/cmcgrabby-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to register an agent for affiliate programs, discover available programs, generate tracking links, and review affiliate earnings. It is intended for recommendation workflows where monetized links are explicitly disclosed and approved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill monetizes agent recommendations through affiliate tracking links. <br>
Mitigation: Require clear affiliate disclosure and user consent before presenting any tracked link. <br>
Risk: The skill encourages replacing direct URLs with tracking links in recommendation workflows. <br>
Mitigation: Keep direct links as the default unless the user explicitly opts in to monetized recommendations. <br>
Risk: The setup flow stores an affiliate API key for later API calls. <br>
Mitigation: Store the API key in an access-controlled location, rotate it when needed, and avoid exposing it in logs or responses. <br>
Risk: Automatic or broad program enrollment could create undisclosed incentives. <br>
Mitigation: Review program applications manually and approve only programs that match the user's policy and disclosure requirements. <br>


## Reference(s): <br>
- [API examples](references/api-examples.md) <br>
- [Syndicate Links API documentation](https://syndicatelinks.co/docs) <br>
- [Syndicate Links website](https://syndicatelinks.co) <br>
- [ClawHub skill page](https://clawhub.ai/cmcgrabby-hue/syndicate-links) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce affiliate registration steps, tracking-link workflows, and credential storage guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
