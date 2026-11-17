## Description:

为四口之家（夫妻+爷爷+2岁宝宝）规划一天三餐，结合日期、节气、节日、工作日/周末、带饭、宝宝和老人适口性约束，生成不重样的家常餐食推荐。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongzichixiangjiao](https://clawhub.ai/user/kongzichixiangjiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for Chinese-language household meal planning when they need breakfast, lunch-box, and dinner recommendations tailored to a four-person family with toddler and elder-friendly constraints. The agent runs the local planner, then turns the structured results into concise Markdown meal guidance with prep notes, packing advice, serving order, and child-safety notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records recent meal recommendations in a local history.json file for deduplication.

Mitigation: Use --no-save for test runs that should not write meal history, and use --reset-history only when intentionally clearing that local history.

Risk: Generated meal guidance may not match individual dietary restrictions, allergies, or medical nutrition needs.

Mitigation: Review recommendations before use and adjust ingredients, seasoning, and portioning for household-specific dietary requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kongzichixiangjiao/skills/what-to-eat-today)
- [Dish library](references/dish_library.md)
- [Calendar and seasonal reference](references/calendar.md)
- [Meal planner script](scripts/meal_planner.py)
- [Structured dish library](scripts/dish_library.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown meal plan with tables, short notes, and structured JSON from the local planner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The planner may update a local history.json file for deduplication unless run with --no-save.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
