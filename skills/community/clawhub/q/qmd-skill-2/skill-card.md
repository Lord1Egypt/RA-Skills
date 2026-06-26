## Description: <br>
Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifecoacher](https://clawhub.ai/user/lifecoacher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to search and retrieve content from local Markdown note or documentation collections that they have indexed with qmd. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing qmd adds an external CLI from the referenced GitHub project. <br>
Mitigation: Install only after reviewing the qmd project and confirming the source is acceptable for the environment. <br>
Risk: Indexing broad note or work directories may surface private Markdown content in agent responses. <br>
Mitigation: Index narrow Markdown folders, use named collections, and apply collection filters when searching. <br>
Risk: Scheduled qmd update or embedding jobs can continue background re-indexing and local model work. <br>
Mitigation: Enable cron or scheduler jobs only intentionally, and keep update/embed schedules scoped to the desired collections. <br>


## Reference(s): <br>
- [qmd GitHub project](https://github.com/tobi/qmd) <br>
- [ClawHub Qmd skill page](https://clawhub.ai/lifecoacher/qmd-skill-2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline qmd CLI commands and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to request JSON output from qmd when structured search results are useful.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
