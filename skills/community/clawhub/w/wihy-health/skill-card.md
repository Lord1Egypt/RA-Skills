## Description: <br>
Fact-check health and nutrition claims using the WIHY research knowledge base. Returns science-backed answers with citations from peer-reviewed sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kortney-lee](https://clawhub.ai/user/kortney-lee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to check health and nutrition claims, ask what research says about a topic, and receive concise answers with peer-reviewed citation links when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Health and nutrition questions are sent to WIHY's external API. <br>
Mitigation: Avoid including names, medical record details, account identifiers, or highly personal medical history unless the user trusts the provider and its privacy practices. <br>
Risk: Some answers may be returned without citations from the service. <br>
Mitigation: Tell the user when no citations were returned and keep the response factual and neutral. <br>


## Reference(s): <br>
- [Wihy Health Skill Page](https://clawhub.ai/kortney-lee/wihy-health) <br>
- [WIHY](https://wihy.ai) <br>
- [WIHY Ask API](https://ml.wihy.ai/ask) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with source links when citations are returned] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include citation links, a mixed-evidence note for low confidence, and optional follow-up questions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
