## Description:

Fetches WeChat Official Account reading-growth rankings by date and returns a Markdown ranking table with optional trend analysis grounded in the same API output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, editors, and researchers use this skill to fetch recent WeChat Official Account reading-growth rankings, inspect linked representative articles, and request concise pattern analysis based on the returned ranking data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read shell profile files to locate REDFOX_API_KEY and uses that key for RedFox API access.

Mitigation: Prefer a scoped secret or temporary environment variable, avoid storing keys in broad shell profiles, and rotate or revoke the key if exposure is suspected.

Risk: Broad or ambiguous prompts may activate the ranking workflow unexpectedly.

Mitigation: Use explicit WeChat ranking requests and confirm the intended date before allowing network-backed ranking retrieval.

Risk: Generated Markdown output can contain external article links.

Mitigation: Review links before clicking and verify important claims against the original article or returned API data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/if530770/skills/wechat-growth-ranking)
- [Core workflow](references/core_workflow.md)
- [API specification](references/api-spec.md)
- [RedFoxHub](https://redfox.hk?source=clawhub)
- [RedFoxHub API keys](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown ranking table with optional Markdown analysis and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranking queries are limited to the most recent 30 days; script stdout is intended to be shown verbatim and not rewritten.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
