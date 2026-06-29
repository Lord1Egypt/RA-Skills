## Description: <br>
Analyzes pet-carrier videos or video URLs through server-side APIs to estimate resting respiratory rate, flag rates above 40 bpm, and return structured monitoring results without diagnosing disease. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet owners, transport operators, and support agents use this skill to submit pet-carrier video for respiratory-rate monitoring, abnormal-rate alerts, structured reports, and cloud history lookup during pet air or long-distance transport. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet videos or video URLs are sent to the Life Emergence cloud service for analysis and history lookup. <br>
Mitigation: Use the skill only with footage approved for that external service, and avoid submitting unrelated or sensitive video content. <br>
Risk: The skill silently creates or reuses an internal cloud identity and stores returned authentication tokens in a local workspace database. <br>
Mitigation: Run the skill in an isolated workspace when identity separation matters, and review or clear the workspace data directory when token reuse is not desired. <br>
Risk: Respiratory-rate alerts are health-reference signals and are not a disease diagnosis or treatment recommendation. <br>
Mitigation: Treat abnormal-rate results as monitoring alerts and seek qualified veterinary review for urgent or clinical decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-pet-carrier-respiratory-rate-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [Pet Carrier Respiratory Rate API Documentation](references/api_doc.md) <br>
- [Shared Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON analysis report with optional report link; shell commands for execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save output to a file when --output is provided; supports basic, standard, or json detail modes.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
