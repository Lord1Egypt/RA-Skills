## Description: <br>
Point-in-time Buffett-style company analysis for stocks, Berkshire case studies, and BUY/PASS verdicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yixiao1032-publish](https://clawhub.ai/user/yixiao1032-publish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, finance researchers, and agent operators use this skill to produce structured Buffett/Graham underwriting memos, moat tests, control-group comparisons, and benchmark backtests from cached company cards and point-in-time public evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BUY/PASS outputs may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as research, review assumptions independently, and keep personalized investment decisions outside the skill. <br>
Risk: Maintenance workflows may fetch public filings or write local research files. <br>
Mitigation: Run maintenance commands only intentionally and review generated file changes before relying on or committing them. <br>
Risk: Private documents used with corpus or evolution workflows could influence the local framework. <br>
Mitigation: Use those workflows only with documents intended to shape the local research corpus. <br>
Risk: The local preview server is intended for trusted environments. <br>
Mitigation: Use the preview server only on trusted networks and avoid exposing it publicly. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/yixiao1032-publish/think-like-warren-buffett) <br>
- [Skill instructions](SKILL.md) <br>
- [Framework overview](README.md) <br>
- [Coverage scope](coverage_scope.md) <br>
- [Methodology audit](methodology_audit.md) <br>
- [Gate review](gate_review.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with structured verdict blocks and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference cached company-card JSON and, when maintenance workflows are explicitly used, write local research files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
