## Description: <br>
The official Skill Base CLI client helps agents use the `skb` command to search, install, update, publish, import from GitHub, and configure skills from Skill Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ginuim](https://clawhub.ai/user/ginuim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they need an assistant to run Skill Base CLI commands for skill search, installation, updates, publishing, imports, authentication, and endpoint configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill installation, update, publish, import, and global npm commands can change local skill files, account state, or configured Skill Base endpoints. <br>
Mitigation: Confirm the target skill, target directory, account, and `SKB_BASE_URL` before running commands that modify local files or remote Skill Base state. <br>
Risk: Login verification codes and resulting tokens provide access to Skill Base operations. <br>
Mitigation: Treat login verification codes and tokens as sensitive and keep them within the local login flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ginuim/skill-base-cli) <br>
- [Publisher profile](https://clawhub.ai/user/ginuim) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute or propose Skill Base CLI commands and summarize command results for the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
