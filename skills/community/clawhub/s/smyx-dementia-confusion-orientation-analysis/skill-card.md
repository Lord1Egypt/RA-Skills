## Description: <br>
Analyzes fixed-camera dementia-care audio/video to identify confusion or disorientation behaviors, produce structured reports, query cloud report history, and support orientation-soothing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External care operators, developers, and caregivers use this skill to analyze dementia-care facility or home camera media for confusion/disorientation indicators, receive structured results and report links, and review cloud-hosted historical reports. It is framed as behavioral support and orientation assistance, not medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes dementia-care audio/video and cloud-hosted history that may be sensitive health or care-context data. <br>
Mitigation: Install only after confirming lawful consent, institution notice or opt-out where applicable, acceptable cloud upload/history use, report access controls, and retention expectations. <br>
Risk: The skill automatically creates or reuses a local user identity and uses account tokens for API access. <br>
Mitigation: Run it with a scoped operator account, protect workspace data and token storage, keep report access auditable, and revoke credentials when the deployment ends. <br>
Risk: Analysis results may trigger caregiver notifications or device actions such as speaker prompts and lighting adjustments. <br>
Mitigation: Configure caregiver oversight, escalation thresholds, action limits, audio volume, lighting intensity, and emergency workflows before production use. <br>
Risk: Behavioral recognition could be mistaken for clinical diagnosis or used beyond the documented support role. <br>
Mitigation: Use outputs as objective behavioral observations and orientation-support prompts only; route persistent or severe confusion events to qualified clinical or care professionals. <br>
Risk: Family voice recordings and soothing prompts can create consent, impersonation, or distress risks. <br>
Mitigation: Use only authorized pre-recorded family audio, prohibit AI-cloned voices, and avoid corrective or shaming prompts in caregiver-facing configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-dementia-confusion-orientation-analysis) <br>
- [API documentation](artifact/references/api_doc.md) <br>
- [Shared analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files] <br>
**Output Format:** [Markdown text with structured JSON report content, cloud report links, and optional saved output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports analysis of local files or URLs, cloud history listing, and basic, standard, or json detail modes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
