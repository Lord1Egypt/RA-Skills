## Description: <br>
旅行场景美食推荐与餐饮规划助手；帮旅行者找景点周边餐厅、当地必吃特色、生成多日餐饮计划。当用户需要查找旅行目的地美食、景点附近餐厅、当地特色菜、旅行饮食建议或规划旅途餐饮时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to find restaurants near attractions or hotels, identify local specialties, and produce multi-day dining plans for a destination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live restaurant searches send place names, addresses, cuisine keywords, and nearby-search parameters to the skill publisher's proxy-backed map service. <br>
Mitigation: Use only when that data sharing is acceptable, avoid entering sensitive itinerary details, and keep PROXY_TOKEN limited to this skill's proxy use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/travel-food-guide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Natural-language guidance, usually Markdown, based on JSON returned by the skill script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include restaurant lists, local specialties, dining tips, and multi-day meal plans.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
