## Description: <br>
Provides automated and manual rollback for long-running OpenClaw tasks by saving and restoring caller-provided state snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cortez-1](https://clawhub.ai/user/Cortez-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers integrating OpenClaw workflows can use this skill to create task-start snapshots and prompt users to continue or roll back long-running work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad caller-provided state snapshots can include secrets or unrelated private data. <br>
Mitigation: Pass only the specific state that should be reversible and exclude credentials, tokens, and unrelated private data. <br>
Risk: Package and display naming are not perfectly consistent across server evidence and artifact metadata. <br>
Mitigation: Verify the package identity and publisher profile before installation or deployment. <br>
Risk: Default JSON-based cloning may not fully preserve non-serializable state. <br>
Mitigation: Provide custom save and restore callbacks for complex state objects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Cortez-1/timeback-machine) <br>
- [Publisher profile](https://clawhub.ai/user/Cortez-1) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, guidance] <br>
**Output Format:** [JavaScript module behavior with confirmation prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts before restoring caller-provided in-memory state; rollback behavior depends on the supplied save and restore callbacks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifests) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
