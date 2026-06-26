## Description: <br>
Send images, videos, audio, or documents through WhatsApp by downloading the file, copying it into the OpenClaw workspace, sending it with the WhatsApp message tool, and cleaning up the temporary copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seekeyl](https://clawhub.ai/user/seekeyl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents assisting users who want to send media or documents over WhatsApp use this skill to stage a file in the workspace, send it to a specified phone number with an optional caption, and remove temporary files afterward. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted URLs or unusual filenames could place unwanted files in the workspace before sending. <br>
Mitigation: Confirm the URL or source file and filename before downloading, and avoid untrusted sources. <br>
Risk: Media or documents could be sent to the wrong WhatsApp recipient or include sensitive content. <br>
Mitigation: Confirm the recipient phone number, caption, and file before sending, then remove temporary workspace copies when the media is sensitive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/seekeyl/whatsapp-image-send) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with shell commands and message command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation of the file source, recipient phone number, caption, and filename before sending.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
