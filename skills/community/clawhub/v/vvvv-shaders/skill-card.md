## Description:

Helps agents write and debug SDSL shaders for Stride and vvvv gamma, including TextureFX, shader mixins, compute shaders, ShaderFX composition, and related HLSL work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tebjan](https://clawhub.ai/user/tebjan)

### License/Terms of Use:

CC-BY-SA-4.0

## Use Case:

Developers and coding agents use this skill when creating or debugging .sdsl shader files for vvvv gamma and Stride. It provides shader-language patterns, syntax rules, mixin guidance, compute and draw shader examples, and practical GPU safety checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad shader or compute discussions when vvvv context is present.

Mitigation: Use it for vvvv gamma or Stride shader work, and confirm generated shader guidance against the target runtime and compiler.

Risk: Generated shader examples may introduce visual artifacts, compilation failures, or GPU performance issues if applied without review.

Mitigation: Review generated SDSL/HLSL changes, compile them in the target project, and test representative inputs before release.

## Reference(s):

- [SDSL Syntax Rules and Gotchas](artifact/syntax-rules.md)
- [ClawHub skill page](https://clawhub.ai/tebjan/skills/vvvv-shaders)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with inline SDSL, HLSL, and C# code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include shader snippets, syntax corrections, implementation patterns, and debugging guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
