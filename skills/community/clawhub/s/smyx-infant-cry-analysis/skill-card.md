## Description: <br>
Detects baby cries from audio or video, classifies likely causes such as hunger, tiredness, pain, discomfort, or irritability, and returns a structured report for caregiver review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers and agent users can use this skill to analyze submitted baby-cry audio or video and receive a structured summary of likely needs, recommendations, and report links. The output is intended as parenting support and not as a substitute for medical evaluation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Baby audio, video, or media URLs may be sent to the lifeemergence cloud service for analysis. <br>
Mitigation: Use the skill only with appropriate consent, submit only media needed for the analysis, and review service retention and privacy expectations before installation. <br>
Risk: Prior cry-analysis reports may be queried from the cloud. <br>
Mitigation: Ask before retrieving history, limit history lookup to the intended user context, and avoid exposing report links or report contents to unauthorized users. <br>
Risk: The skill may create or reuse a local identity and persist account tokens. <br>
Mitigation: Install only in environments where local token persistence is acceptable, and review or clear stored credentials according to local policy. <br>
Risk: Cry analysis output can be mistaken for medical advice. <br>
Mitigation: Present results as parenting support only, and direct users to seek medical care when crying is persistent or health concerns are present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-infant-cry-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files] <br>
**Output Format:** [Markdown report or JSON analysis result, with an optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a cloud-hosted report export link and cloud history query results when requested.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter lists 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
