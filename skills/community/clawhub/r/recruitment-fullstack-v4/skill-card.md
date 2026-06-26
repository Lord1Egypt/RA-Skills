## Description: <br>
Provides a structured recruiting workflow for intake, resume screening, interview design, BARS interview evaluation, calibration, and final hiring decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuritu](https://clawhub.ai/user/wuritu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring managers, and interview panels use this skill to structure candidate intake, resume review, interview scripts, evidence-based scoring, calibration discussions, and final hiring recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A corrupted final-decision module can make hiring recommendations unreliable. <br>
Mitigation: Repair and review the final-decision file before use, and manually verify every recommendation against the full candidate evidence. <br>
Risk: Recruiting workflows can expose sensitive candidate data and create legal or anti-discrimination risk. <br>
Mitigation: Use the skill only with recruiter or hiring-manager direction, limit candidate-data access, and follow applicable hiring-law, privacy, retention, and anti-discrimination requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuritu/recruitment-fullstack-v4) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill entrypoint](artifact/SKILL.md) <br>
- [Final-decision module](artifact/packages/07-final-decision.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Analysis, Configuration] <br>
**Output Format:** [Markdown reports, scorecards, interview scripts, evaluation rubrics, calibration notes, and hiring recommendation templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite candidate evidence, include scoring details, preserve uncertainty, and avoid protected or irrelevant personal attributes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
