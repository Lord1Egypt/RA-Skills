## Description: <br>
Displays the last lines of local files or stdin for checking recent log and text-file entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Tail Tool to inspect the most recent lines from a local file or stdin when checking logs and text output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reading sensitive files can expose secrets, private logs, or credential material to the agent context. <br>
Mitigation: Only point the skill at files whose recent lines are appropriate for the current agent session. <br>
Risk: The documentation mentions follow, byte-count, quiet, and multi-file behavior that the implementation does not support. <br>
Mitigation: Use the supported local file or stdin line-tail behavior unless the implementation is updated. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/tail-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and concise Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads from a selected local file or stdin and emits the requested last lines; default is 10 lines.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
