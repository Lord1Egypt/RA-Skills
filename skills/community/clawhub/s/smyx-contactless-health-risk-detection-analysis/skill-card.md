## Description: <br>
Combines frontal facial image capture with multimodal physiological feature analysis to provide early risk screening and alerts for chronic and acute conditions such as heart attack, stroke, hypertension, and hyperlipidemia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and care-support workflows can use this skill to submit frontal face images or short videos for non-contact early health risk screening and report lookup. Results are screening references and should not replace professional medical diagnosis or clinical examination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face images, videos, remote media URLs, identity metadata, and report-history queries may be sent to the lifeemergence cloud service. <br>
Mitigation: Use the skill only with consent, avoid submitting third-party faces or private videos without authorization, and use a dedicated test account or workspace when evaluating it. <br>
Risk: The skill can silently create or reuse a local identity, store tokens locally, and link health-screening reports to that identity. <br>
Mitigation: Review or clear the local data directory when identity reuse is not desired, and avoid using shared environments for sensitive screening sessions. <br>
Risk: Health-risk results are screening references and may be incomplete or misleading if treated as diagnosis. <br>
Mitigation: Treat outputs as early risk-screening guidance only and seek professional medical diagnosis or urgent care for high-risk results or symptoms. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-contactless-health-risk-detection-analysis) <br>
- [API Documentation](references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON analysis reports with risk findings, recommendations, report links, and history tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a remote cloud API for analysis and report-history retrieval.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
