## Description: <br>
The reply ends mid-sentence or mid-code-block because the model hit a token limit or was cut short. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvogt99](https://clawhub.ai/user/mvogt99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to identify incomplete model replies before they are sent, recover from token-limit truncation, and communicate incomplete output clearly when recovery is not possible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regenerating truncated replies with higher token limits can increase cost or latency. <br>
Mitigation: Confirm truncation first, trim context where possible, and break large tasks into smaller turns before raising token limits. <br>
Risk: A reply may appear complete while still omitting final steps, closing code fences, or terminal punctuation. <br>
Mitigation: Check finish reasons, unmatched code fences, trailing lists, and sentence completion before sending the response. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mvogt99/truncated-output) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; no files, shell commands, persistence, credentials, or external access requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
