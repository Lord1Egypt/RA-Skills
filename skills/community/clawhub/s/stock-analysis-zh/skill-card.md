## Description:

Analyzes stocks and crypto assets through AISA, returning scores, BUY/HOLD/SELL signals, confidence, and risk notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request live-data stock or cryptocurrency analysis, compare tickers, and summarize market position with scores, signals, confidence, and risks. It is informational only and not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AISA_BASE_URL can redirect the AISA API key and analysis request to another compatible endpoint.

Mitigation: Keep AISA_BASE_URL unset unless intentionally using a trusted endpoint; run in a minimal environment with only the required AISA_API_KEY.

Risk: Generated financial analysis may be incorrect or misleading.

Mitigation: Treat outputs as informational, verify data independently, and do not use the skill as financial advice.

Risk: The Python dependency range is broad and may change behavior over time.

Mitigation: Pin dependencies before routine or managed use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis by default, with optional fenced JSON summary from the bundled Python client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; may send ticker symbols and generated analysis prompts to an external AISA-compatible API.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
