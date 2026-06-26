## Description: <br>
Normalize messy Rolling Suds customer or salesperson inputs for exterior cleaning jobs into a clean intake summary, estimator-ready handoff, Workiz-friendly internal note, follow-up questions, and manual-review flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mwdearing](https://clawhub.ai/user/mwdearing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and estimating staff use this skill to turn messy Rolling Suds exterior-cleaning leads into concise intake summaries, Workiz-ready notes, follow-up questions, manual-review flags, and handoff text for estimating. <br>

### Deployment Geography for Use: <br>
St. Louis metro area, United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process customer lead details such as addresses, photos, and scheduling notes. <br>
Mitigation: Provide only customer information authorized for business intake and avoid adding unnecessary personal data. <br>
Risk: Generated Workiz notes or estimator handoffs can misstate messy or incomplete source input. <br>
Mitigation: Review generated notes before pasting them into Workiz or another estimator workflow. <br>
Risk: Missing Lead number or address can make a handoff look more complete than the source supports. <br>
Mitigation: Require the Lead number and address before treating the handoff as estimator-ready. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mwdearing/rolling-suds-customer-quote-intake) <br>
- [Default design](artifact/references/default-design.md) <br>
- [Version history](artifact/references/version-history.md) <br>
- [Iteration notes](artifact/references/iteration-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown with fixed intake, handoff, note, question, and manual-review sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces internal-use summaries and handoffs; no code execution or system access.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release evidence and artifact version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
