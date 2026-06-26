## Description: <br>
Download files from Tailscale Taildrop inbox to local storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cortexuvula](https://clawhub.ai/user/cortexuvula) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Tailscale users use Taildrop to retrieve files sent to a Linux machine through Tailscale Taildrop and save them locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom destination paths can trigger command injection in the helper script when passed to the Tailscale command. <br>
Mitigation: Avoid custom destination paths until the helper replaces eval with safe argument handling; use the default Downloads target or review and patch the script before running. <br>
Risk: Tailscale operator access or sudo may be required, and loop mode continuously receives Taildrop files. <br>
Mitigation: Grant Tailscale operator access only to trusted local users and use loop mode only when continuous receiving is intended. <br>


## Reference(s): <br>
- [ClawHub Taildrop listing](https://clawhub.ai/cortexuvula/taildrop) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tailscale to be installed and running; file retrieval may require Tailscale operator access or sudo.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
