## Description: <br>
Automates Quark Drive file operations, including QR-code login, list and search, upload, share-link creation, and saving external shared links into an allowlisted drive folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StNJJJJJ](https://clawhub.ai/user/StNJJJJJ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to operate a linked Quark Drive account from an agent workflow while keeping file activity scoped to configured local and remote allowlists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain ongoing access to the linked Quark Drive account through session, cookie, and token files. <br>
Mitigation: Install only for accounts where this access is acceptable, keep generated credential files private, and rotate or delete sessions when access should end. <br>
Risk: Some cloud-file mutations may run without the confirmation behavior promised by the skill documentation. <br>
Mitigation: Manually confirm rename and move intent before execution, and review command output until confirmation behavior is enforced consistently. <br>
Risk: Broad local or remote allowlists could expose or modify more files than intended. <br>
Mitigation: Configure a narrow references/config.json before use and keep operations under the intended Quark Drive folder and approved local upload paths. <br>
Risk: Share links can expose files outside the immediate agent session. <br>
Mitigation: Set expiry and passcodes intentionally, and verify the selected file or folder before creating a share link. <br>


## Reference(s): <br>
- [Configuration example](references/config.example.json) <br>
- [Quark Netdisk ClawHub page](https://clawhub.ai/StNJJJJJ/quark-netdisk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON status responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce QR-code PNG files, session files, share links, and machine-readable interaction codes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
