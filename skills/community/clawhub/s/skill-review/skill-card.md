## Description: <br>
Scrapes ClawHub skill pages for Security Scan results, runtime requirements, and comments for local skills, then writes a markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and skill maintainers use this skill to review ClawHub Security Scan, runtime requirement, and comment information across local skills and produce a consolidated markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security findings may be adjusted through suppressions, which can make acknowledged results look less severe than raw ClawHub or VirusTotal findings. <br>
Mitigation: Inspect suppressions.json before use and compare any Acknowledged status with the raw scanner result before relying on the report. <br>
Risk: The skill can read a local VirusTotal API key from the environment or local OpenClaw configuration. <br>
Mitigation: Use a limited VirusTotal API key and review the credential source before running the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Review release page](https://clawhub.ai/odrobnik/skill-review) <br>
- [Skill homepage](https://github.com/odrobnik/skill-review-skill) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the report to a user-selected output path, commonly under /tmp/.] <br>

## Skill Version(s): <br>
0.2.4 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
