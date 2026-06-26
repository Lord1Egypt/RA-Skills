## Description: <br>
Runs a backend-backed live safety check for instructions that may trigger tool execution, external calls, file edits, permission changes, destructive or irreversible actions, prompt injection, or compliance-sensitive operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modeioai](https://clawhub.ai/user/modeioai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request a live safety decision before executing instructions with side effects, including destructive operations, permission changes, external calls, file edits, prompt-injection-sensitive work, or compliance-sensitive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operation descriptions may be sent to a remote safety service. <br>
Mitigation: Avoid including secrets, tokens, private customer data, or full sensitive URLs in input, context, or target fields. <br>
Risk: A SAFETY_API_URL override can redirect safety checks to an unexpected backend. <br>
Mitigation: Verify any SAFETY_API_URL override before use and configure only trusted safety endpoints. <br>
Risk: Network, dependency, API, or blocking-decision results can leave the caller without an approval to proceed. <br>
Mitigation: Configure callers not to proceed silently when the check errors or returns a blocking decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modeioai/security-modeio) <br>
- [Skill homepage](https://github.com/mode-io/mode-io-skills/tree/main/security) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and machine-readable JSON envelopes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Success envelopes include success/tool/mode/data; error envelopes include success/tool/mode/error.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
