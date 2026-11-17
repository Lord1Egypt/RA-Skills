## Description:

Use Valyu (valyu.ai) to search the web, extract content from web pages, answer with sources, and do deepresearch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unicodeveloper](https://clawhub.ai/user/unicodeveloper)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to run Valyu-backed web, news, academic, financial, patent, content extraction, answer, and deep research workflows with source-aware results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries, URLs, and supported file content may be sent to Valyu.

Mitigation: Use the skill only for data you are comfortable sharing with Valyu, and avoid submitting sensitive or restricted content unless approved for that workflow.

Risk: VALYU_API_KEY can be exposed if pasted into chat, command history, logs, or saved through the setup command.

Mitigation: Configure VALYU_API_KEY through the Gateway environment or another secure secret mechanism; use the setup command only if plaintext storage in ~/.valyu/config.json is acceptable.

## Reference(s):

- [Valyu Docs](https://docs.valyu.ai)
- [Search API Reference](https://docs.valyu.ai/api-reference/endpoint/search)
- [Contents API Reference](https://docs.valyu.ai/api-reference/endpoint/contents)
- [Answer API Reference](https://docs.valyu.ai/api-reference/endpoint/answer)
- [DeepResearch Guide](https://docs.valyu.ai/guides/deepresearch)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON responses and Markdown reports with citations, plus setup and command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and VALYU_API_KEY; API use can send research queries, URLs, and supported file content to Valyu.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
