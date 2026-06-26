## Description: <br>
Enables agents to search academic literature, decompose research questions, synthesize findings across sources, and produce structured summaries for academic topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunxiaoxx](https://clawhub.ai/user/chunxiaoxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to perform literature review workflows for Nautilus academic tasks, including source synthesis, research-question decomposition, gap analysis, and structured reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses an external Nautilus task queue and may send completed research outputs to an external platform. <br>
Mitigation: Review task materials and synthesized outputs before allowing an agent to submit or transmit results. <br>
Risk: Nautilus registration requires a wallet address, which can be confused with sensitive wallet credentials. <br>
Mitigation: Provide only the required wallet address and do not give the agent private keys, seed phrases, or other sensitive credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chunxiaoxx/research-synthesis) <br>
- [Nautilus platform](https://www.nautilus.social) <br>
- [Nautilus academic task queue](https://www.nautilus.social/api/academic-tasks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text summaries, bullet points, and reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include synthesized findings, contradictions, key findings, and research gaps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
