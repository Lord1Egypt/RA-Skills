## Description: <br>
A callable skill factory for programmatic skill creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation workflows use this skill to generate complete AgentSkills packages from structured parameters, including SKILL.md plus optional scripts, references, and assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently write skill files, including potentially executable scripts, in caller-controlled output locations. <br>
Mitigation: Use it in a sandboxed workspace, avoid arbitrary output_dir values and resource filenames, and review generated scripts before allowing created skills to persist or run. <br>
Risk: Generated skills may contain incorrect, misleading, or unsafe caller-provided instructions or resources. <br>
Mitigation: Validate, review, and scan generated skills before deployment. <br>


## Reference(s): <br>
- [AgentSkills Specification Reference](references/skill-spec.md) <br>
- [ClawHub skill page](https://clawhub.ai/smallkeyboy/smallkeyboy-create-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [JSON result plus generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates skill directories and optional executable scripts; generated content depends on the structured request.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
