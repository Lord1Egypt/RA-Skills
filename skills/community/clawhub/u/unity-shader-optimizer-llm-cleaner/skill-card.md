## Description:

Unity HLSL Shader code style guidance for reducing duplicate code, extracting shared functions, organizing reusable header files, and cleaning LLM-generated shader output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joashchou](https://clawhub.ai/user/joashchou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and shader engineers use this skill when writing, reviewing, or refactoring Unity HLSL and URP ShaderLab code. It helps agents remove duplicated shader logic, extract shared functions and material buffers, preserve valid ShaderLab structure, and apply project line-ending guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill strongly favors DRY refactors, which can split shader logic across additional include files and change project file organization.

Mitigation: Review proposed shader file structure and include paths against the Unity project before applying changes.

Risk: The skill recommends Windows CRLF line endings for Unity shader files, which may conflict with repositories that standardize on LF.

Mitigation: Confirm the repository line-ending policy and normalize generated shader files to the project convention.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joashchou/skills/unity-shader-optimizer-llm-cleaner)
- [Publisher profile](https://clawhub.ai/user/joashchou)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with HLSL and ShaderLab code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend shader file organization, reusable HLSL includes, ShaderLab structure corrections, URP texture sampling macros, and line-ending conventions.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
