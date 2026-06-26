## Description: <br>
Browser-based song creation with Suno, including gathering a song brief, generating lyrics, setting Persona/Custom mode, and producing new tracks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[machinesbefree](https://clawhub.ai/user/machinesbefree) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to create songs in Suno through a browser session by collecting a song brief, preparing lyrics and style tags, generating tracks, and sharing resulting links or files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may send song prompts, lyrics, personas, titles, and style tags to Suno under the user's account. <br>
Mitigation: Review creative inputs before generation and use an appropriate Suno account and browser session. <br>
Risk: The bundled workflow includes a hard-coded Anchor Protocol example that may not match the user's requested song. <br>
Mitigation: Treat the Anchor Protocol values as an example only and replace them with the user's confirmed brief, persona, title, lyrics, and style tags. <br>


## Reference(s): <br>
- [Suno Browser Workflow](references/suno-workflow.md) <br>
- [Suno](https://suno.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown guidance with song titles, lyrics, style tags, browser steps, and resulting Suno links or file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser automation steps and user-provided creative inputs intended for Suno.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
