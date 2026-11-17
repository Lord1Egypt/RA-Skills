## Description:

A Chinese-language pixel-art cultivation roguelike browser game with career choices, weapon evolution, realm progression, curse challenges, and an AI control interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[121212165](https://clawhub.ai/user/121212165)

### License/Terms of Use:

MIT-0

## Use Case:

External users can play the browser-based roguelike directly, while agent developers can inspect or use the exposed YinYangDAO interface to read game state and issue game actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Game progress and achievements are stored in browser local storage.

Mitigation: Use a trusted browser profile and clear the site's local storage when persistent game state should be removed.

Risk: The browser game loads a font from Google.

Mitigation: Allow the external font request only where policy permits, or self-host or remove the font before controlled deployment.

Risk: Broad trigger phrases may cause less precise activation.

Mitigation: Review and narrow the trigger phrases before installing the skill in shared agent environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/121212165/skills/yangyindao-rogue)
- [Game specification](artifact/SPEC.md)
- [AI game interface specification](artifact/AI_INTERFACE_SPEC.md)

## Skill Output:

**Output Type(s):** [Files, Code, Guidance]

**Output Format:** [HTML, JavaScript, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local browser game state and a window.YinYangDAO control interface.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
