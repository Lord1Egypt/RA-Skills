## Description: <br>
Provides guidance and sample Python code for classifying tool commands by access tier and identifying operations that should require approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review tool execution plans, classify commands into read, write, delete, or dangerous tiers, and document when human approval should be required before risky operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may overstate its safety protections; the artifact appears to classify commands but does not implement a complete fail-closed approval or blocking layer. <br>
Mitigation: Review behavior before installing, and do not rely on it as a protection layer for destructive or privileged commands unless approval, blocking, argument validation, and fail-closed tests are implemented. <br>
Risk: The release has unexplained high-impact capability metadata for wallet access, transaction signing, and sensitive credentials. <br>
Mitigation: Resolve or remove the unexplained capability metadata before using the skill in any sensitive environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/safe-tool-executor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands] <br>
**Output Format:** [Markdown guidance with Python examples and text or JSON-like status output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command tier and approval-required labels; does not provide a verified enforcement boundary by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
