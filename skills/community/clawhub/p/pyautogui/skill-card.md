## Description:

Cross-platform mouse/keyboard automation skill that supports mouse control, keyboard input, screenshots, region screenshots, image utilities, screen and image markers, template/OCR locating, clipboard automation, and cleanup of generated image files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ikaros-521](https://clawhub.ai/user/ikaros-521)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to inspect screen state, calibrate coordinates, control mouse and keyboard actions, locate UI elements by template or OCR, and manage generated screenshots or annotated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can click, type, paste, and invoke hotkeys in active desktop applications.

Mitigation: Use it only for explicit UI automation tasks; verify the focused window, target coordinates, and expected action before execution, and keep PyAutoGUI failsafe behavior available.

Risk: Screenshots, OCR, and clipboard operations can expose sensitive on-screen or copied content.

Mitigation: Avoid using the skill over sensitive windows, do not include real passwords or secrets in prompts or examples, and review captured or recognized content before sharing it.

Risk: Template or OCR matches can identify the wrong UI target, especially when automatic clicking is enabled.

Mitigation: Review matches with screen overlays or marked images before using click actions, and avoid automatic click flags unless the target has been visually confirmed.

Risk: Cleanup commands can delete generated image files in selected directories.

Mitigation: Run cleanup only in directories containing disposable generated screenshots or marked images, preview clean operations first, and use custom patterns carefully.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ikaros-521/skills/pyautogui)
- [Publisher profile](https://clawhub.ai/user/ikaros-521)
- [requirements.txt](references/requirements.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance, files]

**Output Format:** [Markdown instructions with inline shell commands plus text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, cropped regions, annotated images, temporary OCR/template matching files, and cleanup reports.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
