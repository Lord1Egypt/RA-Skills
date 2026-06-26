## Description: <br>
Cache and reuse code from prior AI agent executions via Raysurfer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryx2](https://clawhub.ai/user/ryx2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding agents use this skill to search Raysurfer for cached code before implementing a task and to upload successfully executed code for future reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task descriptions and selected source files may be sent to a third-party Raysurfer service. <br>
Mitigation: Use only when the user is comfortable sharing the task and code; avoid private, regulated, customer, or secret-bearing code unless the upload has been reviewed. <br>
Risk: Remote cached or public snippets may be incorrect, insecure, or unsuitable for the current project. <br>
Mitigation: Treat retrieved snippets as untrusted code, review and adapt them before use, and run project tests before accepting the result. <br>


## Reference(s): <br>
- [Raysurfer API Reference](artifact/references/api-reference.md) <br>
- [Raysurfer API](https://api.raysurfer.com) <br>
- [Raysurfer API Key Dashboard](https://raysurfer.com/dashboard/api-keys) <br>
- [ClawHub Release Page](https://clawhub.ai/ryx2/raysurfer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RAYSURFER_API_KEY for API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
