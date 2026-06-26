## Description: <br>
Standard SAPCONET SSH command templates for bird reads, Puppeteer runs, and inbox messaging workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Highlander89](https://clawhub.ai/user/Highlander89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare SSH-based SAPCONET command patterns for connectivity checks, bird reads, Puppeteer prerequisite checks, and inbox messaging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill initiates SSH sessions to SAPCONET and includes a documented default target. <br>
Mitigation: Confirm the SSH target and account before execution, and set SAPCONET_TARGET explicitly for the intended environment. <br>
Risk: The inbox message script can allow crafted message text to run unintended commands on the remote host. <br>
Mitigation: Before using scripts/msg-sapconet.sh with real content, pass message text safely, such as through stdin or a properly quoted remote argument. <br>
Risk: The included remote commands are placeholders for operational workflows. <br>
Mitigation: Review and replace placeholders with the intended SAPCONET commands before running the scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Highlander89/sapconet-ssh-bridge) <br>
- [Publisher profile](https://clawhub.ai/user/Highlander89) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill provides command templates and operator guidance; users must supply the intended SAPCONET target and replace placeholders before real use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
