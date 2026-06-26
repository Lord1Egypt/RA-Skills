## Description: <br>
Generates structured Chinese study roadmaps from a learner's goal, current level, available time, and optional target direction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seulkilu](https://clawhub.ai/user/seulkilu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn broad learning goals into structured Chinese roadmaps with learner profile, success criteria, staged plans, resources, common blockers, and adjustment guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may answer in Chinese even when the surrounding conversation is in another language. <br>
Mitigation: Set the expected response language explicitly when using it in non-Chinese workflows. <br>
Risk: The skill may activate for broad study-planning prompts. <br>
Mitigation: Review activation behavior in the target agent and scope prompts when a generic planning response is preferred. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seulkilu/study-roadmap-generator) <br>
- [patterns.md](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Chinese structured roadmap text, with optional JSON output from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Roadmaps follow a fixed six-section structure covering learner profile, success criteria, staged plan, recommended learning stack, common blockers, and dynamic adjustments.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
