## Description: <br>
Provides guidance and shell commands for encrypting or decrypting text and files with a local Node.js implementation of the Pieter Theijssen triple-layer XOR format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theijssenp](https://clawhub.ai/user/theijssenp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other users can use this skill to generate commands and guidance for encrypting or decrypting local messages or files with a shared key file. It is not appropriate for high-value secrets where vetted cryptographic tooling is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports weak custom cryptography and incomplete safeguards for sensitive data. <br>
Mitigation: Use this only after review; prefer vetted encryption tools such as age, OpenPGP, or libsodium-based tooling for confidential or high-value secrets. <br>
Risk: Key files and decrypted outputs can expose sensitive content if stored or shared carelessly. <br>
Mitigation: Manage key files out of band, protect local outputs, and avoid sending keys over the same channel as encrypted messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/theijssenp/secure-communicator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/theijssenp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text, Files] <br>
**Output Format:** [Markdown with inline bash commands and generated command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files and requires node and openssl according to ClawHub metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
