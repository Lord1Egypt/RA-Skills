## Description: <br>
Analyzes git commit history to report commit frequency, top contributors, file changes, and commit message quality for development insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryudi84](https://clawhub.ai/user/ryudi84) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, team leads, and engineering managers use this skill to understand repository activity, contributor patterns, file-change hotspots, and commit message quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can expose private repository metadata, including contributors, file paths, branch details, and commit history summaries. <br>
Mitigation: Treat reports as internal by default and review or redact them before uploading CI artifacts or sharing output from private repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryudi84/sovereign-git-commit-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, or plain text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the generated report to a file and can exit with failure when the commit message quality score is below the configured threshold.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill.json, script header, and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
