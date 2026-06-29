## Description: <br>
Helps an agent trace downstream consequences of a decision, including actor responses, feedback loops, reversals, consensus checks, and confidence decay. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to pressure-test decisions where the immediate outcome is clear but downstream effects, incentives, or reversals are uncertain. It can run a concise consequence cascade or coach a user through the same reasoning step by step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Second-order analysis can become misleading when the causal model is weak or the chain extends beyond grounded evidence. <br>
Mitigation: Use the skill's stop rule, name actor incentives at each hop, and state where confidence turns speculative. <br>
Risk: The artifact includes an external promotional link. <br>
Mitigation: Review external links before following them and rely on the ClawHub skill page for publisher context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/second-order-thinking) <br>
- [Sources - second-order-thinking](references/sources.md) <br>
- [Method in Action: US Prohibition (1920-1933)](examples/us-prohibition-1920.md) <br>
- [Howard Marks, I Beg to Differ](https://www.oaktreecapital.com/insights/memo/i-beg-to-differ) <br>
- [Economics in One Lesson](https://en.wikipedia.org/wiki/Economics_in_One_Lesson) <br>
- [U.S. National Archives: Amendments 11-27](https://www.archives.gov/founding-docs/amendments-11-27) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text response with a Consequence Cascade] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pause for user input in coach mode; otherwise produces a concise analysis with stop point and confidence notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
