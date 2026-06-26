## Description: <br>
A lightweight release-quality workflow for OpenClaw / ClawHub skills. Use when deciding whether a skill is ready to publish, verifying a release, and turning post-release feedback into actionable updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[choosenobody](https://clawhub.ai/user/choosenobody) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill maintainers use this skill to decide whether an OpenClaw or ClawHub skill is ready to publish, verify a release, and convert feedback into concrete update decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated agent prompt can lead an agent to patch a local SKILL.md and run ClawHub/OpenClaw verification commands. <br>
Mitigation: Review the target slug, command list, and proposed file changes before allowing the agent to patch files or run release verification. <br>
Risk: Release reports may overstate verification when the public page or current release evidence is blocked or unavailable. <br>
Mitigation: Label blocked checks as BLOCKED, cite the evidence source used, and avoid reporting PASS without matching CLI, OpenClaw, ClawHub, or public-page evidence. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/choosenobody/skill-release-lifecycle) <br>
- [Dogfood Run 001 - skill-release-lifecycle](references/dogfood-run-001-skill-release-lifecycle.md) <br>
- [Dogfood Run 001 - Self-Gate](references/dogfood-run-001-self-gate.md) <br>
- [Dogfood Run 002 - lifecycle self-evaluation](references/dogfood-run-002-lifecycle-self-eval.md) <br>
- [Publish Gate - Worked Example: waste-audit](references/publish-gate-example.md) <br>
- [Iteration Loop - Worked Example: waste-audit](references/iteration-loop-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with checklist results and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces release-readiness judgments, verification steps, feedback classifications, and a copy-paste agent prompt.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
