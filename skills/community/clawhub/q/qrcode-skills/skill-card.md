## Description: <br>
Generate and decode QR codes locally. Use when the user wants to create a QR code from text/URL, decode/read QR code content from an image, or asks about QR code generation and scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiNISAL](https://clawhub.ai/user/hiNISAL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to generate QR code image files from text or URLs and to decode QR code content from local images or image URLs. It also supports batch generation and decoding workflows for CSV, Excel, and text inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Python or Node.js dependencies when required. <br>
Mitigation: Use an isolated environment and review dependency installation before running the skill in sensitive workspaces. <br>
Risk: The skill can download remote image URLs supplied for QR decoding. <br>
Mitigation: Decode only trusted URLs, and prefer local image files when handling sensitive or untrusted content. <br>
Risk: Batch decoding can write results back into the original CSV or XLSX input file. <br>
Mitigation: Run batch decode on copies of important spreadsheets or request separate TXT output when preserving the source file matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hiNISAL/qrcode-skills) <br>
- [qr-scanner-wechat decoder dependency](https://github.com/AntFu/qr-scanner-wechat) <br>
- [qrcode-remote-skills alternative remote workflow](https://github.com/caoliao/qrcode-remote-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown responses with JSON script results and local PNG, SVG, TXT, CSV, XLSX, or ZIP files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Python and Node.js script variants expose matching command parameters for single and batch QR code workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package.json reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
