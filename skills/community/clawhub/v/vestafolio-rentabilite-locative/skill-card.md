## Description:

Compute gross and net rental yield and monthly cash-flow for a French buy-to-let investment from acquisition cost, rent and annual charges using Vestafolio's simulator API, after asking the simulator's questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to estimate rental profitability for French buy-to-let investments by collecting simulator inputs, obtaining consent, calling Vestafolio's API, and explaining gross yield, net yield, and monthly cash-flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Property-investment assumptions are sent to Vestafolio's external API.

Mitigation: Summarize the exact simulator fields and values, obtain the user's agreement, and omit unused optional data, names, addresses, credentials, files, and conversation history.

Risk: Rental-yield outputs may be mistaken for a complete investment recommendation.

Mitigation: Ground the answer in the API result and state the limits, including that financing and rental-income taxation are excluded.

Risk: Network or API failure could otherwise lead to unsupported numerical results.

Mitigation: Use only a successful POST response with ok=true and result present; if execution or the API is unavailable, say the calculation could not be completed.

## Reference(s):

- [Vestafolio Rental Yield API](https://www.vestafolio.com/api/tools/v1/rentabilite-locative)
- [Vestafolio Rental Yield Simulator](https://www.vestafolio.com/simulateurs/rentabilite-locative)
- [Vestafolio Website](https://www.vestafolio.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown response with API-derived rental-yield figures and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls Vestafolio's API only after user consent; no credentials required.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
