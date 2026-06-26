## Description: <br>
Integrates with TimeDoctor API to pull employee time tracking data, worklogs, statistics, and productivity metrics using simple Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JehadurRE](https://clawhub.ai/user/JehadurRE) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized developers, operations teams, and workforce administrators use this skill to query TimeDoctor data from an agent, including worklogs, user and project lists, productivity statistics, payroll-related data, and screenshots or screencasts where permitted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive employee time tracking, productivity, payroll, screenshot, and screencast data. <br>
Mitigation: Use only an authorized, least-privileged TimeDoctor account and confirm employee monitoring is lawful, expected, and approved before use. <br>
Risk: The artifact includes workflows that ask for TimeDoctor passwords and produce long-lived JWT tokens. <br>
Mitigation: Do not paste passwords into chat; provide credentials outside the agent where possible and treat TIMEDOCTOR_TOKEN like a password. <br>
Risk: Persisting TIMEDOCTOR_TOKEN in shell profiles on shared systems can leak access to TimeDoctor data. <br>
Mitigation: Avoid storing tokens in shared shell profiles, rotate exposed tokens, and clear environment variables when the session ends. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JehadurRE/timedoctor-skill) <br>
- [Publisher profile](https://clawhub.ai/user/JehadurRE) <br>
- [Homepage from ClawHub metadata](https://github.com/JehadurRE/timedoctor-openclaw-skill) <br>
- [TimeDoctor API documentation](https://timedoctor.redoc.ly/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Markdown, Guidance] <br>
**Output Format:** [JSON from the Python CLI, typically summarized by the agent as Markdown tables, lists, or short explanations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, httpx, a TimeDoctor JWT token, and a TimeDoctor company ID for most data commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
