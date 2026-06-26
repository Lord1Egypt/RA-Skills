## Description: <br>
Generate and read QR codes. Use when the user wants to create a QR code from text/URL, or decode/read a QR code from an image file. Supports PNG/JPG output and can read QR codes from screenshots or image files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Omar-Khaleel](https://clawhub.ai/user/Omar-Khaleel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users can use this skill to create QR codes from text or URLs and decode QR codes from image files or screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing dependencies from untrusted sources could introduce package risk. <br>
Mitigation: Install dependencies from trusted package repositories, preferably in a virtual environment. <br>
Risk: Generated QR output paths may overwrite existing files. <br>
Mitigation: Choose output paths carefully before running QR generation. <br>
Risk: Decoded QR payloads may contain links or text that should not be trusted automatically. <br>
Mitigation: Verify decoded QR links or text before opening or acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Omar-Khaleel/qr-code) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Files, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; generated image files or decoded text/JSON when scripts run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated QR codes are saved as image files; decoded QR results can be plain text or JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
