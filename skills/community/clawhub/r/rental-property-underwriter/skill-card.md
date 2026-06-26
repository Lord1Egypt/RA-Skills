## Description: <br>
Use this skill when a real estate investor, agent, or analyst needs to underwrite a residential rental property such as a single-family, small multi-family, or short-term rental; it computes NOI, cap rate, cash-on-cash return, DSCR, a 5-year pro-forma, sensitivity results, and a go/no-go memo with deal-breaker flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External real estate investors, agents, and analysts use this skill to evaluate a residential rental opportunity before making an offer, renegotiating, or walking away. It guides intake, confirms assumptions, calculates underwriting metrics, stress-tests the deal, and produces a draft decision memo. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The intake can involve sensitive property identifiers, financing details, and personal capital information. <br>
Mitigation: Use a property code instead of a full address when discretion is needed, and avoid sharing unnecessary personal or loan details. <br>
Risk: The underwriting memo can be misleading if rent comps, taxes, insurance, HOA rules, STR regulations, or legal and tax assumptions are incomplete or stale. <br>
Mitigation: Independently verify rent comps, binding insurance quotes, taxes, HOA documents, STR eligibility, inspection findings, and legal or tax implications before acting on the memo. <br>
Risk: Users may mistake the draft underwriting memo for investment, tax, or legal advice. <br>
Mitigation: Keep the memo labeled as a draft underwriting aid and treat local broker, CPA, attorney, lender, and insurance review as required before an offer or financing decision. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown underwriting memo with tables and a GO / CONDITIONAL / NO-GO verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes formulas, a 5-year pro-forma, sensitivity matrix, deal-breaker flags, unresolved information, and a draft/non-advice reminder.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
