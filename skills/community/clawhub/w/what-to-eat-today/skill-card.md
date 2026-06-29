## Description: <br>
为四口之家规划一天三餐，结合节日节气、周末季节、电饭锅预约、蒸菜便当、宝宝和老人适口性，以及跨会话排重来生成不重复的家常饭菜建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongzichixiangjiao](https://clawhub.ai/user/kongzichixiangjiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
家庭用户可用此技能在日常不知道吃什么时生成早饭、午饭便当和晚饭安排。代理先运行本地规划脚本选择日期感知且排重后的菜品，再用参考菜库补全做法要点、预处理、便当打包和宝宝老人注意事项。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The planner may update local meal history when run, which can affect future recommendations. <br>
Mitigation: Use the documented --no-save option for testing or --reset-history when the recommendation history should be cleared. <br>
Risk: Meal suggestions may not match allergies, dietary restrictions, choking hazards, or medical nutrition needs. <br>
Mitigation: Review recommendations before use and adapt ingredients, seasoning, texture, and portions for the household. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kongzichixiangjiao/what-to-eat-today) <br>
- [Dish library reference](references/dish_library.md) <br>
- [Calendar and seasonal reference](references/calendar.md) <br>
- [Meal planner script](scripts/meal_planner.py) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown meal plan with tables; the planner script emits JSON for agent use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local dish library and may update a small local meal-history file to avoid repeated recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
