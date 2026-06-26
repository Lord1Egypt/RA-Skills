## Description: <br>
Retrieves Tonghuashun stock theme, concept-sector, and popularity-ranking data and helps generate Markdown reports for individual A-share stocks or popularity lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinelp100](https://clawhub.ai/user/shinelp100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-data users can query Tonghuashun/Iwencai pages for a stock's themes, regional and business details, or a current popularity ranking, then produce JSON or Markdown summaries. Returned market data should be treated as informational rather than investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock codes and ranking queries may be sent to third-party Tonghuashun or Iwencai pages. <br>
Mitigation: Use the skill only with data that is appropriate to submit to those public websites. <br>
Risk: Returned stock themes, prices, rankings, and popularity values may be incomplete, delayed, or unsuitable for financial decisions. <br>
Mitigation: Treat results as informational market data and verify important conclusions against authoritative financial sources. <br>
Risk: Changes to third-party page structure can cause missing or incorrectly parsed fields. <br>
Mitigation: Review generated reports for empty or inconsistent values and update selectors or parsing notes when website layouts change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shinelp100/ths-stock-themes) <br>
- [Implementation notes](references/implementation.md) <br>
- [Tonghuashun stock pages](https://stockpage.10jqka.com.cn/) <br>
- [Iwencai popularity ranking query](https://www.iwencai.com/unifiedwap/result?w=%E4%B8%AA%E8%82%A1%E4%BA%BA%E6%B0%94%E6%8E%92%E5%90%8D) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports, JSON data, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes timestamps and source labels when producing stock theme or popularity data.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
