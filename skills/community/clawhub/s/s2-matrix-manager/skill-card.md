## Description: <br>
Manage and monitor a local 3x3 grid of offline s2-matrix-pod agents with real-time status and local chat in the current directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local s2-matrix-pod JSON state, view pod activity status, and leave local chat messages for nearby pods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local chat messages are saved in s2_matrix_data. <br>
Mitigation: Do not enter secrets or sensitive data into the chat interface unless local storage in that directory is acceptable. <br>
Risk: Pod JSON metadata influences displayed text and chat log filenames. <br>
Mitigation: Use pod JSON files from trusted local sources and review the s2_matrix_data directory before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpaceSQ/s2-matrix-manager) <br>
- [Space2.world](https://space2.world) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text prompts, status output, and local chat log text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads pod JSON files from s2_matrix_data and appends chat logs in the same local directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
