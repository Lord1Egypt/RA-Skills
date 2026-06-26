## Description: <br>
Valuation is a local shell utility for logging, viewing, searching, and exporting valuation-related activity records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agents can use this skill to record and review local notes about valuation runs, checks, analyses, configuration changes, and reports. Treat it as a plaintext activity log, not as a valuation modeler. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may rely on the skill as a valuation modeler even though the reviewed artifacts show only local logging and export behavior. <br>
Mitigation: Use it only to record and retrieve valuation-related notes; perform valuation calculations and financial review in separate validated tools. <br>
Risk: Sensitive financial notes may be persisted in plaintext local files. <br>
Mitigation: Avoid entering confidential or regulated information unless the local data directory is approved, access-controlled, and managed according to the user's data-handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/valuation) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; the utility writes plaintext log and export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries locally under ~/.local/share/valuation by default; VALUATION_DIR can override the data directory.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
