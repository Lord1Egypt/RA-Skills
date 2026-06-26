## Description: <br>
根据用户输入的多个目的地，生成推荐的旅行路线规划。当用户需要提供多城市旅行路线建议、行程规划、交通方式推荐时使用此技能。适用于自由行规划、多目的地旅行、跨区域旅行等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yufish-w](https://clawhub.ai/user/yufish-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and agents use this skill to plan multi-destination trips, compare route order, choose transportation modes, estimate time and budget, and assemble practical travel tips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may rely on separate travel or web search tools for real-time transit, weather, lodging, attraction, price, account, or booking information. <br>
Mitigation: Confirm that any connected travel or search tools are trusted before use, especially when they can access accounts, API keys, prices, or booking workflows. <br>
Risk: Generated route details and the local script's transportation recommendations may be incomplete or stale without current travel data. <br>
Mitigation: Review itinerary details and verify transit times, prices, weather, lodging, and attraction hours with current sources before purchasing or traveling. <br>


## Reference(s): <br>
- [Travel route planning tips](references/travel_tips.md) <br>
- [ClawHub release page](https://clawhub.ai/yufish-w/travel-route-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown travel route plan with optional command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include route order, transportation suggestions, stay-duration guidance, budget estimates, and practical travel tips.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
