## Description: <br>
Reddit Pain Workflow helps agents run a daily pipeline that scans Reddit communities, classifies developer pain points, generates Markdown reports, pushes them to GitHub, and tracks metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to orchestrate scheduled Reddit monitoring, categorize community pain signals, and produce GitHub-published Markdown reports for trend and content analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact describes running an external script named reddit_pain_workflow.py, but that script is not included in the artifact evidence. <br>
Mitigation: Confirm which script or repository supplies reddit_pain_workflow.py before installing or running the workflow. <br>
Risk: The workflow publishes generated reports to GitHub and may require repository credentials. <br>
Mitigation: Use a test or dedicated GitHub repository and grant any GitHub token only the minimum permissions needed to push generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/reddit-pain-workflow) <br>
- [HermesMade homepage](https://github.com/minirr890112-byte/HermesMade) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces daily pain-point report guidance intended for scheduled automation and GitHub publication.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
