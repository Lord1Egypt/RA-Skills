## Description: <br>
Enables an agent to interact with Jenkins CI/CD via REST API to trigger builds, list configured projects, and check build results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lentiancn](https://clawhub.ai/user/lentiancn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure project-to-Jenkins job mappings, inspect Jenkins job status, and trigger builds after an explicit confirmation step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Jenkins API credentials can be used to inspect jobs and trigger builds. <br>
Mitigation: Install only where JENKINS_USER and JENKINS_API_TOKEN are intended for agent use, and scope the token to the minimum Jenkins permissions needed. <br>
Risk: Stored project and Jenkins URLs could point the agent to the wrong job or repository. <br>
Mitigation: Review PROJECTS.md before use and confirm the selected project carefully before allowing a build trigger. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lentiancn/skills/skill-jenkins) <br>
- [PROJECTS.md](artifact/PROJECTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON question tool payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local project configuration and Jenkins credentials to inspect jobs, request confirmation, trigger builds, and summarize build status.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
