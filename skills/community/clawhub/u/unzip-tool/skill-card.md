## Description: <br>
List, test, and extract files from ZIP archives. Use when you need to decompress or inspect ZIP file contents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect or extract ZIP archives during local file workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracting ZIP archives writes files locally and can overwrite existing paths. <br>
Mitigation: Extract only trusted archives into a new empty directory and review the extracted files before use. <br>
Risk: Documented list, test, and non-overwrite options may not be supported by the current implementation. <br>
Mitigation: Confirm supported arguments before use and use another ZIP tool for list, test, or non-overwrite workflows until the implementation is updated. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands] <br>
**Output Format:** [Extracted archive files plus plain-text status or error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local filesystem output; no network or credential behavior is reported by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
