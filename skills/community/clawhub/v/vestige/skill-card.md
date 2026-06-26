## Description: <br>
Vestige provides a local cognitive memory system using FSRS-6 spaced repetition for persistent recall across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Belkouche](https://clawhub.ai/user/Belkouche) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Vestige to search, store, and manage persistent local memories such as preferences, project context, bug fixes, and reminders across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory may save and reuse personal or project details more automatically than users expect. <br>
Mitigation: Install only when a persistent local memory layer is desired, review and delete stored memories regularly, and avoid storing secrets, credentials, health, financial, legal, or other sensitive information. <br>
Risk: The skill relies on local Vestige binaries for memory operations. <br>
Mitigation: Verify the local Vestige binaries before use and run only trusted installations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local CLI and MCP command examples for searching, saving, reviewing, and managing memories.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
