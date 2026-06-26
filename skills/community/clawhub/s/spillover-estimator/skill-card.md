## Description: <br>
Estimate whether one commerce channel is creating measurable spillover into another channel using simple exports, campaign timing, and directional evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leooooooow](https://clawhub.ai/user/Leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and commerce teams use this skill to compare source-channel activity with downstream channel performance and decide whether observed lift is likely related, weak, mixed, or unsupported by the available evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process channel exports or screenshots that contain unrelated customer details, account identifiers, payment data, or out-of-scope fields. <br>
Mitigation: Remove unrelated customer details, payment data, account identifiers, and fields outside the needed date range and channels before sharing data with the agent. <br>
Risk: Timing overlap between channels can be mistaken for causal attribution. <br>
Mitigation: Treat outputs as directional unless the user provides stronger measurement evidence, and keep confidence caveats with the recommendation. <br>


## Reference(s): <br>
- [Output template](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns an executive summary, spillover estimate, evidence blocks, confidence caveats, and a recommended next step.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
