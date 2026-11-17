## Description:

知乎内容搜索分析 helps agents search Zhihu topics and hot lists, rank content opportunities, and produce Chinese-first topic recommendations for creators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and media operators use this skill to find Zhihu questions, compare topic heat and answer competition, and identify questions worth answering or developing into content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided Zhihu search keywords are sent to Zhihu endpoints.

Mitigation: Avoid sensitive or confidential keywords and use the skill only when external Zhihu queries are acceptable.

Risk: The documented --analyze example appears unsupported by the included script.

Mitigation: Use the implemented --search, --hot, --topic, --limit, and --json options, or verify behavior before relying on --analyze.

Risk: Output is Chinese-focused and depends on Zhihu endpoint availability.

Mitigation: Review generated recommendations for audience fit and retry or fall back when Zhihu endpoints are unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/zhida-content)
- [Publisher profile](https://clawhub.ai/user/freedompixels)
- [Zhihu search endpoint](https://www.zhihu.com/api/v4/search_v3)
- [Zhihu hot list endpoint](https://api.zhihu.com/topstory/hot-lists/total)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Chinese-first text summaries with links, scores, command examples, and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided keywords to query Zhihu endpoints and rank questions by estimated heat and opportunity.]

## Skill Version(s):

1.2.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
