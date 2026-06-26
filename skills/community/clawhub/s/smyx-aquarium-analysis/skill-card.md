## Description: <br>
Analyzes aquarium pet videos or URLs through a cloud API to produce fish and aquatic pet health reports covering scales, fins, color, activity, potential disease signs, and care suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External aquarium pet owners and agent users use this skill to submit local or URL-based aquatic pet media for cloud health analysis and to retrieve structured current or historical health reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aquarium videos, URLs, and an internal identity are sent to the provider's cloud service for analysis. <br>
Mitigation: Use only media and URLs intended for sharing with that provider, and avoid private or sensitive resources unless cloud processing is acceptable. <br>
Risk: The skill silently creates or reuses a user identity and stores session tokens locally with limited user control or disclosure. <br>
Mitigation: Run the skill in an isolated workspace, review whether local identity and token storage are acceptable, and clear workspace data when the skill is no longer needed. <br>
Risk: Aquatic pet health reports may be mistaken for a professional veterinary diagnosis. <br>
Mitigation: Treat reports as health-reference guidance and consult a qualified aquatic veterinarian before making medical or treatment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-aquarium-analysis) <br>
- [Skill demo](https://lifeemergence.com/guide.html) <br>
- [API interface documentation](references/api_doc.md) <br>
- [smyx_analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON health analysis reports, with optional saved text or JSON output files and report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Historical-report mode returns a Markdown table built from cloud API records.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
