## Description: <br>
Create and manage short URLs with custom aliases and tracking, including click statistics and QR code generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users can use this skill to create local short aliases for long URLs, list saved URLs, inspect simulated click counts, and generate QR codes for sharing links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shortened URL records are stored locally in plaintext in the user's home directory. <br>
Mitigation: Avoid storing sensitive private links unless plaintext local storage is acceptable. <br>
Risk: The skill creates local aliases and does not appear to create hosted public short links. <br>
Mitigation: Confirm the expected sharing model before relying on generated aliases outside the local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/url-shortener) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON records in the user's home directory and optional QR code image files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
