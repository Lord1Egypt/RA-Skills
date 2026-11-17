## Description:

Compare LMNP furnished-rental taxation between micro-BIC and regime reel with amortization using Vestafolio's simulator API after collecting the simulator's required rental, tax, charge, and property inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect LMNP furnished-rental facts, submit approved inputs to Vestafolio's simulator, and explain whether micro-BIC or regime reel is more favorable. It is intended for French furnished-rental tax estimates, not professional tax advice.

### Deployment Geography for Use:

France

## Known Risks and Mitigations:

Risk: Personalized calculations send approved rental and tax inputs to Vestafolio's external API.

Mitigation: Review the summarized destination and fields before agreeing, decline API submission when needed, and avoid adding names, addresses, account identifiers, credentials, files, or conversation history.

Risk: The result may be mistaken for professional tax advice or may become stale as French tax rules change.

Mitigation: Treat outputs as estimates, check stated assumptions and dates, and consult a qualified tax professional for decisions.

## Reference(s):

- [Vestafolio LMNP simulator](https://www.vestafolio.com/simulateurs/lmnp-fiscalite)
- [Vestafolio LMNP API schema](https://www.vestafolio.com/api/tools/v1/lmnp-fiscalite)
- [ClawHub skill page](https://clawhub.ai/vestafolio/skills/vestafolio-lmnp-fiscalite)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose with optional shell command examples and API result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a recommended tax regime, annual and ten-year savings, per-regime tax figures, assumptions, limits, and links for manual simulation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
