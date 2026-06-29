## Description: <br>
基于飞常准数据，提供航班实时动态、延误分析、舒适度评分、机场天气查询，覆盖全球航班，零配置即用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, support teams, and agents use this skill to check live flight status, route-level disruption, comfort comparisons, and airport weather impact using VariFlight data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends flight numbers, city or airport names, and dates to an external proxy and VariFlight API. <br>
Mitigation: Install only when that network use is expected, and use a dedicated least-privilege API token as recommended by the security guidance. <br>
Risk: Real-time flight and airport weather data can be delayed, unavailable, or incomplete. <br>
Mitigation: Treat results as planning guidance and verify critical travel decisions with the airline, airport, or official booking channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/variflight-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Markdown-style text tables and JSON-encoded command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include live flight status, route summaries, comfort scores, delay analysis, and airport weather impact notes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
