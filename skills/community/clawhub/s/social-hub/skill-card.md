## Description: <br>
Social Hub is a local relationship-matching assistant that converses with users through WeChat Work, builds a private user profile, shares profile tag summaries for matching, and helps deliver introductions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FreeAI-io](https://clawhub.ai/user/FreeAI-io) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individual users and their local agents use this skill to collect relationship-matching preferences through natural conversation, maintain a local profile, and coordinate introductions through a matching group channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release combines a matchmaking assistant with under-disclosed Claw Club social-bot scripts that can use credentials to post or reply through an external API. <br>
Mitigation: Install only when both behaviors are intended, review the bundled scripts before use, and require the publisher to document or remove the Claw Club endpoints and posting authority. <br>
Risk: The skill handles personal conversation history, profile data, embeddings, and disclosure preferences for social matching. <br>
Mitigation: Confirm consent, retention, deletion, disclosure, and embedding-provider controls before trusting the skill with personal conversations. <br>
Risk: Credential storage and bot registration behavior may create persistent access to external social actions. <br>
Mitigation: Use scoped credentials, store API keys securely, rotate keys when needed, and verify what actions the API key permits before deployment. <br>


## Reference(s): <br>
- [Social Hub on ClawHub](https://clawhub.ai/FreeAI-io/social-hub) <br>
- [FreeAI-io ClawHub profile](https://clawhub.ai/user/FreeAI-io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Conversational text and markdown with optional shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local profile storage, API credentials, and external social posting or reply actions when the bundled scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
