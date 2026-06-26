## Description: <br>
Scrcpy Claw helps agents control Android devices through ADB and scrcpy, including touch and keyboard input, system operations, screen analysis, AI-assisted automation, and script recording/playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[italks](https://clawhub.ai/user/italks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to control connected Android devices, automate app testing or repetitive device workflows, inspect screens, and record or replay Android actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can broadly control a connected Android device, including touch input, keyboard entry, app launch or stop, clipboard operations, screen recording, and script playback. <br>
Mitigation: Install only when that level of Android device control is intentional; prefer a test device or test accounts, keep sensitive apps closed, and review planned actions before execution. <br>
Risk: Some supported actions can be sensitive or destructive, including messaging, form entry, clipboard paste, APK install, app uninstall, app data clearing, wireless ADB, screen recording, and replaying saved scripts. <br>
Mitigation: Require manual approval before those actions, verify the target device and package names, and avoid running saved playback scripts from untrusted sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/italks/scrcpy-claw) <br>
- [Publisher profile](https://clawhub.ai/user/italks) <br>
- [Scrcpy control commands reference](references/scrcpy-commands.md) <br>
- [scrcpy project](https://github.com/Genymobile/scrcpy) <br>
- [ADBKeyboard](https://github.com/senzhk/ADBKeyBoard) <br>
- [uiautomator2](https://github.com/openatx/uiautomator2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python examples, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also produce Android automation action sequences and JSON playback scripts when users invoke the bundled controllers.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
