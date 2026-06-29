## Description: <br>
Grades a codebase for AI-slop and code-quality signals, then produces a scored report with cited findings and fix-it prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aidan945](https://clawhub.ai/user/aidan945) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill to assess a repository's code quality, identify AI-generated or sloppy patterns, and produce a local report with actionable repair prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the target repository and summarizes source details into local report artifacts. <br>
Mitigation: Run it only on repositories whose code you are comfortable storing in local scan and report files. <br>
Risk: The skill writes report artifacts into the target repository. <br>
Mitigation: Review the generated .slop-check directory and slop-report.html before committing or sharing repository contents. <br>
Risk: The skill can start a local report server. <br>
Mitigation: Use the localhost-only report server for inspection and stop it when the review is complete. <br>
Risk: Generated findings and fix-it prompts may contain incorrect or misleading code-review guidance. <br>
Mitigation: Review cited file and line evidence before applying recommended changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aidan945/skills/slop-check) <br>
- [HEURISTICS.md](references/HEURISTICS.md) <br>
- [SCORING.md](references/SCORING.md) <br>
- [REPORT-SCHEMA.md](references/REPORT-SCHEMA.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown/text response with shell commands plus generated JSON and HTML report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local scan artifacts such as .slop-check/metrics.json, .slop-check/slop-map.json, .slop-check/report-data.json, and slop-report.html; may serve the report on localhost.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
