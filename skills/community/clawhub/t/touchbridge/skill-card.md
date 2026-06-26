## Description: <br>
Authenticate sudo and macOS system prompts using your phone's biometric (Face ID/fingerprint) instead of typing passwords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmakt99](https://clawhub.ai/user/hmakt99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install, configure, test, and operate TouchBridge so macOS sudo and system authentication prompts can be approved from a phone, watch, browser, or terminal instead of a typed password. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides installation of third-party software into the macOS sudo and authentication path. <br>
Mitigation: Install only when the project and package provenance are intentionally trusted, and confirm how to restore the original PAM configuration before relying on it. <br>
Risk: Simulator mode auto-approves authentication and is not suitable for real security use. <br>
Mitigation: Use simulator mode only in controlled testing, then switch to paired-device production approval for normal use. <br>
Risk: Browser URL approval may be less controlled than paired-device approval. <br>
Mitigation: Prefer paired-device production approval over browser URL approval where possible. <br>


## Reference(s): <br>
- [TouchBridge setup reference](references/setup.md) <br>
- [TouchBridge project homepage](https://github.com/HMAKT99/UnTouchID) <br>
- [Install TouchBridge package](https://github.com/HMAKT99/UnTouchID/releases/download/v0.1.0-alpha/TouchBridge-0.1.0.pkg) <br>
- [ClawHub skill page](https://clawhub.ai/hmakt99/touchbridge) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the touchbridged and touchbridge-test binaries for the documented workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
