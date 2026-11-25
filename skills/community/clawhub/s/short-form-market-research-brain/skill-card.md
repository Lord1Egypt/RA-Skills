## Description:

Short-form video market research via the Virlo API: viral niche research, trend tracking, creator vetting, hashtag, sound, and hook intelligence across TikTok, YouTube Shorts, and Instagram Reels. Use when the user wants to research what's working in a niche, find rising creators, monitor trends, get viral hooks (opening lines) to model, or analyze social video performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virlo-ai](https://clawhub.ai/user/virlo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and researchers use the agent to study short-form video niches, discover rising creators and trends, evaluate hashtags, sounds, and hooks, and monitor performance across TikTok, YouTube Shorts, and Instagram Reels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics and keywords are sent to Virlo, and the skill requires a Virlo API key.

Mitigation: Avoid sending confidential research terms, store the API key in the agent's secret environment configuration, and review Virlo's data handling and prepaid pricing before use.

Risk: The security scan covered 10 of 11 components and could not resolve many local references, so its evidence is incomplete.

Mitigation: Review the skill and its referenced materials before installation, and confirm the manifest metadata is valid.

## Reference(s):

- [Virlo API Documentation](https://dev.virlo.ai/docs)
- [Virlo API Reference for Agents](https://dev.virlo.ai/llms-full.txt)
- [Virlo Pricing](https://dev.virlo.ai/pricing)
- [ClawHub release page](https://clawhub.ai/virlo-ai/skills/short-form-market-research-brain)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown research summaries, comparisons, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include metrics and links to source videos or Virlo research agents; some API actions use prepaid credits.]

## Skill Version(s):

1.36.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
