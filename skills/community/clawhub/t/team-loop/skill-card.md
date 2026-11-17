## Description:

team-loop is an autonomous task loop engine that executes quantifiable repository goals through repeated planning, implementation, verification, memory, and replanning cycles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ifeel-is-a-mouse](https://clawhub.ai/user/ifeel-is-a-mouse)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use team-loop to pursue measurable repository goals such as coverage improvement, code migration, refactoring, and test completion with autonomous verification rounds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous repository mutation and test execution can change files, create commits, revert work, and run project code after launch.

Mitigation: Install only in disposable clones or branches where autonomous edits, commits, reverts, test execution, and local logging are acceptable.

Risk: The loop has limited user control after launch and may continue spending tokens or rounds until a stop condition is reached.

Mitigation: Set tight budget and max_rounds limits before invocation, review the parsed goal before launch, and stop with .team-loop/STOP when needed.

Risk: Local state can persist prompts, code context, file paths, debug logs, patches, and reports.

Mitigation: Review .team-loop/ and logs/ contents before sharing the repository or committing generated artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ifeel-is-a-mouse/skills/team-loop)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus generated code, tests, JSON state snapshots, audit reports, token reports, and patches during execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces incremental repository deliverables, state snapshots, audit reports, token bills, commits, reverts, and local loop logs when invoked.]

## Skill Version(s):

2.4.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
