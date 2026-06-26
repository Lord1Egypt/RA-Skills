## Description: <br>
Web Change Monitor helps users track configured webpages for content, keyword, selector, or regex changes and prepare Feishu change notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiji0802](https://clawhub.ai/user/qiji0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users can monitor product pages, inventory listings, pricing pages, forums, or other public webpages and receive a change summary when configured conditions change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitored URLs, timestamps, change details, and sometimes fetched HTML may be stored locally in SQLite. <br>
Mitigation: Avoid monitoring private, authenticated, internal, or regulated pages unless local retention is acceptable. <br>
Risk: Notification behavior may require setup review because the artifact documents Feishu push while evidence notes only message-building code is included. <br>
Mitigation: Verify dependencies and notification delivery behavior before relying on alerts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiji0802/web-change-monitor) <br>
- [Changelog](references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces monitoring task guidance, status summaries, change logs, and Feishu-style notification text.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
