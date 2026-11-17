## Description:

Fetches recent Twitter/X activity from AI-focused KOLs, identifies hot topics, and generates strategic internal briefing reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryder-mhumble](https://clawhub.ai/user/ryder-mhumble)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and operators use this skill to monitor AI-related Twitter/X KOL activity, cluster emerging topics, and produce Markdown internal briefing reports with strategic analysis and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A fallback Twitter API credential may be used when user configuration is absent.

Mitigation: Remove and rotate the embedded credential, and require user-supplied secrets through configuration or environment variables before installation.

Risk: Tweet data and generated prompts are sent to OpenRouter for opportunity detection and report generation.

Mitigation: Require explicit user consent for third-party LLM processing and avoid submitting sensitive or private source data.

Risk: The documentation claims temporary files are deleted, while the scripts write intermediate JSON files under temporary paths for reuse.

Mitigation: Use a private temporary directory, add cleanup after execution, and update the documentation so retention behavior is accurate.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ryder-mhumble/skills/twitter-ai-kol-fetcher)
- [KOL account list](references/kol_list.json)
- [LLM prompt templates](references/llm_prompts.md)
- [Internal report template](references/internal_report_template.md)
- [TwitterAPI.io](https://twitterapi.io)
- [OpenRouter settings](https://openrouter.ai/settings)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with supporting JSON topic data and console text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes intermediate tweet and topic JSON to temporary paths and returns up to three selected briefing reports per run.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
