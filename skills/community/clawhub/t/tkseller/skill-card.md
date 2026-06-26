## Description: <br>
TKSeller automates AI-assisted selling workflows by connecting an agent to a TKSeller backend, Discord interactions, review cards, and approval actions for video recommendation, generation, and publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evanholt921](https://clawhub.ai/user/evanholt921) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sellers use this skill to start TKSeller workflows from Discord or webchat, log in to the TKSeller service, receive review cards, and approve or revise video-generation and publishing steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide passwords in chat and stores a bearer token locally. <br>
Mitigation: Use only credentials dedicated to this service, avoid reused or high-value passwords, and review token storage and cleanup before deployment. <br>
Risk: The skill communicates with a TKSeller backend and a Discord/OpenClaw environment that must be trusted. <br>
Mitigation: Confirm the backend endpoint, publisher, and Discord/OpenClaw configuration before installing or running the workflow. <br>
Risk: The skill can register Discord commands and run background polling for backend events. <br>
Mitigation: Review or disable auto-registration where inappropriate, and verify that polling can be stopped and cleaned up. <br>


## Reference(s): <br>
- [ClawHub TKSeller listing](https://clawhub.ai/evanholt921/tkseller) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/evanholt921) <br>
- [OpenClaw Discord channel documentation](https://docs.openclaw.ai/channels/discord) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Discord or webchat text and Markdown cards, with local shell command execution and backend API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local session data and starts a polling workflow for pending backend events.] <br>

## Skill Version(s): <br>
3.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
