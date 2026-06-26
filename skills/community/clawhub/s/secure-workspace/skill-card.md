## Description: <br>
Encrypts API keys, tokens, and passwords with age to protect workspace secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asistentegordito](https://clawhub.ai/user/asistentegordito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Secure Workspace to create age keys and encrypt or decrypt workspace secret files for local repositories and backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local private age key can decrypt protected workspace secrets if it is exposed. <br>
Mitigation: Protect the private key carefully, keep it out of repositories and backups that do not require it, and restrict file access to trusted users. <br>
Risk: Sourcing decrypted secrets can expose values in shared shells, logs, CI steps, or sessions that later run untrusted commands. <br>
Mitigation: Decrypt or source secrets only in trusted local sessions and avoid printing, logging, or reusing decrypted values in shared automation. <br>
Risk: Encryption and decryption depend on the expected local age key path and can fail or use the wrong key if setup is skipped or inconsistent. <br>
Mitigation: Run setup first, verify the helper scripts use the intended key path, and test decryption before relying on encrypted secret files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asistentegordito/secure-workspace) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the age CLI and a local age key file before encryption or decryption.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
