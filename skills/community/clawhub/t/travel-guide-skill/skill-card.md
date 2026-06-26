## Description: <br>
出游攻略助手根据目的地、日期、人员和预算，通过实时网络查询生成包含机票、酒店、行程、交通、美食和天气的旅行攻略，并要求关键价格和时间标注来源。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wendyhufh](https://clawhub.ai/user/wendyhufh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to collect travel requirements and produce a sourced itinerary with transportation, lodging, dining, weather, budget, and local guidance. It is intended for planning support and asks users to verify booking, visa, schedule, price, and opening-hour details before travel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel prices, schedules, visa notes, opening hours, and weather can change or be inaccurate after lookup. <br>
Mitigation: Verify booking, visa, schedule, price, and opening-hour details with official providers before purchasing or traveling. <br>
Risk: Trip planning may share destination, dates, departure city, group size, and budget with the assistant or external search and booking sources. <br>
Mitigation: Share only the trip details needed for planning and avoid unnecessary sensitive personal information. <br>
Risk: If current data cannot be retrieved, generated recommendations may rely on estimates or planning references. <br>
Mitigation: Label unavailable or estimated values clearly, provide user-checkable sources, and avoid inventing flight numbers, hotels, restaurants, or exact prices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wendyhufh/travel-guide-skill) <br>
- [Guide template](references/guide-template.md) <br>
- [Budget template](references/budget-template.md) <br>
- [Question library](references/questions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown travel guide with tables, source notes, budget breakdowns, itinerary options, and follow-up prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires source and query-time labels for current prices, schedules, weather, and venue details; estimates must be labeled as estimates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and package.json report 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
