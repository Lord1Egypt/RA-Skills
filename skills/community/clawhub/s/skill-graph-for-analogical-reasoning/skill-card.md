## Description:

Skill Graph for Analogical Reasoning builds a graph over local SKILL.md folders to choose one primary skill and retrieve complementary support instead of naive top-similar matches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4444433333](https://clawhub.ai/user/h4444433333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-workflow maintainers use this skill to build and query a graph of local SKILL.md folders, select a primary skill for a task, and inspect complementary or fallback skills before adding context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher can fall back to running a local grap-skill executable discovered from PATH.

Mitigation: Use the bundled helper or a trusted installed module in a controlled environment, and avoid untrusted PATH entries until the launcher uses only a trusted absolute entrypoint.

Risk: Generated graph.json files can contain local paths and excerpts from indexed skill files.

Mitigation: Run the build command only on skill directories intended for indexing, and review graph artifacts before sharing them outside the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/h4444433333/skills/skill-graph-for-analogical-reasoning)
- [README](README.md)
- [Reference](reference.md)
- [Python package README](python-package/README.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with shell commands; CLI commands can produce JSON graph data and HTML visualization files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3. The build command scans selected skill directories and can write graph.json; the look command can write an HTML visualization.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
