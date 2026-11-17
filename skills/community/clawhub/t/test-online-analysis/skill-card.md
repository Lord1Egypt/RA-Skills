## Description:

Online (real-time) data analysis, rule extraction, and pattern recognition for testing scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shineniefei](https://clawhub.ai/user/shineniefei)

### License/Terms of Use:

MIT

## Use Case:

Developers and QA engineers use this skill to analyze logs, API responses, streams, or database-derived data, extract business and technical rules, identify testing patterns, and produce anomaly reports or test case suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may analyze sensitive logs, API responses, streams, or database outputs.

Mitigation: Use sanitized test data where possible, avoid production secrets or regulated data, and confirm the scope of any live-source access before running analysis.

Risk: Extracted rules, test suggestions, and anomaly reports may be incorrect or incomplete if the input data is narrow, noisy, or unrepresentative.

Mitigation: Review generated findings against source systems, test requirements, and counterexamples before using them for test coverage decisions.

Risk: The skill depends on local Python execution and numpy for included analysis scripts.

Mitigation: Install pinned dependencies in an isolated environment before running the scripts.

## Reference(s):

- [Rule Extraction Standards](references/rule_extraction_standards.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/shineniefei/skills/test-online-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with command examples and structured rule, test case, or anomaly findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize findings in chat and offer exportable analysis files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
