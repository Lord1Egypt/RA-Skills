## Description:

Analyzes A-share stocks and the broader A-share market across fundamentals, valuation, capital flows, technical indicators, chip distribution, and news or research signals to produce structured scores and operating suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derrors](https://clawhub.ai/user/derrors)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate A-share stock deep-dive reports or daily A-share market reviews with structured conclusions, risk alerts, and suggested trading posture. It is intended for analysis support only and the artifact states that results are not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A caller-controlled LLM endpoint could expose the configured LLM API key or send market, news, and prompt content to an unintended provider.

Mitigation: Install only in a trusted environment, restrict allowed LLM endpoints, and do not expose the handler to untrusted callers until configuration fields are allowlisted.

Risk: Saved reports may be written outside the intended reports folder when an unsafe output path is accepted.

Mitigation: Keep saved report paths under a known reports directory and validate or constrain output_dir before enabling report persistence.

Risk: Market data, news content, and user prompts may be transmitted to configured LLM and search providers.

Mitigation: Review configured providers, keys, and data-sharing expectations before use, and treat generated investment analysis as support material rather than financial advice.

Risk: Unpinned Python dependencies can change behavior across installs.

Mitigation: Pin dependency versions and review dependency updates before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/derrors/skills/stock-analysis-report)
- [Miaoxiang Skills Page](https://dl.dfcfs.com/m/itc4)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown reports and JSON objects with stock or market analysis fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save reports locally when requested; outputs include disclaimers and may include scores, suggested action, price levels, risk alerts, checklist items, news summaries, and raw LLM report text.]

## Skill Version(s):

1.0.9 (source: server release metadata, SKILL.md frontmatter, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
