## Description: <br>
Threshold Keel provides safety guardrails for autonomous agents by classifying risky actions, requiring structured approval before irreversible operations, and supporting CLI-backed audit trails and policy checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andaltan](https://clawhub.ai/user/andaltan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users install Threshold Keel to add approval gates, action classification, and optional CLI or cloud audit trails before autonomous agents perform risky state-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is an agent-wide approval and audit layer, so users should only enable it when they want Keel to mediate risky agent actions. <br>
Mitigation: Install intentionally, review the approval workflow, and verify that the threshold-keel package is trusted before enabling CLI or cloud mode. <br>
Risk: CLI mode may store action metadata locally under ~/.keel/, and cloud mode may sync action metadata when KEEL_CLOUD_API_KEY is set. <br>
Mitigation: Keep cloud sync disabled unless the user has approved Threshold Cloud data handling, and review local audit storage expectations before use. <br>


## Reference(s): <br>
- [Threshold Keel ClawHub listing](https://clawhub.ai/andaltan/threshold-keel) <br>
- [Threshold Keel homepage](https://thresholdsignalworks.com/keel) <br>
- [Threshold Cloud overview](https://thresholdsignalworks.com/cloud) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use the local keel CLI for durable policy checks and audit trails, or provide behavioral guidance only when the CLI is unavailable.] <br>

## Skill Version(s): <br>
0.2.7 (source: server release metadata; artifact frontmatter lists 0.2.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
