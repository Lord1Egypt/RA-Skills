## Description: <br>
Identifies abnormal behaviors such as limb tremors, convulsions, stiffness, and gait abnormalities through video recognition to support home risk monitoring for patients with chronic conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and care-support workflows use this skill to submit monitoring videos, images, or media URLs for cloud analysis of tremors, convulsions, stiffness, gait abnormalities, and related report history. Results are auxiliary monitoring information and do not replace professional medical diagnosis or clinical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends patient videos, video URLs, identifiers, and report queries to the lifeemergence cloud service. <br>
Mitigation: Use only with patient consent, a clear privacy and retention agreement, and media that is appropriate to disclose to the service provider. <br>
Risk: The skill may create or reuse a local identity database containing authentication tokens. <br>
Mitigation: Run it in a controlled workspace, restrict access to local storage, and review token lifecycle and cleanup expectations before installation. <br>
Risk: The security verdict is suspicious because sensitive health media and identity binding are handled automatically with limited user-facing consent or control. <br>
Mitigation: Review the security summary and guidance before installing, and avoid identifiable health footage unless the deployment has explicit consent and compliance controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-parkinson-epilepsy-behavior-recognition-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and tables, JSON-style analysis responses, report links, and shell commands for analysis or report-history queries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local image or video paths and public media URLs; documented media formats include jpg, jpeg, png, mp4, avi, and mov with a 10 MB maximum.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence; artifact frontmatter reports 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
