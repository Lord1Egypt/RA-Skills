## Description: <br>
Encrypt API keys, tokens and passwords with age to protect secrets in your workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asistentegordito](https://clawhub.ai/user/asistentegordito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Secure Workspace to generate an age key pair, encrypt workspace secrets into .age files, and decrypt or source those secrets when needed for local development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive local secret files and depends on an age private key. <br>
Mitigation: Protect the private key, restrict access to local secret files, and install only if local secret-key management is acceptable. <br>
Risk: Decrypted secrets may be sourced into a shell and remain available longer than intended. <br>
Mitigation: Source decrypted secrets only when needed, avoid long-lived shells for sensitive environments, and clear related environment variables afterward. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asistentegordito/secure-workspace-en) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include commands that create, read, encrypt, decrypt, and source local secret files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
