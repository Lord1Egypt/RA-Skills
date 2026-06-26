## Description: <br>
Think Expand is an OpenCode orchestration skill that routes agent input through a central planning core with memory retrieval, self-evolution, and task suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenCode can use this skill as a central planning layer to coordinate related hear, see, speak, do, and learn modules, retrieve local memory, and recommend next actions. It is intended for broad input orchestration and local learning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed as an always-on orchestrator that can inspect broad user input, monitor the clipboard, and retain local learning or profile data. <br>
Mitigation: Install only when that behavior is intended, and confirm how to disable startup behavior, clipboard monitoring, habit recording, and local data retention before use. <br>
Risk: Automatic learning from GitHub or the web may introduce untrusted skill content into the local knowledge base. <br>
Mitigation: Review and scan learned or integrated skills before deployment, and disable automatic learning if the environment requires curated sources only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/think-expand) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with inline shell commands and task recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local tools, clipboard monitoring, and local learning state described by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
