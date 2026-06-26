## Description: <br>
Ruiping produces assertive Chinese-language news commentary by screening events, analyzing likely impacts, and turning them into decision-oriented opinion pieces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leslietong2046-ship-it](https://clawhub.ai/user/leslietong2046-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and content creators use this skill to turn supplied or searched news events into Chinese commentary with source summaries, short conclusions, impact analysis, forecasts, and practical recommendations. It is intended for opinionated decision support rather than neutral news reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally produces assertive opinion and decision recommendations, including investment, career, and current-events guidance. <br>
Mitigation: Treat recommendations as commentary, verify sources and facts independently, and avoid using the output as the sole basis for high-impact decisions. <br>
Risk: Search-style behavior and current-events analysis can rely on incomplete, stale, or incorrect source material. <br>
Mitigation: Check cited or summarized sources before publishing or acting on the analysis, especially for fast-moving news. <br>
Risk: The fixed commentary format may be unwanted for ordinary news questions after installation. <br>
Mitigation: Use explicit prompts when neutral summaries, raw facts, or a different response format are desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leslietong2046-ship-it/ruiping-skill) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Tesla price-cut example](examples/tesla-price-cut.md) <br>
- [AI regulation example](examples/ai-regulation.md) <br>
- [Python formatter reference](scripts/ruiping.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese-language Markdown commentary with source summary, conclusion, impact analysis, recommendations, and final comment.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include investment, career, consumer, or current-events recommendations; source claims and recommendations should be independently verified before reliance.] <br>

## Skill Version(s): <br>
2.0.4 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
