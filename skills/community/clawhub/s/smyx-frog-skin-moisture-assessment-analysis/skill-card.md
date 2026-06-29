## Description: <br>
Assesses frog skin moisture from dorsal or lateral enclosure camera images or videos by analyzing skin glossiness, wrinkles, white film, species context, and image quality to produce dehydration-risk reports and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External amphibian keepers, amphibian farms, animal hospitals, and developers integrating vivarium cameras use this skill to submit frog skin images or videos, receive structured moisture and dehydration-risk assessments, and query account-linked historical reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends frog images or videos, submitted media URLs, and account-linked identifiers to the LifeEmergence cloud service. <br>
Mitigation: Install and use it only when cloud processing is acceptable; avoid private or signed URLs and avoid submitting sensitive media. <br>
Risk: The skill silently creates and reuses identity or session data for analysis and history-report lookup. <br>
Mitigation: Review whether local tokens or the default user database can be disabled or cleared, and treat history lookup as account-bound cloud access. <br>
Risk: Visual moisture assessment can be mistaken for veterinary diagnosis or treatment guidance. <br>
Mitigation: Keep outputs limited to visual moisture findings and non-prescriptive care prompts; do not provide drugs, doses, procedures, or diagnoses, and direct severe cases to a professional amphibian veterinarian. <br>
Risk: Poor image quality, recent misting, immersion, shedding, or missing species context can make glossiness and white-film signals unreliable. <br>
Mitigation: Require species and enclosure context where available, use clear 1080p dorsal or lateral images under even neutral light, exclude water or recent-misting frames, and return an unreliable result when signals are not trustworthy. <br>


## Reference(s): <br>
- [Frog Skin Moisture API Documentation](artifact/references/api_doc.md) <br>
- [Shared Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON analysis report with risk level, observed skin metrics, recommendations, and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a result file when --output is supplied and can list cloud-stored historical reports for the resolved user identity.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
