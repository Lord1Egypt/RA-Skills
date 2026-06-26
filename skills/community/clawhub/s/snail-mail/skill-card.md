## Description: <br>
Snail Mail provides a slow-channel inbox for important operator messages, including notable, abnormal, decision-requiring, unread, read, and archived items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dvdegenz](https://clawhub.ai/user/dvdegenz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Operators and agents use this skill to store, review, mark read, and archive non-urgent but important messages in a local inbox. It supports decision-required, abnormal, interesting, and FYI notifications without interrupting the operator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inbox messages are persisted in a local plain-JSON file and may contain sensitive operator context. <br>
Mitigation: Set OPENCLAW_WORKSPACE to the intended storage location and avoid storing secrets unless local persistence is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dvdegenz/snail-mail) <br>
- [Publisher profile](https://clawhub.ai/user/dvdegenz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Rendered inbox messages as text, Markdown, HTML, or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores messages in a local JSON inbox under the configured workspace.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
