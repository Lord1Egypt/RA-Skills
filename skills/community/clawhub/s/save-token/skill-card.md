## Description: <br>
Save Token is a documentation-only guidance skill that helps agents reduce repeated context by summarizing older conversation, referencing prior reads, deduplicating repeated blocks, and compressing long outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesilsin-netizen](https://clawhub.ai/user/yesilsin-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other agent users use this skill when conversation context is long or repeated content is increasing token cost. It guides the agent to summarize, reference prior material, deduplicate repeated blocks, and compress verbose outputs before continuing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarization or deduplication can omit details needed for legal, security, debugging, compliance, or other precision-sensitive work. <br>
Mitigation: For precision-sensitive tasks, explicitly tell the agent to preserve important details or re-read source material instead of relying only on summaries. <br>
Risk: The skill provides guidance only and does not directly modify runtime context or guarantee exact savings. <br>
Mitigation: Treat token-saving actions as agent-applied recommendations and review the optimization summary before relying on the result. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown guidance with examples and concise optimization summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code; agent applies the strategies and may report estimated token savings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
