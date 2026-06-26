## Description: <br>
Scene Analysis helps agents evaluate commercial scenarios through Gate0 strategic screening, Gate1 weighted scoring, and independent blue-force review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyf1986](https://clawhub.ai/user/yyf1986) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business reviewers, product leaders, and investment reviewers use this skill to assess a scenario's strategic dependency, core-process embedding, commercial score, risks, and final S/A+/A/B/C rating from user-provided evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outputs may be misleading when scenario evidence is incomplete or inferred. <br>
Mitigation: Treat results as advisory decision support and review the evidence basis before using ratings for business decisions. <br>
Risk: Scenario descriptions may contain confidential contracts, customer information, or internal process details. <br>
Mitigation: Avoid supplying sensitive business information unless the agent runtime is approved for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yyf1986/scene-analysis) <br>
- [Gate0 strategic screening standards](references/gate0-standards.md) <br>
- [Gate1 scoring rules](references/gate1-scoring-rules.md) <br>
- [Blue-force review process](references/blue-force-review.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style structured assessment report with scores, risk deductions, evidence notes, and a final rating.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Evidence-constrained advisory decision support; no code execution or external tool calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
