## Description: <br>
Determines nine TCM constitution types from facial photos, videos, or URLs and returns constitution scores, tendencies, health-risk notes, and personalized TCM wellness suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit a face image, video, or media URL for TCM constitution analysis and to retrieve prior analysis reports. The results are wellness-oriented and should not be treated as a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face photos, videos, URLs, and report history are sent to the Life Emergence service and linked to a persistent local/backend identity. <br>
Mitigation: Get explicit user consent before analysis or history lookup, avoid submitting unnecessary personal media, and confirm the publisher's retention and deletion controls before routine use. <br>
Risk: The skill provides TCM wellness analysis that could be mistaken for medical diagnosis or treatment advice. <br>
Mitigation: Present results as wellness reference only and direct users with health concerns to qualified medical professionals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-tcm-constitution-recognition-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, JSON, shell commands, files] <br>
**Output Format:** [Markdown or JSON analysis reports, Markdown tables for history listings, and optional saved output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local image/video paths or media URLs and can query report history through the service API.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
