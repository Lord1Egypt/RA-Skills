## Description: <br>
Rubicon Sentinel v2 is an OpenClaw skill for web-sourced geopolitical sovereignty analysis, scoring countries and topics across eight pillars with quick scans, deep scans, comparisons, forecasts, memes, and tweet drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgmnemesis](https://clawhub.ai/user/lgmnemesis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and analysts use this skill to generate opinionated, source-backed sovereignty briefs, country comparisons, forecasts, claim rebuttals, and social-media-ready summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is strongly opinionated and its sovereignty scores may be mistaken for neutral intelligence. <br>
Mitigation: Treat scores as ideological commentary, check the cited sources, and review assumptions before relying on conclusions. <br>
Risk: The scoring rules and social-output modes can produce biased, inflammatory, or harassing roasts, memes, and tweet drafts. <br>
Mitigation: Review generated content before sharing, avoid private scan topics, and do not use outputs for decisions about protected or vulnerable groups. <br>
Risk: Optional X/Twitter sentiment lookup requires exposing a bearer token to the agent environment. <br>
Mitigation: Provide a Twitter bearer token only when sentiment lookup is intentionally needed, use least-privilege credentials, and remove the token afterward. <br>


## Reference(s): <br>
- [Rubicon Sentinel v2 - 8-Pillar Sovereignty Scoring Rubric](references/scoring.md) <br>
- [Rubicon Sentinel v2 - Smart Query Templates](references/queries.md) <br>
- [Rubicon Sentinel v2 - Marco Rubio Quotes](references/quotes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with tables, bullets, sourced findings, forecasts, quotes, and optional meme or tweet text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use web search and fetch results; optional image generation and X/Twitter sentiment lookup are skipped when unavailable.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
