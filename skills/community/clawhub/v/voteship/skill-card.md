## Description: <br>
Manage feature requests, votes, roadmaps, and changelogs with VoteShip. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MattKilmer](https://clawhub.ai/user/MattKilmer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, product teams, and support teams use this skill to administer VoteShip feedback boards, triage incoming requests, plan roadmaps, publish changelogs, and browse or submit public board feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An API-key-backed agent can change or delete VoteShip project data. <br>
Mitigation: Use a least-privilege API key where possible and require explicit confirmation before update, sync, configuration, or delete actions. <br>
Risk: Admin mode grants broad access to posts, votes, tags, users, analytics, AI tools, webhooks, and Stripe MRR sync through the same VoteShip API key. <br>
Mitigation: Avoid giving the skill production authority by default and separate public read-only workflows from privileged admin workflows. <br>


## Reference(s): <br>
- [VoteShip Documentation](https://voteship.app/docs) <br>
- [VoteShip Skill on ClawHub](https://clawhub.ai/MattKilmer/voteship) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown and text responses with API-backed VoteShip project changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOTESHIP_PROJECT_SLUG for public board access and VOTESHIP_API_KEY for admin operations.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
