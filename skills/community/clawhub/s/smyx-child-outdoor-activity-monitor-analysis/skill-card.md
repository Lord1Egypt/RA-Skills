## Description: <br>
This skill analyzes fixed-camera videos at a balcony door, home entrance, or similar indoor-outdoor boundary to estimate a child's daily outdoor activity duration and produce activity reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents, child-care operators, schools, kindergartens, and developers can use this skill to analyze door or balcony camera video, estimate child exit and return sessions, and generate daily outdoor-duration reports or reminders. The output is activity tracking guidance only and is not a medical diagnosis or prescription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the skill sends child or home camera footage, video URLs, and user identifiers to configured LifeEmergence cloud services. <br>
Mitigation: Use only with guardian consent, confirm endpoint ownership and data handling terms, and avoid sensitive household video until retention and deletion practices are documented. <br>
Risk: The security scan reports persisted account tokens with incomplete disclosure and scoping. <br>
Mitigation: Review token storage and access controls before installation, and remove or replace bundled API keys where appropriate. <br>
Risk: Activity estimates are based on visual entry and exit events and may not represent true outdoor exercise or health status. <br>
Mitigation: Treat results as household activity tracking, review outputs before acting on reminders, and avoid using them as medical advice. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/18072937735/smyx-child-outdoor-activity-monitor-analysis) <br>
- [API Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown guidance, command examples, and JSON-style activity reports or history tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include child detection status, ROI status, exit and return events, total outdoor duration, goal completion, alert type, alert level, parent-facing reminder text, and report links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
