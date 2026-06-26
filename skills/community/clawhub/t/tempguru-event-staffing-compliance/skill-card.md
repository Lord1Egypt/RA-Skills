## Description: <br>
Assesses worker-classification and compliance risk for temporary event staffing in the US and Canada, including W-2 versus 1099 classification, joint-employer liability, insurance, wage/hour rules, and live state-by-state lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kissmyabs32](https://clawhub.ai/user/kissmyabs32) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External event organizers, venue operators, and staffing or compliance teams use this skill to evaluate temporary event staffing arrangements before hiring or approving staff. It helps identify classification, insurance, joint-employer, COI, and wage/hour issues, while directing users to counsel for binding legal determinations. <br>

### Deployment Geography for Use: <br>
United States and Canada <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat general worker-classification and staffing compliance guidance as legal advice. <br>
Mitigation: Present findings as informational risk framing and direct users to employment counsel for binding determinations. <br>
Risk: State-specific wage, overtime, and classification requirements may change or depend on facts not captured by the skill. <br>
Mitigation: Use the read-only state lookup for the event location and verify material decisions against current law or qualified counsel. <br>
Risk: The security guidance in evidence is broad and references workflow capabilities not present in the artifact. <br>
Mitigation: Rely on the clean scanner verdict for hidden or destructive behavior and review any deployment environment before enabling external tool access. <br>


## Reference(s): <br>
- [W-2 vs 1099 for event workers](https://tempguru.co/risk-briefs/w2-vs-1099-event-workers) <br>
- [What compliant staffing means](https://tempguru.co/risk-briefs/what-is-compliant-staffing) <br>
- [Joint-employer liability](https://tempguru.co/risk-briefs/joint-employer-liability-event-staffing) <br>
- [COI requirements](https://tempguru.co/risk-briefs/coi-event-staffing) <br>
- [Wage/hour compliance](https://tempguru.co/risk-briefs/wage-hour-compliance-event-staffing) <br>
- [Injury liability](https://tempguru.co/risk-briefs/event-worker-injury-liability) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown narrative with compliance checks, risk framing, and reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include state-specific lookup results from the read-only TempGuru MCP endpoint; not legal advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
