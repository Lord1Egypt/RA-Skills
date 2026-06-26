## Description: <br>
Analyzes fixed-camera elder-care video, with optional audio, to estimate loneliness-related behavior signals, produce a loneliness index, and suggest warm companionship actions without making a medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and care-platform developers use this skill to analyze elderly living-space video or history reports, summarize behavior metrics, and recommend consent-based companionship follow-up for smart-aging scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive elder-care video, identities, and history reports through remote processing. <br>
Mitigation: Confirm the publisher, remote API operator, consent from the monitored elder and bystanders, retention/deletion terms, and history-report access controls before installation or use. <br>
Risk: The security review flags silent account/token handling, broad history access, and local token storage concerns. <br>
Mitigation: Use dedicated non-personal test identifiers first, avoid real phone numbers or private-room video until account creation and token storage are explicit, and restrict report access to authorized caregivers. <br>
Risk: Loneliness scoring and companionship actions could be mistaken for clinical mental-health diagnosis or automated care decisions. <br>
Mitigation: Treat outputs as behavior-based support signals only, keep the no-diagnosis boundary visible, and refer concerning cases to qualified elder mental-health or community-care professionals. <br>
Risk: Bundled artifacts include mismatched pet/medical implementation remnants and a dependency issue identified by the security guidance. <br>
Mitigation: Review and test the packaged scripts before deployment, fix dependency declarations, and remove unrelated artifacts that could confuse operators or reviewers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/smyx-elderly-loneliness-comfort-analysis) <br>
- [API interface documentation](artifact/references/api_doc.md) <br>
- [Analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown and JSON reports, with shell command examples for running the packaged scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include loneliness index, level, behavior metrics, comfort-action recommendations, history tables, and report links.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
