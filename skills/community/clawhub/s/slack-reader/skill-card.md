## Description: <br>
Reads Slack channel history, thread conversations, and individual replies so an agent can summarize discussions or inspect recent messages from Slack links or channel IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Epikoding](https://clawhub.ai/user/Epikoding) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, support teams, and workspace users use this skill to fetch Slack channel history, full threads, or single replies for summarization and review by an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read large amounts of private Slack content available to the configured bot token. <br>
Mitigation: Use the narrowest applicable Slack link, limit, and date range, and confirm whether thread replies should be included before fetching channel history. <br>
Risk: Slack user-name mappings are cached locally on disk. <br>
Mitigation: Review the local cache at ~/.cache/slack-reader/users.json and the configured Slack bot scopes before deployment. <br>


## Reference(s): <br>
- [Slack Thread Reader on ClawHub](https://clawhub.ai/Epikoding/slack-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text Slack transcript output with concise Markdown usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chronological output may include timestamps, Slack message IDs, sender names, reactions, attachment identifiers, thread participation, and channel metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
