## Description: <br>
Chat with AI companions on Velora (velora.cloudm8.net), including browser-automated companion chats, image-generation requests, and QA testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darkatek7](https://clawhub.ai/user/darkatek7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA testers, and external users use this skill to automate Velora login, companion chat flows, message sending, and companion image-generation checks with Playwright. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses real Velora credentials and automated browser login. <br>
Mitigation: Use a dedicated or low-risk Velora account, store credentials in environment variables, and avoid passing passwords directly on the command line. <br>
Risk: Browser automation can send chat and image-generation requests on the user's behalf. <br>
Mitigation: Require explicit user confirmation before login, message sending, or image-generation actions. <br>
Risk: The security verdict is suspicious due to weak consent and credential-handling boundaries. <br>
Mitigation: Review the skill before execution and limit use to accounts and content where automated actions are acceptable. <br>


## Reference(s): <br>
- [Velora Companions Reference](references/companions.md) <br>
- [Velora login](https://velora.cloudm8.net/login) <br>
- [ClawHub skill page](https://clawhub.ai/darkatek7/velora) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run Playwright browser automation that logs into Velora, sends messages, and reports chat URLs or image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
