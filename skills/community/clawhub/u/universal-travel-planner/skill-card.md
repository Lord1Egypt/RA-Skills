## Description: <br>
通用商旅出行规划助手 helps plan business trips with transport comparisons, hotel price checks, budget estimates, destination details, and generated HTML itinerary reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business travelers and assistants use this skill to compare rail, flight, route, hotel, weather, and budget options before a trip. It can produce a structured itinerary and an HTML report with booking and navigation links for user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use third-party travel, map, search, and booking services, so trip details may be sent to external providers during planning. <br>
Mitigation: Avoid entering confidential meeting details or sensitive travel plans unless sharing them with those services is acceptable. <br>
Risk: Generated booking and navigation links may be incomplete, stale, or not the best available option. <br>
Mitigation: Review all prices, routes, times, terms, and destination details on the provider site before booking or traveling. <br>
Risk: Generated HTML reports can save or share itinerary details. <br>
Mitigation: Store and share reports only in locations appropriate for the sensitivity of the trip information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/universal-travel-planner) <br>
- [12306 rail ticket service](https://www.12306.cn/) <br>
- [Amap REST API](https://restapi.amap.com/v3/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or HTML report content with itinerary tables, budget breakdowns, booking links, and optional MCP/API configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated HTML files and external travel, map, search, or booking links for user review.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
