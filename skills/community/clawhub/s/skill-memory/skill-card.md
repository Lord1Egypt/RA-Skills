## Description: <br>
Self-learning task-to-skill routing table that records skill choices and updates preset parameters based on usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systiger](https://clawhub.ai/user/systiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to look up preferred skills and preset parameters for recurring task types, then record or update mappings as usage changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task details and parameters may be saved into the local memory file, including sensitive context if supplied by a user. <br>
Mitigation: Avoid storing secrets or private task details in scenarios or parameters, and review references/memory.json periodically. <br>
Risk: Stored mappings can influence future skill choices without clear opt-in or cleanup controls. <br>
Mitigation: Install only when self-updating skill routing is intended, and manually remove stale or unwanted entries from the memory file. <br>
Risk: The screenshot preset connects to an existing Chrome CDP session. <br>
Mitigation: Use a dedicated browser profile when applying the Chrome CDP screenshot preset. <br>


## Reference(s): <br>
- [Skill Memory Release Page](https://clawhub.ai/systiger/skill-memory) <br>
- [memory.json](artifact/references/memory.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates a local memory JSON file when the bundled script is run.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
