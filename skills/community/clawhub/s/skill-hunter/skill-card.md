## Description: <br>
Find, evaluate, and install ClawHub skills using semantic search, security vetting, and side-by-side comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenoodl-synthesis](https://clawhub.ai/user/kenoodl-synthesis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use Skill Hunter to discover ClawHub skills, inspect candidate skill files before installation, compare trust and adoption signals, and manage local skill installs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install, update, update-all, and uninstall workflows can change local skill files. <br>
Mitigation: Treat those commands as explicit approval steps and confirm the target slug before running them. <br>
Risk: Search and inspection queries are sent to ClawHub public endpoints. <br>
Mitigation: Avoid including secrets or sensitive project details in ClawHub search queries. <br>


## Reference(s): <br>
- [Skill Hunter ClawHub page](https://clawhub.ai/kenoodl-synthesis/skill-hunter) <br>
- [Publisher profile](https://clawhub.ai/user/kenoodl-synthesis) <br>
- [ClawHub search API example](https://clawhub.ai/api/v1/search?q=code+review+security) <br>
- [ClawHub skills API example](https://clawhub.ai/api/v1/skills?sort=trending&limit=10) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with curl and ClawHub CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public ClawHub API URLs, ranked skill metadata, comparison criteria, and install-management commands.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence and artifact/claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
