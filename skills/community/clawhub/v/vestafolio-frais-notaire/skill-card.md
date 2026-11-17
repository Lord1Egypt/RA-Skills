## Description:

Computes French property purchase notary fee estimates by acquisition type, department, first-time-buyer status, and optional mortgage costs using Vestafolio's simulator API after user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents assisting French property buyers use this skill to estimate closing costs, compare ancien and neuf fee differences, and explain the fee breakdown. The skill asks for the required purchase parameters and obtains approval before sending them to Vestafolio's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User purchase parameters are sent to Vestafolio's external API.

Mitigation: Disclose the destination and exact fields, obtain explicit approval, omit non-essential data, and offer the manual simulator if the user declines.

Risk: A notary-fee estimate may be mistaken for definitive tax or legal advice.

Mitigation: State assumptions and limits, ground the answer in the API result, and explain that the final amount is fixed by the notary at signing.

Risk: Network failures, API errors, or schema changes could make a calculation unreliable.

Mitigation: Fetch the canonical schema first, check HTTP success and the API success envelope, and report that the calculation could not be completed instead of inventing a result.

## Reference(s):

- [Vestafolio frais de notaire API schema](https://www.vestafolio.com/api/tools/v1/frais-notaire)
- [Vestafolio frais de notaire simulator](https://www.vestafolio.com/simulateurs/frais-notaire)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown response with fee totals, breakdowns, assumptions, caveats, and optional command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before transmitting purchase parameters; no credentials are required.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter reports 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
