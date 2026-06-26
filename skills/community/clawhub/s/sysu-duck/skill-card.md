## Description: <br>
SYSU Duck is a Sun Yat-sen University campus companion skill for duck-themed profiles, personality modes, campus Q&A memory, and CLI-driven commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars2003](https://clawhub.ai/user/mars2003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and campus community members use this skill to manage a personalized SYSU companion persona, answer campus questions, and preserve useful campus knowledge in local memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged executable is incomplete, so the documented CLI behavior cannot be verified from this release artifact. <br>
Mitigation: Review the installed package before use and confirm that the referenced implementation files are present and runnable. <br>
Risk: The skill describes persistent local memory and external lookup behavior that may store or transmit conversation-derived campus information. <br>
Mitigation: Confirm where SQLite memory is stored, how users can inspect or delete it, and what data may be sent to external services before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text and Markdown-style responses with CLI commands and JSON recall results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user identifier environment variable for CLI-backed profile and memory operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
