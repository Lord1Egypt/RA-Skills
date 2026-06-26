## Description: <br>
Real-Time Cost Guard helps agents analyze token-cost risks, identify runaway usage patterns, and plan external runtime protections before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[showmethemoney2023](https://clawhub.ai/user/showmethemoney2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when designing or reviewing AI workflows to spot cost-risk patterns, runaway loops, and missing budget controls. It supports planning for external enforcement rather than enforcing limits itself. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The marketplace summary may overstate real-time enforcement, causing users to rely on this skill for budget protection. <br>
Mitigation: Treat it as an educational checklist only and configure a separate runtime limiter before running workflows that need hard cost or token caps. <br>
Risk: AI workflows with retry loops, recursive calls, long chains, or missing stopping conditions can create uncontrolled token usage. <br>
Mitigation: Review workflows for token limits, session budget caps, maximum step counts, and timeout controls before execution. <br>


## Reference(s): <br>
- [Real-Time Cost Guard ClawHub page](https://clawhub.ai/showmethemoney2023/real-time-cost-guard) <br>
- [ClawFirewall](https://www.clawfirewall.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown checklist and advisory guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory only; it does not enforce token limits, budget caps, loop prevention, or request blocking.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
