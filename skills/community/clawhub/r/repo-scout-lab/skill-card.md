## Description: <br>
Use when the user wants to use Repo Scout or work on the Repo Scout project to search GitHub repos, generate project ideas and reports, compare runs, inspect history or trending data, build dashboards, manage bookmarks/watchlists, or prepare publishable scouting outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsvips](https://clawhub.ai/user/itsvips) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, and research teams use this skill to operate Repo Scout for GitHub repository discovery, trend tracking, project idea generation, scouting reports, dashboards, and saved-run comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested Repo Scout commands may query GitHub, write local reports, keep history or bookmarks, use an optional LLM flag, or start a local dashboard server. <br>
Mitigation: Review generated commands before execution, choose output paths intentionally, avoid sharing sensitive saved data, enable LLM use only when acceptable, and bind local dashboard usage to an appropriate trusted environment. <br>


## Reference(s): <br>
- [Repo Scout command map](references/commands.md) <br>
- [ClawHub listing](https://clawhub.ai/itsvips/repo-scout-lab) <br>
- [Publisher profile](https://clawhub.ai/user/itsvips) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command option guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest saving reports with --out, using --json for automation, enabling optional LLM-assisted idea generation, or running a local dashboard server.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
