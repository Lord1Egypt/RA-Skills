## Description: <br>
Cadence Virtuoso Skill language development helper that supports API lookup, code linting, and natural-language API recommendations for writing and debugging Virtuoso Skill code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keenone](https://clawhub.ai/user/keenone) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query Cadence Virtuoso Skill APIs, recommend likely API functions from natural-language tasks, and lint Skill source files or snippets for undefined calls and argument-count issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional web UI has no authentication and listens on all interfaces. <br>
Mitigation: Start the web UI only on localhost or a trusted network. <br>
Risk: Directory linting reads files from user-selected project folders. <br>
Mitigation: Run directory checks only on intended Virtuoso Skill project folders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keenone/virtuoso-skill) <br>
- [skill_api_database.json](artifact/references/skill_api_database.json) <br>
- [skill_api_database_full.gz.json](artifact/references/skill_api_database_full.gz.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text with Skill code snippets, API details, lint diagnostics, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked API recommendations, syntax and parameter summaries, example Skill code, warnings, and validation errors.] <br>

## Skill Version(s): <br>
1.0.4 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
