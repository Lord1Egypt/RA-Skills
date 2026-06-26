## Description: <br>
Thorough on-demand refresh of one skill in a skills repository: researches usage/upstream/docs in parallel, gates twice for approval, bumps version, updates CHANGELOG, runs the repo's validation, then commits and watches CI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and maintainers use this skill to refresh a specific skill in a skills repository, review upstream and usage evidence, apply approved updates, validate the repository, and manage the commit or PR workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide repository edits, validation, commits, pushes, and public release workflows that affect skills and published content. <br>
Mitigation: Use it only with the intended repository and account, and follow the built-in approval gates, privacy scan, and validation before committing or pushing. <br>
Risk: Optional prior-session usage research can surface advisory leads that are unsuitable for direct publication without review. <br>
Mitigation: Ground usage findings in primary sources before acting on them and redact any private or unsafe material before public release. <br>


## Reference(s): <br>
- [Pond MCP](https://pond.cascade.fyi/) <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/update-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured reports, approval gates, inline shell commands, and proposed file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit human approval before edits and before commit or push actions.] <br>

## Skill Version(s): <br>
0.7.0 (source: frontmatter and changelog, released 2026-06-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
