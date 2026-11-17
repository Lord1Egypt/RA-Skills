## Description:

This skill helps an agent use the configured turing-shikuan-mcp service to identify a product image's category, brand, series, and brief product information, while avoiding authenticity, quality, or value judgments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyyyyyaa](https://clawhub.ai/user/xyyyyyaa)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure turing-shikuan-mcp and return structured product-recognition results from accessible image URLs. It is intended for product identification only, not counterfeit detection, authenticity assessment, quality assessment, or valuation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses API key and secret values and may expose credentials if shell history, logs, or process command lines are retained.

Mitigation: Use scoped or revocable credentials, avoid committing secrets, and rotate the key and secret if the environment may have logged them.

Risk: The setup script installs the global npm helper mcporter if it is not already available.

Mitigation: Review the setup script before running it, avoid sudo where possible, and confirm the global install is acceptable for the environment.

Risk: The skill depends on a third-party MCP endpoint for product-recognition results.

Mitigation: Confirm the Turing MCP endpoint is trusted and available before use, and do not fabricate results when the MCP service is unavailable or returns incomplete data.

Risk: Users may ask for authenticity, quality, or value judgments that are outside the skill's stated purpose.

Mitigation: Keep responses limited to product recognition and explicitly state that outputs are not counterfeit, authenticity, quality, or valuation conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xyyyyyaa/skills/turing-shikuan-skill)
- [turing-shikuan-mcp endpoint](https://turing-mcp-server-test.turingsenseai.com/mcp)
- [ClawHub publisher profile](https://clawhub.ai/user/xyyyyyaa)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured bullet lists and inline shell or JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product-recognition responses use category, brand, series, summary, and an explicit note that results are not authenticity conclusions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
