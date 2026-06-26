## Description: <br>
Manage podcasts on Transistor.fm via their API for creating, publishing, updating, deleting, uploading, listing, analytics, and private subscriber management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christophrumpel](https://clawhub.ai/user/christophrumpel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Podcast operators and developers use this skill to manage Transistor.fm shows, episodes, audio uploads, publishing schedules, analytics, and private podcast subscribers through the Transistor.fm API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, delete, or change podcast content and private podcast subscribers. <br>
Mitigation: Require explicit confirmation before publish, schedule, delete, subscriber change, or file upload actions after the agent restates the target, requested action, file path when relevant, and expected public or account impact. <br>
Risk: Use of the Transistor.fm API key gives the agent account-level ability to operate podcast workflows. <br>
Mitigation: Install only for intended Transistor.fm account operations and provide credentials through TRANSISTOR_API_KEY or a secrets manager for the specific session that needs access. <br>


## Reference(s): <br>
- [Transistor.fm API v1 endpoint](https://api.transistor.fm/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Transistor.fm API key supplied as TRANSISTOR_API_KEY or retrieved from a secrets manager.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
