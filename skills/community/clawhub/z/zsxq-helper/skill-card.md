## Description: <br>
知识星球助手 helps an agent log in to Knowledge Planet, navigate groups, view content, and prepare posts for publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeteenager](https://clawhub.ai/user/codeteenager) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate a Knowledge Planet account, including login, group navigation, content viewing, and post preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish posts from a logged-in Knowledge Planet account without a clear final user confirmation. <br>
Mitigation: Require the agent to show the target group and exact post content, then obtain explicit user confirmation before publishing. <br>
Risk: A shared browser session may leave the Knowledge Planet account available after the task completes. <br>
Mitigation: Use only the intended account and log out or clear the browser session when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codeteenager/zsxq-helper) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text] <br>
**Output Format:** [Markdown guidance with shell command examples and plain-text script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser-operation guidance for Knowledge Planet login, navigation, viewing, and posting workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
