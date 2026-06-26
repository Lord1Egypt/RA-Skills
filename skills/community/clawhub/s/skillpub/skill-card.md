## Description: <br>
Create, validate, security-scan, and publish skills to ClawHub for requests to make, scaffold, package, or distribute agent capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theashbhat](https://clawhub.ai/user/theashbhat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill publishers use this skill to scaffold a new skill, validate its structure, scan it for common security issues, and publish it to ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publishing workflow has a legitimate purpose, but the server security summary reports possible command injection in publish.sh and bypass flags for validation and security checks. <br>
Mitigation: Use only with skill sources you control, review SKILL.md metadata before publishing, avoid --skip-checks and --force except in isolated testing, and fix publish.sh to avoid eval and tightly gate bypass behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/theashbhat/skillpub) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify skill directories and scripts when its shell helpers are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
