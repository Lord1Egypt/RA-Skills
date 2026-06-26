## Description: <br>
Provides Chinese-oriented code and project analysis, summarizing project structure, dependencies, business logic, issues, and implementation details for requested code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inksnowhailong](https://clawhub.ai/user/inksnowhailong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to explain unfamiliar repositories or specific code paths in Chinese, including architecture, key files, dependencies, call flows, business logic, issues, and improvement suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest running a local Madge dependency diagram command, which can execute code in the workspace. <br>
Mitigation: Confirm the repository and referenced local script path are trusted before allowing the command. <br>
Risk: Large project analyses may intentionally simplify details or focus only on the main path. <br>
Mitigation: Review critical files directly or ask for a deeper follow-up before relying on conclusions for important decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inksnowhailong/tvs-analyze) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with Chinese prose, ASCII diagrams, and optional bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise improvement suggestions, risk notes, or a follow-up question when the analysis target is unclear.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
