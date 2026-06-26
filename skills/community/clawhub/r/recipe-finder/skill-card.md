## Description: <br>
Finds and formats recipe suggestions by ingredient, cuisine, or dietary preference using TheMealDB API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harshasic](https://clawhub.ai/user/harshasic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users ask an agent for meal ideas or recipes based on ingredients, cuisine, or dietary preferences. The skill guides the agent to query TheMealDB and present concise recipe summaries with ingredients, cuisine, and brief instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipe search terms may be sent to TheMealDB, so unrelated private information entered into a query could be exposed to that service. <br>
Mitigation: Keep recipe queries limited to ingredients, cuisines, meal names, and dietary preferences. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harshasic/recipe-finder) <br>
- [TheMealDB ingredient filter API](https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}) <br>
- [TheMealDB cuisine filter API](https://www.themealdb.com/api/json/v1/1/filter.php?a={cuisine}) <br>
- [TheMealDB meal search API](https://www.themealdb.com/api/json/v1/1/search.php?s={query}) <br>
- [TheMealDB meal lookup API](https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, API calls] <br>
**Output Format:** [Markdown recipe summaries with optional image thumbnails, category, cuisine, ingredients, and brief instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TheMealDB search and lookup results; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
