## Description:

Uses the pywencai library to retrieve Tonghuashun Wencai stock data, including live quotes, financial indicators, Dragon-Tiger list data, capital flows, individual stock details, and sector or concept stock lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nnzenw](https://clawhub.ai/user/nnzenw)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agents use this skill to query China A-share market data from Wencai with natural-language stock questions and receive tabular results for reports, screening, monitoring, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example and troubleshooting code include unsafe execution patterns, including an SSL verification bypass.

Mitigation: Use the core search wrapper in a dedicated virtual environment, avoid running example.py as written, and do not disable SSL verification.

Risk: Unpinned or unreviewed dependencies can change behavior or introduce supply-chain risk.

Mitigation: Pin and review dependency versions before installing or deploying the skill.

Risk: Stock data depends on upstream Wencai and pywencai behavior and may fail, change shape, or require cookies.

Mitigation: Handle query failures, validate returned columns before downstream use, and review upstream API changes before relying on automated outputs.

## Reference(s):

- [PyWenCai API Reference](references/pywencai-api.md)
- [PyWenCai Query Examples](references/query_examples.md)
- [pywencai GitHub](https://github.com/stephanj/pywencai)
- [Tonghuashun Wencai](https://www.iwencai.com/)
- [ClawHub Skill Page](https://clawhub.ai/nnzenw/skills/pywencaistock)

## Skill Output:

**Output Type(s):** [Structured data, Text, Code]

**Output Format:** [pandas DataFrame returned by Python helper functions, with examples for CSV, Excel, and JSON export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result columns vary by Wencai query; some queries may require cookies or be affected by upstream API changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
