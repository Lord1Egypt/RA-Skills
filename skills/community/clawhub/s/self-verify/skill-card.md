## Description: <br>
Automatically checks and verifies consequential claims before response to prevent confident errors and ensure accuracy and safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ariffazil](https://clawhub.ai/user/ariffazil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to self-check consequential or high-confidence answers before delivery. It guides source, uncertainty, contradiction, reversibility, and safety checks so claims are better supported and risks are surfaced. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may make answers more cautious or slower because it asks the agent to verify important claims before responding. <br>
Mitigation: Use it for consequential, high-confidence, quantitative, or disputed claims where the added verification step is worth the latency. <br>
Risk: The skill encourages use of configured search and memory tools for verification. <br>
Mitigation: Review available search and memory tools before deployment so verification queries use approved sources and data access paths. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional command snippets and verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Encourages source checks, memory checks, reasoning traces, confidence labels, and uncertainty labels before consequential claims are returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
