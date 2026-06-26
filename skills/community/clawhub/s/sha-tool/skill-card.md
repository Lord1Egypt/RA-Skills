## Description: <br>
Compute SHA family hash values for file integrity verification. Use for checksums, data validation, and security verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security reviewers use this skill to compute SHA checksums for files or text input and compare them with trusted expected hashes for integrity checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A checksum only supports integrity verification when the expected digest comes from a trusted source. <br>
Mitigation: Compare generated hashes against publisher-provided or otherwise trusted digests, not values from the same untrusted channel as the file. <br>
Risk: SHA-1 is available for legacy checks but is weak for security-sensitive collision resistance. <br>
Mitigation: Use SHA-256 or SHA-512 for new verification workflows unless a legacy process explicitly requires SHA-1. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain hexadecimal hash strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SHA digest values for supplied files or stdin; users must provide any expected digest for comparison.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
