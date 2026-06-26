## Description: <br>
自动将任务经验沉淀为 skill，在任务满足可复用条件后评估价值、查重已有 skill，并创建或更新可发布的 SKILL.md。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binyuli](https://clawhub.ai/user/binyuli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill after a completed task to decide whether reusable workflow knowledge should be saved, deduplicated against existing skills, written as SKILL.md, or published through ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change future agent behavior by creating, updating, and publishing persistent skills without requiring approval. <br>
Mitigation: Manually review every new or updated SKILL.md, check for secrets or task-specific private details, and confirm the ClawHub publishing destination before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binyuli/skill-autosave) <br>
- [Publisher profile](https://clawhub.ai/user/binyuli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead the agent to create or update SKILL.md files and publish a local skill when the workflow is followed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
