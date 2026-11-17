## Description:

Build and publish OpenClaw skills from recurring pain points by scanning .learnings/ for repeated errors, scaffolding skills, and publishing them to ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wrentheai](https://clawhub.ai/user/wrentheai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agents use this skill to identify recurring pain points from .learnings/ logs, scaffold reusable skills from them, and package or publish reviewed skills to ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publish workflow can package and publish skills from the active workspace.

Mitigation: Run publish only in a controlled workspace after reviewing the generated skill files and intended release target.

Risk: Untrusted .learnings entries can influence generated skill scaffolds.

Mitigation: Review .learnings input and generated factory prompts before turning a candidate into a published skill.

Risk: The security review flags high-impact safety concerns in the publish path.

Mitigation: Prefer a fixed trusted ClawHub CLI version and review the skill before installation until the shell execution and confirmation issues are addressed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wrentheai/skills/wren-skill-factory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown instructions and generated skill files with Node.js command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create skill scaffolds, factory prompts, scripts, packaged artifacts, and publish commands in the active workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
