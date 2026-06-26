## Description: <br>
Implements a three-layer self-improvement process for agents to evaluate tasks, learn from outcomes, optimize performance, and share knowledge across local agent workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Brandon114](https://clawhub.ai/user/Brandon114) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a local self-improvement loop for scoring completed tasks, recording lessons, generating optimization plans, and sharing lessons between WorkBuddy agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent lesson storage can retain sensitive prompts, customer data, tokens, or operational details if users record them as lessons. <br>
Mitigation: Do not save secrets or sensitive operational details as lessons, and review the generated JSON files before retaining or sharing them. <br>
Risk: Cross-agent sync can spread the shared knowledge file across local WorkBuddy workspaces without strong scoping or retention controls. <br>
Mitigation: Run the sync script only when cross-agent sharing is intended, and remove sensitive, stale, or workspace-specific lessons before syncing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Brandon114/self-improving-agent-python) <br>
- [README_en.md](artifact/README_en.md) <br>
- [SKILL_en.md](artifact/SKILL_en.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python-generated JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local JSON records under self-improvement/ and shared-context/self-improvement/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
