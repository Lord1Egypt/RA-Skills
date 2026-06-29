## Description: <br>
Analyzes aquatic pet videos or video URLs with a remote API to identify fish health indicators, potential disease signs, care guidance, and historical report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and aquarium caretakers use this skill to submit aquatic pet videos or URLs for health analysis covering scales, fins, body color, activity level, possible diseases, and care recommendations. Agents can also use it to retrieve cloud-hosted historical health reports associated with the current account identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the skill sends aquarium videos or URLs, account-linked identifiers, and report-history requests to LifeEmergence services. <br>
Mitigation: Use only media and URLs appropriate for third-party processing, and review the provider's data handling and retention claims before deployment. <br>
Risk: The security review reports automatic identity creation or reuse and local storage of session tokens. <br>
Mitigation: Run in an isolated environment, restrict local file access for token storage, and clear stored credentials when the skill is no longer needed. <br>
Risk: The skill produces health analysis for aquatic pets and is not a substitute for professional veterinary diagnosis. <br>
Mitigation: Present outputs as advisory screening information and route serious or uncertain health concerns to a qualified aquatic veterinarian. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-aquarium-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API reference](references/api_doc.md) <br>
- [Analysis API reference](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON analysis results, report links, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local video files, remote video URLs, fish-type selection, basic/standard/JSON detail modes, and optional output files.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
