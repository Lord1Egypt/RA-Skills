## Description:

Helps agent users and skill authors turn self-improvement needs into practical workflows, checklists, analyses, code changes, and verification notes for fixing bugs, hardening setup and safety, improving reliability, or creating adjacent skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to clarify requirements, create reusable workflows or decision aids, produce concrete artifacts, and verify improvements for self-improving agent-style work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit activation keywords can route unrelated requests to this skill.

Mitigation: Prefer explicit invocation or narrow the trigger keywords before enabling implicit activation.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [Popular ClawHub skill demand: self-improving agent](https://clawhub.ai/skills/self-improving-agent)
- [Popular ClawHub skill demand: Self-Improving + Proactive Agent](https://clawhub.ai/skills/self-improving)
- [HGC QC: cap the module at computation; retire the QC plotting layer](https://github.com/bigbio/hvantk/issues/205)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, templates, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to the user's immediate request and should state assumptions, limits, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
