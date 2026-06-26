## Description: <br>
Control Windows desktop software, system hardware, serial devices, IoT endpoints, and GUI automation through standalone CLI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to let an agent inspect and control Windows applications, processes, system settings, serial devices, smart-home APIs, and GUI workflows after appropriate confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control desktop windows, processes, power state, network adapters, serial devices, and smart-home/API endpoints. <br>
Mitigation: Install only when this broad control is intended, list or inspect targets before acting, and require explicit confirmation before shutdown, restart, sleep, process or window closing, network changes, POST/PUT/API service calls, and GUI typing or clicking. <br>
Risk: Screenshots, OCR, GUI typing, and API commands can expose sensitive data or affect the wrong on-screen target. <br>
Mitigation: Hide sensitive windows before screenshots or OCR, take a screenshot first when the target is uncertain, and avoid placing long-lived tokens in command lines or transcripts. <br>
Risk: Several scripts can automatically install Python dependencies at first use. <br>
Mitigation: Preinstall and review dependencies in the managed environment instead of relying on automatic installation during agent operation. <br>


## Reference(s): <br>
- [Windows System Controller - Command Reference](references/command_reference.md) <br>
- [System Controller ClawHub release page](https://clawhub.ai/wangjiaocheng/system-controller) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with command examples and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets Windows 10/11 and may rely on optional local dependencies for serial, GUI, OCR, and precise volume control.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
