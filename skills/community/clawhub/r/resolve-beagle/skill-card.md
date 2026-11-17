## Description:

Resolve Beagle helps agents close open questions and latent gaps in a brainstorm-beagle spec by researching issues, proposing evidence-backed answers for user approval, and rewriting the spec in place.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product owners, and spec authors use this skill to turn a brainstorm-beagle spec with open questions, placeholders, or ambiguous requirements into an implementation-ready spec before planning starts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read project files, use external web research, and rewrite the target spec in place.

Mitigation: Use it on specs the agent is allowed to inspect and edit, and review the proposed gap list before allowing research to proceed.

Risk: Accepted proposals could introduce incorrect or misleading requirements into a planning document.

Mitigation: Review each evidence-backed proposal before acceptance and re-read the rewritten spec before planning begins.

Risk: The workflow may create a commit if the user approves it.

Mitigation: Require explicit user approval before any commit and inspect the resulting diff when repository history matters.

## Reference(s):

- [Subagent Prompt Templates](references/subagent-prompts.md)
- [Resolve Beagle ClawHub Listing](https://clawhub.ai/anderskev/skills/resolve-beagle)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown spec edits with structured proposal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before research proceeds and before any commit.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
