## Description: <br>
v0-cli helps agents create, refine, and list v0.dev-generated websites from the terminal without interactive prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hlongvu](https://clawhub.ai/user/hlongvu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to automate v0.dev website creation, continue existing v0 chats, and list generated projects from shell workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to operate a user's v0.dev account through V0_API_KEY. <br>
Mitigation: Install only when account operation is intended, review the external npm CLI before use, and avoid including secrets, private code, customer data, or confidential business details in prompts. <br>
Risk: Generated v0 projects may be public unless the user chooses private visibility. <br>
Mitigation: Use --privacy private for non-public work and review project visibility before sharing generated links. <br>
Risk: The v0 create command may time out after a project has already been created. <br>
Mitigation: Run v0 list and continue with the created chat ID before retrying creation. <br>


## Reference(s): <br>
- [v0.dev](https://v0.dev) <br>
- [v0 API keys](https://v0.dev/chat/settings/keys) <br>
- [ClawHub skill page](https://clawhub.ai/hlongvu/v0-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and CLI output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >= 18 and V0_API_KEY; created v0 projects may be public unless private visibility is selected.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
