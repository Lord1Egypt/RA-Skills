## Description: <br>
Analyzes infrared bedroom or hallway monitoring video to detect elderly bed-exit duration and wandering, then returns structured alerts and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers, nursing-home operators, and smart-care integrators use this skill to analyze night-vision bedroom or hallway footage for bed-exit duration, wandering behavior, threshold-based alerts, and historical report review. The output is behavioral monitoring information for care follow-up, not a medical diagnosis or care plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends elderly bedroom or hallway monitoring footage to the LifeEmergence cloud service for analysis. <br>
Mitigation: Use only with appropriate consent and privacy review for monitored individuals, and confirm acceptable cloud processing and retention practices before deployment. <br>
Risk: The skill silently creates or reuses an account identity and stores tokens locally. <br>
Mitigation: Review identity lifecycle, local token storage, access control, and account revocation expectations before installing or running the skill. <br>
Risk: The skill can retrieve historical cloud reports associated with the resolved account identity. <br>
Mitigation: Limit use to authorized operators and verify that report access aligns with organizational privacy and audit requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-elderly-night-bed-exit-wandering-analysis) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [Elderly Night Bed-Exit API Documentation](artifact/references/api_doc.md) <br>
- [SMYX Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files] <br>
**Output Format:** [Markdown status text with embedded structured JSON and report links; optional output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cloud API results may include structured analysis reports, alert levels, report export links, and historical report lists.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact frontmatter lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
