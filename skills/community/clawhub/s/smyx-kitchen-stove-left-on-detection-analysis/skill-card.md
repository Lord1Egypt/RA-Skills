## Description: <br>
Analyzes fixed kitchen camera media to detect unattended stove-on conditions and return structured alerts, monitoring results, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Caregivers, family members, smart-home operators, and elder-care staff use this skill to analyze stove-area kitchen images or videos for unattended flame or heat-source conditions and to review related cloud reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Kitchen images or videos may be sent to the LifeEmergence cloud service and associated with an automatically selected or created identity. <br>
Mitigation: Obtain consent from people being monitored, avoid submitting unrelated sensitive files, and confirm cloud report deletion practices before use. <br>
Risk: Backend tokens for cloud report access may be persisted in local SQLite data. <br>
Mitigation: Restrict local file access and review how to delete local token data when deprovisioning the skill. <br>
Risk: Automated visual detection can produce incorrect stove or occupancy alerts. <br>
Mitigation: Treat alerts as assistive and verify urgent conditions before relying on operational actions such as valve shutdown. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-kitchen-stove-left-on-detection-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Kitchen stove left-on API reference](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown text with structured JSON report content, alert status, report links, and CLI command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local media file paths or public media URLs; history queries return cloud report lists.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release; artifact frontmatter declares 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
