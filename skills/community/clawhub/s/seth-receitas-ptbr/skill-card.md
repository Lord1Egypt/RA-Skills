## Description: <br>
Busca receitas em portugues do Brasil (pt-BR) via Wikilivros e TheMealDB, com geracao de receitas originais quando fontes adequadas nao retornam resultados. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runawaydevil](https://clawhub.ai/user/runawaydevil) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External users and agents use this skill to find, retrieve, and format Brazilian Portuguese recipes from public recipe sources, suggest recipes from ingredients, and optionally look up nutrition information. It can generate an original recipe when the supported sources do not return a suitable match. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipe, ingredient, and optional nutrition queries are sent to public third-party services. <br>
Mitigation: Use the skill only when sharing those queries with Wikilivros, TheMealDB, and OpenFoodFacts is acceptable. <br>
Risk: Cached recipe results are stored locally. <br>
Mitigation: Review or clear the local cache when recipe or ingredient queries should not persist on disk. <br>
Risk: Dietary, allergy, religious, or medical suitability may be incomplete or inaccurate. <br>
Mitigation: Manually verify ingredients and nutrition details before relying on the output for strict dietary or health requirements. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/runawaydevil/seth-receitas-ptbr) <br>
- [Publisher profile](https://clawhub.ai/user/runawaydevil) <br>
- [Wikilivros recipes category](https://pt.wikibooks.org/wiki/Categoria:Receitas) <br>
- [Wikilivros MediaWiki API](https://pt.wikibooks.org/w/api.php) <br>
- [TheMealDB](https://www.themealdb.com/) <br>
- [TheMealDB API](https://www.themealdb.com/api/json/v1/1/) <br>
- [OpenFoodFacts](https://world.openfoodfacts.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style recipe text and CLI output in pt-BR] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recipe outputs include title, yield, preparation time, ingredients, numbered preparation steps, tags, and source attribution when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
