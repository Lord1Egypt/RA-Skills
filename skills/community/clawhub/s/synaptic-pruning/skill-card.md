## Description:

Identifies vestigial code, including dead feature branches, stale configuration, orphaned tests, and old architectural remnants, and produces a pruning report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to examine a codebase for stale features, fossilized configuration, orphaned tests, compatibility shims, defensive fossils, outdated documentation, and abandoned subsystems before planning removals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to recommend code or documentation removal when production usage, reachability, or feature-flag history is incomplete.

Mitigation: Treat pruning recommendations as review candidates and confirm telemetry, ownership, tests, and release history before deleting or disabling anything.

Risk: Large-repository inspection can produce broad findings that mix high-confidence dead code with uncertain architectural context.

Mitigation: Prioritize low-risk findings first and require human review for borderline, user-facing, or recently changed components.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jcools1977/skills/synaptic-pruning)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces vitality scoring, vestigial-code classifications, pruning order, safety notes, and maturity metrics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
