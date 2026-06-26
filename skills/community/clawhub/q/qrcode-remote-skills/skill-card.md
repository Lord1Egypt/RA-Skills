## Description: <br>
Generate and decode QR codes using the CaoLiao QR Code API when a user wants to create a QR code from text or a URL, read QR code content from an image, or work with QR code generation and scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiNISAL](https://clawhub.ai/user/hiNISAL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate QR code links or image files, decode QR code content from image URLs or local files, and run batch QR code generation or decoding workflows over Excel, CSV, or TXT inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR contents, image URLs, or fallback-decoded local images may be sent to the third-party CaoLiao QR API. <br>
Mitigation: Avoid using the skill with secrets, private links, internal URLs, personal data, regulated documents, or other content that should not be sent to api.2dcode.biz. <br>
Risk: Batch decoding can write decoded results back into the original spreadsheet or CSV input. <br>
Mitigation: Back up batch input files before decoding, and use a separate TXT output when a non-mutating workflow is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hiNISAL/qrcode-remote-skills) <br>
- [CaoLiao QR Code API documentation](https://cli.im/open-api/qrcode-api/quick-start.html) <br>
- [QR Code API reference](artifact/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown responses with QR image links, shell commands, JSON script results, and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local QR image, TXT, or ZIP files and may write batch decode results back into spreadsheet or CSV inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
