## Description: <br>
Remote Install automates Windows software installation by detecting installer packages and using silent or GUI-driven installation flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[403914291](https://clawhub.ai/user/403914291) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT operators, and support agents use this skill to find Windows installer packages, choose an installation path, automate installer dialogs, and return installation result summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control Windows installers and RustDesk sessions, creating high-impact remote-control and software-installation actions. <br>
Mitigation: Use only with explicit authorization, confirm each installer path before execution, and restrict execution to trusted Windows hosts. <br>
Risk: The security guidance notes password logging in the remote-access flow. <br>
Mitigation: Remove password logging before use and avoid storing remote-access credentials in installer logs. <br>
Risk: Broad auto-installing from common folders can execute unintended packages. <br>
Mitigation: Prefer explicit package paths, review detected installers, and install only trusted signed installers. <br>
Risk: Dependency versions are specified as lower bounds rather than reviewed pinned versions. <br>
Mitigation: Pin reviewed dependency versions before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/403914291/remote-install) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON result summaries with command-line arguments and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installer counts, per-package success or failure messages, optional remote ID and package path fields, and configurable timeout, retry, and UI button settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
