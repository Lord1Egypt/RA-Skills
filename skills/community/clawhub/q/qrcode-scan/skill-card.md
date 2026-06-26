## Description: <br>
QR code scanning and generation. Invoke when user needs to scan/decode QR codes from images, generate QR codes (text, URL, WiFi), or mentions QR code related tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moxin1044](https://clawhub.ai/user/Moxin1044) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and external users use this skill to scan or decode QR codes from local files, image URLs, or Base64 image data, and to generate text, URL, and WiFi QR codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanning user-provided image URLs can fetch untrusted or internal network resources. <br>
Mitigation: Prefer local image files for sensitive QR codes and avoid scanning internal or untrusted URLs. <br>
Risk: WiFi QR handling can expose network names or passwords through command-line arguments, decoded output, or generated payloads. <br>
Mitigation: Avoid using real WiFi passwords in command-line arguments or printed output; handle sensitive WiFi QR data locally and only with trusted inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Moxin1044/qrcode-scan) <br>
- [python-qrcode](https://github.com/lincolnloop/python-qrcode) <br>
- [pyzbar](https://github.com/NaturalHistoryMuseum/pyzbar) <br>
- [pyzbar PyPI documentation](https://pypi.org/project/pyzbar/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with inline Python and shell examples; runtime outputs may be decoded text, JSON objects, PNG files, or Base64 PNG strings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return multiple decoded QR payloads and can parse or generate WiFi QR payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
