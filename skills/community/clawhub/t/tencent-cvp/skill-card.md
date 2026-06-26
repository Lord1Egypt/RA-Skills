## Description: <br>
All-in-one Android phone automation via ADB: screen analysis, touch/input, foreground app detection, app install. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cobeizailin](https://clawhub.ai/user/cobeizailin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to observe and control a Tencent Cloud Virtual Phone through ADB, including UI inspection, touch and text input, foreground app detection, and app installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad ADB control can interact with sensitive apps, accounts, payment flows, messages, installs, and visible screen content. <br>
Mitigation: Keep sensitive apps and screens out of view, and require explicit approval before taps in accounts, payments, messaging, or install flows. <br>
Risk: The APK download fallback can lead to installing untrusted packages when source or package integrity is not verified. <br>
Mitigation: Prefer verified app-market or official sources, and avoid web APK downloads unless the source and package integrity can be verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cobeizailin/tencent-cvp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires adb on linux or darwin and access to a Tencent Cloud Virtual Phone or Android device.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
