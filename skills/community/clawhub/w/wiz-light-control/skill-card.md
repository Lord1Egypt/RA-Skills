## Description: <br>
Controls Wiz smart bulbs (turn on/off, RGB colors, disco mode) via local WiFi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Canbirlik](https://clawhub.ai/user/Canbirlik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate Wiz smart bulbs on the user's local WiFi network, including power, RGB color, and timed disco-mode changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change physical lighting state on the local network, including on/off and disco actions. <br>
Mitigation: Use explicit prompts with the intended device name and bulb IP address, and confirm disruptive actions before execution. <br>
Risk: An incorrect bulb IP address can cause failed control attempts or target the wrong local device. <br>
Mitigation: Verify the actual local Wiz bulb IP address before running commands instead of relying on placeholder examples. <br>
Risk: Disco mode can run longer than intended if given an unsuitable duration. <br>
Mitigation: Use a positive, limited duration for disco mode. <br>
Risk: The dependency is unpinned, which can introduce unexpected package changes in security-sensitive environments. <br>
Mitigation: Pin the pywizlight package version where reproducibility or stricter dependency control is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Canbirlik/wiz-light-control) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require a local Wiz bulb IP address and the pywizlight Python package.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
