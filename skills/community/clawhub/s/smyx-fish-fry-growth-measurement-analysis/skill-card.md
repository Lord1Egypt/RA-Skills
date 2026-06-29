## Description: <br>
Measures fish fry body length and growth rate from tank images or videos that include a known-size reference object, then returns structured growth reports, curve data, and management suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External aquaculture operators, ornamental fish breeders, laboratory users, and agents use this skill to analyze fish fry images or videos, calibrate measurements against a reference object, and produce growth-rate reports with non-diagnostic management guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically creates or reuses a user identity and stores account tokens locally. <br>
Mitigation: Review the local data directory for the SQLite token store, avoid shared or unmanaged workspaces, and remove retained identity data when the skill is no longer needed. <br>
Risk: Fish tank media, URLs, report history, and analysis requests are sent to the publisher's cloud APIs. <br>
Mitigation: Use only intended fish tank images or videos, avoid sensitive unrelated media or URLs, and run the skill in an environment where outbound network access can be audited. <br>
Risk: Growth measurements can be misleading when the reference object is missing, poorly detected, or not on the same plane as the fish fry. <br>
Mitigation: Require a clear known-size reference object, top-down capture, adequate resolution, and a retake when confidence, posture, occlusion, or perspective checks make measurement unreliable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-fry-growth-measurement-analysis) <br>
- [API Interface Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Reference](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown report text or JSON structured analysis; optional file output when --output is supplied.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes report links and historical report lists when cloud APIs return them.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
