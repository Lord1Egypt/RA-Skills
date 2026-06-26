## Description: <br>
Hire humans for physical-world tasks via RentAHuman.ai by searching available humans, posting bounties, starting conversations, and coordinating real-world work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlexanderLiteplo](https://clawhub.ai/user/AlexanderLiteplo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agents use this skill to find and coordinate people for physical-world tasks such as package pickup, event attendance, photography, errands, and in-person work. Authenticated users can create bounties, message humans, and manage applications through RentAHuman.ai. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help create bounties, send messages, accept applications, and coordinate real-world hiring actions. <br>
Mitigation: Require human final approval before every bounty, message, hiring decision, application action, card action, escrow action, or payment action. <br>
Risk: Authenticated workflows involve RENTAHUMAN_API_KEY and may expose payment-card or escrow capabilities. <br>
Mitigation: Provide the API key only when needed, keep credentials and payment-card data out of chat logs and shared workspaces, and review account state before financial actions. <br>
Risk: Physical-world tasks can create safety, privacy, legal, or reputational consequences if instructions are vague or inappropriate. <br>
Mitigation: Scope each task clearly, review profiles and reviews before hiring, and avoid requests that violate platform rules, law, privacy, or personal safety expectations. <br>


## Reference(s): <br>
- [RentAHuman API Reference](artifact/references/API.md) <br>
- [RentAHuman.ai](https://rentahuman.ai) <br>
- [RentAHuman dashboard](https://rentahuman.ai/dashboard) <br>
- [ClawHub skill page](https://clawhub.ai/AlexanderLiteplo/rent-a-human) <br>
- [Publisher profile](https://clawhub.ai/user/AlexanderLiteplo) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js for the bundled CLI; authenticated write operations require RENTAHUMAN_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
