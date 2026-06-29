## Description: <br>
Analyzes seedling tray images or videos with AI object detection to identify emerged seedlings, count germinated seeds, estimate germination rate, and return structured report output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, growers, seed testers, and developers use this skill to analyze seedling tray images or videos, estimate germination rates, review low-rate alerts, and query prior cloud reports. The skill is intended for visual counting and reference reporting, not agricultural growing advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that seedling images or video URLs may be sent to the lifeemergence.com cloud service. <br>
Mitigation: Use only inputs approved for cloud processing, and avoid submitting sensitive or proprietary imagery unless that service is acceptable for the deployment. <br>
Risk: The security scan reports automatic cloud identity use, identity-linked history lookup, and local token or profile storage with limited user control. <br>
Mitigation: Review or disable identity persistence and history lookup paths when explicit consent, short retention, or local-only operation is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-seed-germination-rate-prediction-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Seed germination API documentation](references/api_doc.md) <br>
- [Analysis API error documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands] <br>
**Output Format:** [Markdown or JSON-style structured analysis report with optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include germinated seed counts, germination-rate estimates, history tables, low-rate alerts, and report links.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release metadata; frontmatter lists 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
