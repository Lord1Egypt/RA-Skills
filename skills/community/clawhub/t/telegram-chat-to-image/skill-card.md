## Description: <br>
Convert Telegram chat exports into a long screenshot-style image with bubble-style message rendering, avatars, timestamps, and text wrapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reetyo](https://clawhub.ai/user/reetyo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to convert local Telegram Desktop JSON chat exports into shareable screenshot-style PNG images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram chat exports and generated images may contain sensitive conversation records. <br>
Mitigation: Review and redact the JSON input and generated PNG or ZIP before sharing. <br>
Risk: Long generated images can become blurry if Telegram compresses them as images. <br>
Mitigation: Package long PNG outputs as ZIP files or use message limits before sending. <br>
Risk: The skill depends on Pillow in the local Python environment. <br>
Mitigation: Install Pillow only from a trusted Python package environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reetyo/telegram-chat-to-image) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated artifact is a PNG image file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes Telegram Desktop JSON exports locally; supports message limits, custom fonts, width selection, and HD image scaling.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
