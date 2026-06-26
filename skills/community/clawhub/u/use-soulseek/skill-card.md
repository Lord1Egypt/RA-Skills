## Description: <br>
Use Soulseek to search, download, and share files, and chat in rooms or privately through GUI or CLI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[svidovich](https://clawhub.ai/user/svidovich) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and users can use this skill to set up Soulseek, search and download files, share selected directories, and communicate with other users through chat rooms or private messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Peer-to-peer sharing and downloads involve untrusted peers, chat messages, and files. <br>
Mitigation: Treat peers, messages, and downloaded files as untrusted, and review or scan files before opening or relying on them. <br>
Risk: Soulseek account credentials can be exposed if reusable passwords are stored in shell history or shared environments. <br>
Mitigation: Use a dedicated Soulseek account and password, and avoid putting reusable credentials in shell history. <br>
Risk: Sharing the wrong directory can expose personal or sensitive data. <br>
Mitigation: Share only an empty or dedicated non-sensitive folder, and review sharing settings before connecting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/svidovich/use-soulseek) <br>
- [Soulseek downloads](https://www.slsknet.org/news/node/1) <br>
- [soulseek-cli](https://github.com/aeyoll/soulseek-cli) <br>
- [aioslsk](https://github.com/JurgenR/aioslsk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and external reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; users choose platform-specific GUI, CLI, or library-based workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
