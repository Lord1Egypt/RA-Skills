## Description: <br>
Analyzes pet drying-box video files or video URLs through a remote service to detect early heat-stress signals such as open-mouth panting intensity, tongue color, and body movement frequency, then returns risk levels and intervention suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, pet grooming stores, pet hospitals, and developers use this skill to review pet drying-box footage for heat-stress warning signals and receive structured risk observations, safety suggestions, and report links. The output is a safety aid for drying operations, not a veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet drying-box videos or URLs are sent to the Life Emergence remote service for analysis, which may expose customer, clinic, or household footage. <br>
Mitigation: Use only with footage whose remote processing and storage terms are acceptable, and review the service's media and report retention practices before deployment. <br>
Risk: The skill silently creates or reuses internal user identity state and stores local account data and tokens. <br>
Mitigation: Deploy only in workspaces where local account and token storage is approved, and restrict access to the workspace data directory and local database. <br>
Risk: The skill returns heat-stress risk levels and intervention suggestions but does not provide veterinary diagnosis or treatment. <br>
Mitigation: Treat outputs as operational safety observations; stop drying and seek qualified veterinary help when the animal appears distressed or symptoms persist. <br>


## Reference(s): <br>
- [Pet Drying Box Heat Stress API Documentation](references/api_doc.md) <br>
- [Shared Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-pet-drying-box-heat-stress-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown text with structured JSON report content and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save the report text to a local output file when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter states 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
