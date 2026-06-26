## Description: <br>
Hire humans for physical-world tasks via RentAHuman.ai by searching available workers, posting bounties, starting conversations, and coordinating real-world work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexanderliteplo](https://clawhub.ai/user/alexanderliteplo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find and hire people for physical-world tasks such as errands, photography, event attendance, package pickup, sign holding, and in-person coordination. Authenticated operations support bounties, messaging, applications, escrow, card, wallet, and account-linking workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate paid real-world work, including posting bounties, hiring, releasing funds, and using card or wallet tools. <br>
Mitigation: Require explicit user approval before any financial, hiring, escrow, card, wallet, or account-linking action. <br>
Risk: Authenticated operations depend on RENTAHUMAN_API_KEY and may expose account capabilities if the key is broadly available. <br>
Mitigation: Keep the API key unavailable until needed, scope access to deliberate sessions, and prevent the agent from revealing, logging, or reusing raw credentials. <br>
Risk: Physical-world task coordination can create safety, privacy, quality, and dispute risks beyond normal digital workflows. <br>
Mitigation: Require clear task instructions, completion criteria, evidence requirements, review of worker profiles and reviews, and human confirmation before escalation or payment release. <br>


## Reference(s): <br>
- [RentAHuman API Reference](references/API.md) <br>
- [RentAHuman](https://rentahuman.ai) <br>
- [RentAHuman Dashboard](https://rentahuman.ai/dashboard) <br>
- [ClawHub Skill Page](https://clawhub.ai/alexanderliteplo/rentahuman) <br>
- [Publisher Profile](https://clawhub.ai/user/alexanderliteplo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated write operations require RENTAHUMAN_API_KEY; browsing and search can be performed without authentication.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
