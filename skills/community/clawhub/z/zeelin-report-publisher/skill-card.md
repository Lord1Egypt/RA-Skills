## Description: <br>
Publish reports to the ZeeLin reports website by copying report assets, inserting a new top entry into public/reports_config.json for any category, running build checks, and preparing pull-request-ready branches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thu-nmrc](https://clawhub.ai/user/thu-nmrc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and report maintainers use this skill to add PDF, PPT, or PPTX reports to the ZeeLin reports site through a branch, build check, and pull request workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional bootstrap can create persistent GitHub SSH access for the selected account. <br>
Mitigation: Run bootstrap only on a trusted machine and account, use skip options when credentials are already configured, and remove the uploaded SSH key later if persistent access is not desired. <br>
Risk: The publishing workflow changes a report-site repository and pushes a branch for review. <br>
Mitigation: Review the generated branch, build result, and pull request before merging. <br>


## Reference(s): <br>
- [Zeelin Report Publisher on ClawHub](https://clawhub.ai/thu-nmrc/zeelin-report-publisher) <br>
- [Report Metadata Contract](references/report-metadata.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, configuration values, and file-change summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create report assets, update reports_config.json, create a git branch, and open or describe a pull request.] <br>

## Skill Version(s): <br>
0.1.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
