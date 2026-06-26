## Description: <br>
Enables any skill to gain self-evolution capabilities by generating domain-specific learning logs, evolution rules, and a Review-Apply-Report workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zhaobudaoyuema](https://clawhub.ai/user/Zhaobudaoyuema) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent-skill maintainers use this skill to add self-evolution behavior to another skill, including feedback logs, error logs, feature-request tracking, and evolution rules tailored to the target skill's domain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently rewrite another skill's behavior and overwrite evolution files. <br>
Mitigation: Run the scaffold script with --dry-run first, inspect diffs, and back up the target skill before applying changes. <br>
Risk: Adding workspace-level SOUL.md or AGENTS.md snippets can change agent behavior beyond a single target skill. <br>
Mitigation: Add workspace-level snippets only when that broader behavior change is intentional and review them before deployment. <br>
Risk: Applying this to third-party skills the user does not control can introduce unreviewed behavior changes. <br>
Mitigation: Use the skill only on skills the operator controls or has permission to modify. <br>


## Reference(s): <br>
- [Domain examples](references/domain-examples.md) <br>
- [OpenClaw active feedback integration](references/openclaw-feedback.md) <br>
- [ClawHub skill page](https://clawhub.ai/Zhaobudaoyuema/skill-self-evolution-enhancer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and shell scaffold commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create .learnings/ files, DOMAIN-CONFIG-DRAFT.md, and EVOLUTION.md in a target skill; dry-run mode is available for the scaffold script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
