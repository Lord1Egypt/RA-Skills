## Description: <br>
Identifies repeated workflow patterns, manages skill change proposals, reviews candidates, chains skills, and scaffolds new skills from review outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chamberz40](https://clawhub.ai/user/chamberz40) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using Claude Code use this skill to capture repeatable multi-step sessions as skill candidates, review them for deduplication, scaffold new skills, and manage changes to existing skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic hooks can quietly record session and tool-use metadata with unclear retention controls. <br>
Mitigation: Review the hook entries before enabling them, use the skill only on appropriate machines, and define a cleanup plan for candidate logs and temporary files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chamberz40/skill-spec) <br>
- [README](README.md) <br>
- [Change proposals](CHANGE.md) <br>
- [Hook validation script](scripts/test-hooks.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can lead to local candidate logs, CHANGE.md proposals, and scaffolded SKILL.md files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
