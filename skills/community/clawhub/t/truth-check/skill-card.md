## Description: <br>
Truth Check guides an agent to check generated content for hallucinations, fabricated details, and inaccurate information after producing technical content, statistics, people or event references, or code examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jack123255829](https://clawhub.ai/user/Jack123255829) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill as a post-generation verification workflow for checking factual claims, numeric statements, references, code examples, and external-operation results before relying on an answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may encourage source lookups or verification of external operations. <br>
Mitigation: Review any resulting tool calls as usual before allowing external access or changes. <br>
Risk: Fact-checking guidance can still miss subtle inaccuracies or unsupported claims. <br>
Mitigation: Treat the verification labels as decision support and review important claims against authoritative sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jack123255829/truth-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with verification labels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce VERIFIED, LIKELY, or UNCERTAIN confidence labels for checked outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
