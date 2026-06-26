## Description: <br>
Self-correction helps an agent detect Chinese user objections or correction cues and re-analyze the user's original intent before producing a fresh answer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hauxu](https://clawhub.ai/user/hauxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to handle Chinese feedback that says the previous answer misunderstood the request. It guides the agent to revisit the original user intent, identify likely misunderstanding points, and provide a fresh answer or brief clarification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Chinese trigger phrases may activate self-correction when the user is adding context rather than rejecting the previous answer. <br>
Mitigation: Review behavior in the target agent and narrow or disable triggers such as "还有", "但是", "等等", and broad negations when false activations are costly. <br>
Risk: Bundled packaging utilities operate on local skill directories. <br>
Mitigation: Run the included scripts only on directories intended for packaging and review generated packages before sharing or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hauxu/self-correction) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown text with structured sections and optional code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language correction workflow; may trigger on broad negations and common phrases such as "还有", "但是", and "等等".] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
