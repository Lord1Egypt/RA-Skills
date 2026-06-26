## Description: <br>
Analyzes cat climbing frame or cat tree videos to report area dwell time, transitions, activity density, and 2D heatmap observations without providing medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and pet-care workflow builders use this skill to turn cat tree or climbing-frame videos into structured activity observations and report links. It supports reviewing enrichment use, dwell time by platform, movement transitions, and history reports while keeping identity handling out of user-facing prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends pet videos or video URLs to the LifeEmergence/SMYX backend and silently associates requests with an internal identity. <br>
Mitigation: Install and run it only when that data flow is acceptable for the videos being analyzed. <br>
Risk: The skill may reuse locally stored workspace data such as API keys, tokens, identity records, or databases. <br>
Mitigation: Review or clear workspace data files such as smyx-api-key.txt and smyx-common-claw.db before use when prior identities or stored tokens should not be reused. <br>
Risk: Activity heatmap outputs could be mistaken for veterinary diagnosis. <br>
Mitigation: Use the outputs as objective activity observations only and route health concerns to a qualified professional. <br>


## Reference(s): <br>
- [Pet Climbing Frame / Cat Tree Activity Heatmap API Documentation](references/api_doc.md) <br>
- [Common AI Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-pet-climbing-frame-heatmap-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON activity report with optional report links and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include dwell-time statistics, jump or transition counts, heatmap observations, history tables, and report URLs.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
