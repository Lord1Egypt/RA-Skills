## Description: <br>
Password Manager helps an agent guide password storage, random password generation, autofill, strength checks, and password leak checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to work with password-manager workflows such as generating passwords, storing credentials, retrieving saved credentials, checking password strength, and understanding password safety practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive credentials, and evidence does not fully explain storage, master-password, or encryption-key behavior. <br>
Mitigation: Review storage and key-management behavior before using real passwords, and test with non-sensitive credentials first. <br>
Risk: Leak checks, cloud sync, or autofill may expose credential-derived data or fill secrets without sufficient user confirmation. <br>
Mitigation: Confirm any external data sharing and require explicit user approval before autofill, leak-check, or sync actions. <br>
Risk: Passing real passwords as command-line arguments can expose them through shell history or process listings. <br>
Mitigation: Avoid entering real passwords directly as command-line arguments; prefer interactive secret input or a reviewed secure storage flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/xiaoming-password-manager) <br>
- [Publisher profile](https://clawhub.ai/user/kaising-openclaw1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include credential-handling guidance; avoid placing real passwords directly in command-line arguments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
