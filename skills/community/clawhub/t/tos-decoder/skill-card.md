## Description:

Decode a terms of service or privacy policy into what you're actually agreeing to, ranked by real-world impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review pasted terms of service or privacy policy text in plain language, prioritizing clauses by practical impact. It highlights issues such as data resale, arbitration and class-action waivers, unilateral changes, content licenses, deletion limits, and available opt-outs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat a plain-language terms or privacy policy reading as legal or financial advice.

Mitigation: Present the result as a plain-language aid and direct users to a qualified professional for decisions with legal or financial consequences.

Risk: Reviewing account terms or privacy policies may expose private account details if users paste unnecessary personal information.

Mitigation: Ask for the policy text and service context only; avoid collecting private account details unless they are necessary for the review.

Risk: The skill can miss high-impact clauses when the user provides only excerpts.

Mitigation: State which high-impact topics were not present in the supplied text instead of assuming they are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/tos-decoder)
- [ToS Decoder homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/tos-decoder.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with a bottom line, ranked findings table, deletion summary, action options, and disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should be grounded in provided ToS or privacy policy text and ranked by real-world impact.]

## Skill Version(s):

50.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
