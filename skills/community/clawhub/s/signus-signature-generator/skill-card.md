## Description: <br>
Generate signature images via the Signus API and return image files for chat delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[signus-ai](https://clawhub.ai/user/signus-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request font-based signature images from Signus using a name, first and last name, or initials, then receive generated image files for chat delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The requested signature name or initials are sent to Signus. <br>
Mitigation: Install and use only when users are comfortable sharing that identity data with Signus. <br>
Risk: The file-writing boundary is weaker than disclosed. <br>
Mitigation: Review path containment, filename sanitization, ZIP entry validation, and response size limits before broad use. <br>
Risk: Generated files are stored locally. <br>
Mitigation: Review local storage location and retention expectations for ~/.openclaw/media/signatures-font/. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/signus-ai/signus-signature-generator) <br>
- [Signus API host](https://api.signus.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, API Calls, Shell commands] <br>
**Output Format:** [JSON status object with local image file paths and chat-delivered signature images] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and writes generated signature files under ~/.openclaw/media/signatures-font/.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
