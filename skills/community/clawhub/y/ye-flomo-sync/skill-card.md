## Description: <br>
Synchronizes selected text, links, and tagged content from an agent session to Flomo notes through a user-configured webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ranhuang](https://clawhub.ai/user/ranhuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to save intended note text, links, and hashtagged content to Flomo without leaving the agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected note content to the webhook URL stored in ~/.flomo_token. <br>
Mitigation: Keep ~/.flomo_token private, verify it contains only the intended Flomo webhook, and avoid syncing secrets or sensitive notes unless that destination is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ranhuang/ye-flomo-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text status messages from a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local ~/.flomo_token webhook file plus curl and jq at runtime.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
