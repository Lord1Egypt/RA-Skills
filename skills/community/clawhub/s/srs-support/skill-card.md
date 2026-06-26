## Description: <br>
Answer SRS (Simple Realtime Server) questions for users and operators about protocols, configuration, codecs, ecosystem tools, deployment, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winlinvip](https://clawhub.ai/user/winlinvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operators, DevOps teams, and developers use this skill to get practical SRS deployment, configuration, monitoring, protocol, codec, and troubleshooting guidance grounded in a trusted local SRS checkout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest build, firewall, curl, nc, FFmpeg, or configuration commands for SRS operations. <br>
Mitigation: Review suggested commands and configuration changes before running them, especially on production systems. <br>
Risk: Answers depend on the local SRS documentation, memory files, and source checkout being trustworthy and current. <br>
Mitigation: Use the skill with a trusted SRS checkout and keep referenced documentation and memory files under review. <br>


## Reference(s): <br>
- [SRS Support release page](https://clawhub.ai/winlinvip/srs-support) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [evals.json](artifact/evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, URLs, configuration snippets, and concise troubleshooting steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Grounds answers in local SRS docs and source context; may ask for logs, configuration, network details, or version information before troubleshooting.] <br>

## Skill Version(s): <br>
1.0.7 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
