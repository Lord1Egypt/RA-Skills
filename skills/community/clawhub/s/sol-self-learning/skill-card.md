## Description: <br>
Persistent memory and self-improvement for AI agents that writes and refines local memory files over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amrree](https://clawhub.ai/user/amrree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a file-based learning loop to OpenClaw or similar agents: capture failures, extract patterns, record fixes, and review memory files that guide future work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write long-lived failure logs and memory files that may capture sensitive prompts, secrets, tokens, or private file content. <br>
Mitigation: Avoid logging sensitive content, review the generated learning files, and periodically delete or redact the JSON and memory files. <br>
Risk: The wrapper can run supplied commands and the automated fix flow can mark similar failures as fixed, which may exceed what users expect from simple file read/write permissions. <br>
Mitigation: Run only commands you understand, review command strings before execution, and avoid the command wrapper or scheduled fix-all flow unless it has been checked for the target environment. <br>


## Reference(s): <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; runtime helpers produce JSON learning logs and text reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local learning files under ~/.openclaw/learning/ and memory files under ~/.openclaw/workspace/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
