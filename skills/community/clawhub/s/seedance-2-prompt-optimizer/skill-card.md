## Description: <br>
Helps agents gather user intent and produce structured Seedance 2.0 video generation prompts using guidance for styles, camera language, prompt structure, and common generation issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wfhiew](https://clawhub.ai/user/wfhiew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to turn natural-language video ideas into structured Seedance 2.0 prompts, including shot planning, reference-asset mapping, audio cues, negative constraints, and generation settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may reference user-supplied media that could be private or rights-sensitive when used with a third-party video generation platform. <br>
Mitigation: Use only media that the user is comfortable sending to that platform and has the right to use. <br>
Risk: Watermark-related prompt guidance can be misused if interpreted as bypassing platform policy or ownership controls. <br>
Mitigation: Apply watermark guidance only through official platform controls, support channels, or legitimate cleanup of assets the user is authorized to use. <br>


## Reference(s): <br>
- [Prompt Best Practices - Seedance 2.0](artifact/best-practices.md) <br>
- [Camera Angles & Movement Reference - Seedance 2.0](artifact/camera-angles.md) <br>
- [Common Issues & Workarounds - Seedance 2.0](artifact/common-issues.md) <br>
- [Visual Styles Reference - Seedance 2.0](artifact/styles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown prompt template with structured sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include mode, asset mapping, subject definitions, shot-by-shot prompt text, dialogue or audio cues, negative constraints, generation settings, and known issues to watch.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
