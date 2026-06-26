## Description: <br>
Travel Planner helps agents plan itineraries, estimate trip budgets, recommend attractions, query weather and currency data, generate packing lists, and export itinerary files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, assistants, and developers use this skill to produce itinerary plans, destination-aware budgets, packing checklists, weather lookups, currency conversions, and itinerary exports for common travel destinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency versions are lower-bounded but not pinned, which can introduce environment drift in production use. <br>
Mitigation: Install the skill in a virtual environment and pin or review dependencies before production deployment. <br>
Risk: Weather and currency helper commands send destination, coordinate, or currency queries to external API providers. <br>
Mitigation: Review provider data-sharing expectations before use and avoid sending sensitive travel information through these commands. <br>
Risk: Travel estimates and fallback exchange rates may be approximate or stale. <br>
Mitigation: Treat generated plans and budgets as drafts and verify costs, schedules, exchange rates, and availability with authoritative providers before booking. <br>


## Reference(s): <br>
- [Travel Planner Skill Page](https://clawhub.ai/kaiyuelv/smart-travel-planner) <br>
- [Destinations Database](references/destinations-database.md) <br>
- [Budget Templates](references/budget-templates.md) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>
- [ExchangeRate API endpoint](https://api.exchangerate-api.com/v4/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands and JSON, CSV, or text file outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write itinerary, budget, packing, weather, currency, text, or CSV outputs to user-selected local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
