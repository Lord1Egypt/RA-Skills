## Description: <br>
Determines when elderly people living alone have no interaction or visitors for extended periods, and actively pushes care reminders to family members, suitable for remote care scenarios for elderly people living alone at home. | 无人陪伴监测技能，判定独居老人长时间无人互动来访，主动推送关怀提醒给家属，适用于居家独居老人远程关怀场景 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, family members, and elder-care platform operators use this skill to analyze home monitoring images, videos, or URLs for extended periods without interaction or visitors and to review related cloud report history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sensitive home-monitoring media or URLs to a third-party cloud service. <br>
Mitigation: Use only with consent from the monitored person and household, minimize submitted media, and confirm the Life Emergence backend is trusted for the deployment. <br>
Risk: The skill may automatically create or reuse an internal user identity and stores authentication tokens locally. <br>
Mitigation: Review local token persistence before installation, isolate execution environments where appropriate, and remove or rotate locally stored credentials when access should end. <br>
Risk: Cloud history queries can expose prior monitoring reports. <br>
Mitigation: Run history queries only for authorized users and review returned report links before sharing them. <br>
Risk: Monitoring analysis and care reminders may be incomplete or incorrect. <br>
Mitigation: Treat results as care-reminder support and confirm concerning situations through human follow-up or professional care channels. <br>


## Reference(s): <br>
- [API documentation](references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-unaccompanied-monitoring-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style structured report output, with optional shell command usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include care reminders, monitoring findings, cloud report history, and report links.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact SKILL.md frontmatter says 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
