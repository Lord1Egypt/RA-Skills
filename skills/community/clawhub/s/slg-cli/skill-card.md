## Description: <br>
Semantic git history search and code archaeology for questions about why code exists, who owns files, regressions, commit ranges, and revert risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[venki0552](https://clawhub.ai/user/venki0552) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to run local semantic searches over git history, summarize changes, identify likely owners, investigate regressions, and assess revert risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool indexes git history, which may include old secrets or sensitive past commits. <br>
Mitigation: Use it only in repositories where local indexing of commit history is acceptable, and prefer npx for trial use if a global install is not desired. <br>
Risk: The optional MCP server can make indexed repository history available to connected agents. <br>
Mitigation: Enable the MCP server only for trusted agents and sessions, and stop it when repository-history access is no longer needed. <br>


## Reference(s): <br>
- [SLG CLI homepage](https://github.com/vrknetha/slg-cli) <br>
- [ClawHub skill page](https://clawhub.ai/venki0552/slg-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume a local git repository and an initialized slg index.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
