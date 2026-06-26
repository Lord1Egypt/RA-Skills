## Description: <br>
Tracks Nova skill versions, monitors selected expert information sources, generates skill-evolution reports, and suggests updates for human approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catplus-eric](https://clawhub.ai/user/catplus-eric) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to track skill version history, monitor selected expert sources on a schedule, and generate Markdown reports that recommend whether a skill update needs human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags recurring monitoring, persistent local writes, broad activation, external notifications, and automatic patch updates without clear user controls. <br>
Mitigation: Require explicit confirmation for each run, skill update, outbound notification, and persistent write before enabling or executing the workflow. <br>
Risk: The security evidence notes that current source-checking results should be treated cautiously because the included script records URLs as checked without fetching or analyzing them. <br>
Mitigation: Treat generated reports as review prompts, not verified source analysis, and require human review before changing tracked skills. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/catplus-eric/skill-evolution-tracker) <br>
- [Server-resolved provenance unavailable](unavailable) <br>
- [Rau LinkedIn posts](https://www.linkedin.com/posts/rauchg) <br>
- [The Vercel Journey with Guillermo Rauch](https://refactoring.fm/p/the-vercel-journey-with-guillermo) <br>
- [Addy Osmani blog](https://addyosmani.com/blog/) <br>
- [Navalmanack](https://navalmanack.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, JSON version records, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write persistent local version records and reports under the skill workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
