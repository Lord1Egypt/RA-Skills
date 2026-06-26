## Description: <br>
Analyzes fixed-camera and optional microphone inputs in dementia care settings to identify confusion or disorientation signals, trigger orientation-soothing actions, and report observed events without making a medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External care teams, facility operators, and developers use this skill to analyze dementia-care audio/video inputs, call the remote analysis service, and produce structured confusion-event and orientation-soothing reports for caregiver review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive dementia-care video, audio, identity, and caregiver context through remote endpoints. <br>
Mitigation: Use only with documented consent from residents or legal representatives, clear facility notice, and a verified data-processing agreement before deployment. <br>
Risk: Server evidence flags cloud identity, credential storage, and remote endpoint handling for review. <br>
Mitigation: Confirm which endpoints receive video, audio, and identity data, then require secure token storage plus documented retention and deletion controls. <br>
Risk: Security evidence reports a mismatch between dementia-care behavior analysis and generic pet or health-analysis code paths. <br>
Mitigation: Remove or justify the mismatched code paths before deployment and validate that the service returns dementia-orientation outputs for the intended scenario. <br>
Risk: The skill can produce caregiver-facing recommendations in a sensitive health context. <br>
Mitigation: Treat outputs as observed behavior and orientation-support records only, require caregiver review, and do not use them as medical diagnosis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-dementia-confusion-orientation-analysis) <br>
- [Dementia orientation API documentation](references/api_doc.md) <br>
- [Common analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Markdown, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [JSON or Markdown report text, with optional saved output files and Markdown tables for history queries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authorized open-id and may use API credentials; outputs should be reviewed by caregivers and must not be treated as medical diagnosis.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
