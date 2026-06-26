## Description: <br>
Surgical quick-fix workflow for small bugs, typos, and simple changes that uses a read-diagnose-fix-verify loop with at most five tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NakedoShadow](https://clawhub.ai/user/NakedoShadow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill for small, clearly defined code fixes when the target file or bug is already known and the expected change is minimal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification commands or local tests may execute project code. <br>
Mitigation: Run verification only in trusted repositories, or skip or sandbox those checks for untrusted code. <br>
Risk: A narrowly scoped quick fix can still introduce an incorrect code change. <br>
Mitigation: Review the generated diff after use and reserve the skill for small fixes where the target file or bug is known. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/NakedoShadow/shadows-oneshot-fix) <br>
- [Publisher profile](https://clawhub.ai/NakedoShadow) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown status with existing-file code edits and verification results when checks are available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limited to small targeted fixes; reports the fixed file, change, and verification result.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
