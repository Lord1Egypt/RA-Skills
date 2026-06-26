## Description: <br>
Generate cryptographically secure passwords, passphrases, and API keys. Supports multiple formats and entropy calculation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hostilespider](https://clawhub.ai/user/hostilespider) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users can use this skill to generate local passwords, passphrases, API keys, PINs, hex strings, and base64 strings with optional entropy display. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated passwords and API keys are sensitive and are printed to standard output. <br>
Mitigation: Avoid capturing generated values in logs, transcripts, shared terminals, or shell history; transfer them directly into an appropriate secret manager. <br>
Risk: Clipboard handling can expose secrets to other local software if added or used in a future version. <br>
Mitigation: Use clipboard features only in trusted local environments and clear clipboard contents after moving the secret into its intended store. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hostilespider/secure-passgen) <br>
- [Publisher profile](https://clawhub.ai/user/hostilespider) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text generated secrets and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated values are written to standard output; optional entropy display appends an estimated bit count.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
