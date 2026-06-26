## Description: <br>
CLI for AI agents to find recipes for their humans. Uses TheMealDB API. No auth required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffaf](https://clawhub.ai/user/jeffaf) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to search for recipes, fetch full recipe details by meal ID, get random meal ideas, list categories, and browse dishes by cuisine through TheMealDB. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package does not include the executable scripts that the README tells users and agents to run. <br>
Mitigation: Inspect the referenced scripts or use a release that includes reviewed executable code before running commands, and avoid running the skill as root. <br>
Risk: Recipe lookup results may omit nutrition, calorie, or dietary restriction information. <br>
Mitigation: Use the skill for recipe discovery and cooking instructions only; verify dietary and nutrition needs with authoritative sources. <br>


## Reference(s): <br>
- [TheMealDB](https://www.themealdb.com) <br>
- [TheMealDB API](https://www.themealdb.com/api.php) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Command-line text with recipe IDs, recipe details, ingredients, instructions, and source links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, and jq; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
