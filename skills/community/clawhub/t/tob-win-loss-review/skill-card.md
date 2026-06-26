## Description: <br>
Helps review lost ToB sales opportunities by using a local rules engine to turn industry, account size, sales stage, competitor, and key-event inputs into root-cause analysis, risk signals, and improvement guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[william202404](https://clawhub.ai/user/william202404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, solution, and revenue teams use this skill to perform structured win/loss reviews after a lost ToB opportunity. It produces a fixed Chinese report with project profile, ranked root causes, risk signals, and short-, medium-, and long-term improvement recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may enter sensitive customer or deal details while preparing a win/loss review. <br>
Mitigation: Provide only the deal context needed for review, avoid real customer identifiers where possible, and review generated reports before sharing them outside the sales team. <br>
Risk: Rules-based findings can be incomplete or misleading when the input omits buyer feedback, decision-chain context, or competitor details. <br>
Mitigation: Treat the report as a review aid, not a substitute for customer interviews or documented post-loss feedback. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/william202404/tob-win-loss-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Chinese Markdown-style report text, with optional formatted JSON when invoked with --json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline rules-based output; no network access, credential use, file modification, or persistence shown in the security evidence.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
