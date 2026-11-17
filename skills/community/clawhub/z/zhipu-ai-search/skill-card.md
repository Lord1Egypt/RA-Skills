## Description:

ZhiPu Search calls the Zhipu Web Search API with multiple search engine options and returns structured results suitable for agent processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hulinying](https://clawhub.ai/user/hulinying)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run web searches through Zhipu, tune search engine and freshness options, and return JSON search results for downstream reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Zhipu's Web Search API.

Mitigation: Avoid submitting sensitive or regulated information as search queries unless that disclosure is approved for the deployment.

Risk: The skill requires a Zhipu API key and can read it from an environment variable or config.json.

Mitigation: Prefer ZHIPU_API_KEY, keep config.json out of shared skill directories, and do not add unrelated secrets to the skill directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hulinying/skills/zhipu-ai-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON search result output with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ZHIPU_API_KEY environment variable or local config.json API key; search queries are sent to Zhipu's Web Search API.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
