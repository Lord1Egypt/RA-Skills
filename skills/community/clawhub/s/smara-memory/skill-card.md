## Description: <br>
Persistent memory for AI agents - store, search, and recall user context via the Smara Memory API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parallelromb](https://clawhub.ai/user/parallelromb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give agents persistent user memory, including storing user facts, searching memories by meaning, retrieving user context, and deleting stored memories through the Smara API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store and retrieve user facts with an external memory service without clear consent or sensitivity boundaries. <br>
Mitigation: Require explicit user consent for persistent memory, define what categories may be saved, and give users a way to review and delete stored memories. <br>
Risk: Sensitive personal data or secrets could be persisted unintentionally. <br>
Mitigation: Avoid storing secrets, credentials, health, financial, or other sensitive personal data by default, and use a scoped or revocable API key. <br>


## Reference(s): <br>
- [Smara](https://smara.io) <br>
- [Smara API documentation](https://api.smara.io/docs/) <br>
- [ClawHub skill page](https://clawhub.ai/parallelromb/smara-memory) <br>
- [Publisher profile](https://clawhub.ai/user/parallelromb) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SMARA_API_KEY and sends memory data to the Smara API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
