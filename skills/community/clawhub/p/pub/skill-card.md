## Description: <br>
Create adaptive interfaces and real-time experiences via the pub CLI, with live P2P browser sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmanatee](https://clawhub.ai/user/xmanatee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to publish generated HTML, Markdown, or text through the pub CLI and to run live browser canvas/chat sessions on pub.blue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pub CLI requires a PUB_API_KEY and stores configuration and runtime state locally. <br>
Mitigation: Use a scoped key where possible and set PUB_HOME to a dedicated absolute directory when containment is needed. <br>
Risk: Publishing, public visibility, update, and delete commands can expose or alter user content. <br>
Mitigation: Review generated content before using --public, update, or delete commands; keep pubs private unless public sharing is intended. <br>
Risk: Live sessions run a local daemon and bridge messages between the browser session and agent runtime. <br>
Mitigation: Check status and logs when starting live mode, run pub doctor for validation, and stop the daemon when the session is complete. <br>


## Reference(s): <br>
- [Pub homepage](https://pub.blue) <br>
- [Pub agent setup](https://pub.blue/agents) <br>
- [Pub CLI releases](https://github.com/xmanatee/pub/releases/latest) <br>
- [ClawHub skill page](https://clawhub.ai/xmanatee/pub) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, markdown, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated HTML, Markdown, or text content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pub CLI and PUB_API_KEY; live sessions may write to chat or canvas channels.] <br>

## Skill Version(s): <br>
5.2.17 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
