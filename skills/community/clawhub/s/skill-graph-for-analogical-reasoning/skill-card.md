## Description: <br>
Builds a graph over SKILL.md skills, chooses one primary skill, and retrieves complementary support instead of naively attaching top similar skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4444433333](https://clawhub.ai/user/h4444433333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build and query a local graph of SKILL.md folders so an agent can choose a primary skill and complementary support for a task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The build command scans local skill directories selected by the user and writes graph files to a user-selected output path. <br>
Mitigation: Run it only against intended skill directories and choose an output location that is safe to create or overwrite. <br>
Risk: Query results may reveal whether required environment variables or binaries for scanned skills appear to be missing. <br>
Mitigation: Review graph and query outputs before sharing them outside the workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/h4444433333/skill-graph-for-analogical-reasoning) <br>
- [Skill bundle README](artifact/README.md) <br>
- [Reference](artifact/reference.md) <br>
- [Python package README](artifact/python-package/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON files, HTML files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, plus JSON graph output and standalone HTML visualization from the CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Build writes graph.json to the selected output directory; query reads an existing graph; look writes an HTML visualization to the selected output path.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
