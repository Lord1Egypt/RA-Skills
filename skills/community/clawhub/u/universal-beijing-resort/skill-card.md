## Description: <br>
零配置即装即用，提供7项游园工具，含实时排队查询和智能推荐下一步，基于themeparks.wiki实时数据与本地预设数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External park visitors and travel planners use this skill to ask for Universal Beijing Resort wait times, operating hours, show guidance, dining suggestions, ticket estimates, route plans, and next-step recommendations. <br>

### Deployment Geography for Use: <br>
Global; content is specific to Universal Beijing Resort in Beijing, China. <br>

## Known Risks and Mitigations: <br>
Risk: Real-time wait-time and schedule answers depend on themeparks.wiki public data and may be delayed, unavailable, or different from on-site conditions. <br>
Mitigation: Use the skill for planning support and verify current hours, showtimes, and wait times with official Universal Beijing Resort sources before acting. <br>
Risk: Built-in ticket, dining, route, attraction, and height-limit reference data can become outdated. <br>
Mitigation: Confirm prices, age and height restrictions, attraction availability, and safety constraints with official park sources, especially for children or guests with accessibility needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/universal-beijing-resort) <br>
- [themeparks.wiki live park data endpoint](https://api.themeparks.wiki/v1/entity/68e1d8f0-ed42-4351-af25-160421e37ce0/live) <br>
- [themeparks.wiki park schedule endpoint](https://api.themeparks.wiki/v1/entity/68e1d8f0-ed42-4351-af25-160421e37ce0/schedule) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese text with lightweight Markdown-style sections and lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool responses may include live public park data when themeparks.wiki is reachable and local reference data otherwise.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; script header still states v1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
