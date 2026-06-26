## Description: <br>
Task Director — turn complex tasks into movie storyboards. Create a plan, review it, then execute step by step with fallback support. Pause, retry, skip anytime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[besty0121](https://clawhub.ai/user/besty0121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Task Director to break complex work into reviewable scenes and shots, approve a plan, then execute and track each step with pause, skip, retry, and fallback controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated storyboards may include shell commands that install packages, contact the network, delete files, or access sensitive directories. <br>
Mitigation: Review each scene and shot before approval, and edit or reject commands that do not match the intended task. <br>
Risk: Task plans and command output are stored in local JSON files under ~/.openclaw/memory/movies/. <br>
Mitigation: Avoid recording secrets or sensitive output in task descriptions and result text, and clean up local records when needed. <br>


## Reference(s): <br>
- [Task Director on ClawHub](https://clawhub.ai/besty0121/task-director) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus JSON records for agent action and result loops] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill tracks local storyboard state as JSON files under ~/.openclaw/memory/movies/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
