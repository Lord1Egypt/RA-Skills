## Description:

A Chinese-language agent skill that upgrades existing Skill.md files with unstable routing or inter-skill conflicts by diagnosing registration, entry matching, boundaries, handoff contracts, and naming before producing a structured L2 upgrade package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeasonhaitao](https://clawhub.ai/user/jeasonhaitao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt engineers, and skill authors use this skill to diagnose and improve existing AI skills that have basic structure but are unstable in multi-skill routing. It produces a complete L2 upgrade package with diagnosis, revised Skill.md content, before-and-after comparison, test prompts, and validation records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may create routing conflicts in a large shared skill set.

Mitigation: Review and narrow trigger phrases before deployment, especially where adjacent skills handle skill creation, prompt engineering, or routing diagnostics.

Risk: Accepted upgrade proposals could introduce incorrect or misleading guidance into another skill.

Mitigation: Treat generated Skill.md revisions as proposals; review and scan revised skills before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeasonhaitao/skills/skill-upgrade-craftsman-l2)
- [Deployment README](artifact/README_DEPLOY.md)
- [Test Prompts](artifact/TEST_PROMPTS.md)
- [Validation Report](artifact/VALIDATION_REPORT.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with Skill.md code blocks, comparison tables, test prompts, and validation templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are proposals for human review; the skill does not automatically modify or deploy other skills.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
