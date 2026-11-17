## Description:

Busca receitas em portugues do Brasil (pt-BR) via Wikilivros e TheMealDB, and can generate an original recipe when supported sources do not return a suitable result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runawaydevil](https://clawhub.ai/user/runawaydevil)

### License/Terms of Use:

ISC

## Use Case:

External users and agents use this skill to search, retrieve, suggest, or generate Brazilian Portuguese recipe content from supported public recipe sources and ingredient prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dietary restrictions, allergy constraints, religious dietary rules, and vegan or vegetarian requests may not be consistently enforced.

Mitigation: Review every ingredient and preparation step before using a recipe for dietary, allergy, medical, or religious requirements.

Risk: Recipe, ingredient, and nutrition queries may be sent to public recipe or nutrition APIs and cached locally.

Mitigation: Avoid entering sensitive personal information in queries and clear the local cache when cached request data should not persist.

Risk: Nutrition data and generated fallback recipes are suggestions and may be incomplete or inaccurate.

Mitigation: Verify nutrition information against trusted labels or professional sources, and review generated recipes for food-safety and suitability before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runawaydevil/skills/seth-receitas-ptbr)
- [Wikilivros receitas category](https://pt.wikibooks.org/wiki/Categoria:Receitas)
- [Wikilivros MediaWiki API](https://pt.wikibooks.org/w/api.php)
- [TheMealDB](https://www.themealdb.com/)
- [TheMealDB API](https://www.themealdb.com/api/json/v1/1/)
- [OpenFoodFacts](https://world.openfoodfacts.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Portuguese markdown-style text with recipe sections, source attribution, and optional CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include source links or IDs; recipe, ingredient, and nutrition queries can be sent to public APIs and cached locally.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
