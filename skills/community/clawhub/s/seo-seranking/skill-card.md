## Description:

SE Ranking AI visibility analyst (extension). Tracks AI Share-of-Voice across ChatGPT, Gemini, Perplexity, AI Overviews, and AI Mode in a single query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External SEO practitioners and marketing teams use this skill to query SE Ranking for AI visibility, organic SERP positions, backlink profiles, and competitor keyword gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to inspect ~/.claude/settings.json, which may expose unrelated local configuration or secrets to the agent context.

Mitigation: Check only whether SERANKING_API_KEY is available in the environment, avoid reading broad settings files into context, and review the skill before installation.

## Reference(s):

- [SE Ranking API documentation](https://seranking.com/api.html)
- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-seranking)
- [ClawHub publisher profile](https://clawhub.ai/user/asale-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command-style examples and SEO analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an SE Ranking API key and may report percentage-based share-of-voice metrics with confidence notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
