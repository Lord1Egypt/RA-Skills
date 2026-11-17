## Description: <br>
WhatsApp图片发送-免费版 helps agents send a single JPG, PNG, or GIF image with an optional caption to a specified WhatsApp recipient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to share one image with a WhatsApp contact, including lightweight personal sharing, screenshots, previews, and feedback images. It is not intended for bulk sending, documents, video, audio, media conversion, scheduled messages, or group messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Overbroad trigger instructions may route unrelated video, audio, media conversion, or document-sharing requests into a WhatsApp sending workflow. <br>
Mitigation: Use the skill only for explicit single-image requests involving JPG, PNG, or GIF files, and decline video, audio, document, bulk-send, dubbing, conversion, or ambiguous file-sharing requests. <br>
Risk: The workflow sends content through WhatsApp and may copy files into the platform workspace. <br>
Mitigation: Confirm the exact image, caption, and recipient phone number before sending, avoid sensitive media unless explicitly approved, and clean temporary and workspace copies after completion. <br>
Risk: Incorrect recipient details can send an image to the wrong WhatsApp contact. <br>
Mitigation: Require a recipient phone number with country code and a final confirmation of the recipient, file, and caption before executing the send command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/whatsapp-image-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON-like status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for sending one supported image file and confirming send status.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
