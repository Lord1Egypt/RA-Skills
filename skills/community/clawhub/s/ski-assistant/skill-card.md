## Description: <br>
Global ski resort assistant for trip planning, price comparison, technique coaching, presale monitoring, mountain weather checks, and packing guidance across 854 resorts in 40+ countries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjyhahaha](https://clawhub.ai/user/wjyhahaha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ski and snowboard users use this skill to choose resorts, estimate trip costs, compare lift-ticket and travel prices, prepare for departures, and get structured technique feedback. It supports English and Chinese ski-planning workflows with live web/API lookups when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain local ski profile, trip, watchlist, price-history, custom-resort, coaching-history, usage-stat, and export files. <br>
Mitigation: Tell users when persistent files are used, keep the data under the documented ~/.ski-assistant directory or SKI_ASSISTANT_DATA_DIR override, and let users review or remove saved records. <br>
Risk: Live web, weather, currency, and resort lookups can fail, be stale, or return inconsistent prices. <br>
Mitigation: Label every price and forecast source, disclose fallback behavior, and avoid treating estimated or database-reference values as current confirmed prices. <br>
Risk: Reminder and notification workflows could contact users at the wrong time or through the wrong channel. <br>
Mitigation: Create reminders only after explicit user confirmation of destination, dates, notification channel, and cancellation expectations. <br>
Risk: Skiing guidance and coaching feedback can affect physical safety. <br>
Mitigation: Include helmet, ski-specific insurance, rescue coverage for international trips, and practical safety reminders in trip, price, and departure outputs. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/wjyhahaha/ski-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/wjyhahaha) <br>
- [Travel Guide](artifact/references/travel-guide.md) <br>
- [Budget Templates](artifact/references/budget-templates.md) <br>
- [Coaching Rubric](artifact/references/coaching-rubric.md) <br>
- [Pre-Departure Checklist](artifact/references/pre-departure-checklist.md) <br>
- [Gear Guide](artifact/references/gear-guide.md) <br>
- [Resorts Reference](artifact/references/resorts-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, checklists, source labels, and occasional shell commands for local tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local profile, trip, watchlist, coaching-history, price-history, custom-resort, usage-stat, and export files under ~/.ski-assistant when the user requests persistent planning or coaching workflows.] <br>

## Skill Version(s): <br>
7.0.0 (source: server release metadata and artifact/SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
