## Description: <br>
Provides Chinese-language Unity HLSL shader style guidance for reducing duplicate code, extracting shared functions, and organizing shared include files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joashchou](https://clawhub.ai/user/joashchou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Unity shader developers and agents use this skill to review, refactor, or generate HLSL and ShaderLab code that follows DRY patterns, separates common functions and CBUFFER definitions into includes, preserves line-ending consistency, and avoids common URP structure and sampling mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated shader refactors may introduce incorrect behavior when splitting files, adding includes, or normalizing line endings. <br>
Mitigation: Review generated shader changes before accepting them and test the affected Unity materials or render paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joashchou/unity-shader-optimizer-llm-cleaner) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HLSL and ShaderLab code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; users should review generated shader edits before applying them.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
