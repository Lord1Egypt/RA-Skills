## Description: <br>
Analyze a product from name plus platform, read public reviews, and turn evidence into a practical buying recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and buying researchers use this skill to evaluate products from public review evidence, identify recurring complaints, and get a practical buy, avoid, or caveated recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Buying recommendations may be incomplete or misleading when public reviews are blocked, sparse, promotional, or mixed across product variants. <br>
Mitigation: State what review evidence was actually accessible, switch to a low-confidence limited conclusion when evidence is weak, and tell the buyer what to verify before ordering. <br>
Risk: Users may treat shopping guidance as a guarantee of product quality or seller reliability. <br>
Mitigation: Frame recommendations as shopping research, include confidence, and avoid promising outcomes beyond the visible review evidence. <br>
Risk: Review analysis could involve sensitive shopping context if users provide private account, order, or payment details. <br>
Mitigation: Use public review content where possible and avoid requesting private account details, order history, or payment information unless separately necessary for the user's own task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/review-buying-advisor) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/harrylabsj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown recommendation with verdict, evidence summary, buyer fit, risks, verification points, final advice, and confidence.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should distinguish accessible review evidence from unavailable or incomplete review access and lower confidence when evidence is weak.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
