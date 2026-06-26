## Description: <br>
Computes SHA-1 160-bit cryptographic hash values for file integrity checking and data fingerprinting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to calculate SHA-1 hashes for local files when checking integrity or creating data fingerprints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation describes piped input and -b/-t options, but the scanned implementation only hashes a file path or the default a.txt file. <br>
Mitigation: Run the skill with an explicit file path and do not rely on piped input or -b/-t behavior unless the skill is updated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/sha1-tool) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text hash output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a 40-character hexadecimal SHA-1 digest for the selected local file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
