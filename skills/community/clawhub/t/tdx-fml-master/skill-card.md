## Description:

TDX Formula Master helps agents generate, validate, and explain TongDaXin stock-screening and indicator formulas from built-in templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g1776933879](https://clawhub.ai/user/g1776933879)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft TongDaXin stock formulas, check formula syntax, detect future functions, and generate common screening templates for further review in TongDaXin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated stock formulas may be treated as trading advice or assumed to be fully backtested.

Mitigation: Treat formulas as educational templates, verify them in TongDaXin, and perform independent strategy review before using them for screening or trading decisions.

Risk: TongDaXin functions such as WINNER, COST, and DYNAINFO can behave differently across versions or during historical backtests.

Mitigation: Review validator warnings, test formulas with non-future-function implementations such as REF(C,1), and confirm behavior in the target TongDaXin environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g1776933879/skills/tdx-fml-master)
- [Publisher profile](https://clawhub.ai/user/g1776933879)
- [Node.js runtime](https://nodejs.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with TongDaXin formula code blocks and optional local CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated formulas and validation results should be reviewed in TongDaXin before trading or screening use.]

## Skill Version(s):

2.2.1 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
