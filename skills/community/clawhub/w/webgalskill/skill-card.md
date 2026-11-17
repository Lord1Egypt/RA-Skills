## Description:

WebGAL Skill 助手 helps creators write, check, and optimize WebGAL visual novel scripts using command syntax, variable logic, scene flow, and presentation controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenruyan](https://clawhub.ai/user/zhenruyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and visual novel creators use this skill to draft, debug, and refine WebGAL scripts for dialogue, assets, variables, branching, audio, video, animation, and visual effects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scripts can affect player experience or saved game state through user input, global variables, or configuration changes.

Mitigation: Review generated WebGAL scripts before publishing and test commands that use getUserInput, -global variables, or config values.

Risk: Scene jumps, calls, and branches can unintentionally preserve stage state such as backgrounds, figures, or audio.

Mitigation: Test each branch and explicitly clear or replace inherited stage elements when moving between scenes.

Risk: Non-skippable videos can block or frustrate players if used unintentionally.

Mitigation: Confirm each playVideo command that uses -skipOff is deliberate and appropriate for the release.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/zhenruyan/skills/webgalskill)
- [Base commands](references/base.md)
- [Dialogue](references/dialogue.md)
- [Backgrounds and figures](references/bg-and-figure.md)
- [Scenes and branching](references/scenes.md)
- [Variables](references/variable.md)
- [Audio](references/audio.md)
- [Video](references/video.md)
- [Animation](references/animation.md)
- [Special effects](references/special-effect.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown responses with WebGAL script code blocks and concise explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WebGAL ws code blocks, syntax checks, and workflow recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
