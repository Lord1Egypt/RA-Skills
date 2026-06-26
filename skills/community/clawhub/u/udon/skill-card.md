## Description: <br>
Search and browse 100 curated Japanese udon noodle recipes from Cookpad by keyword, ingredient, category, or recipe number. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to find udon recipe ideas and retrieve matching recipe titles, ingredients, and source links from a curated Cookpad-derived reference list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs publisher-provided Python locally. <br>
Mitigation: Review the bundled script and run it only in environments where local execution of a small stdlib Python helper is acceptable. <br>
Risk: Search results include links to third-party Cookpad recipe pages. <br>
Mitigation: Treat opened recipe links as external websites and apply normal browser and organizational link-handling controls. <br>
Risk: Recipe search output may be incomplete or may not match every user intent. <br>
Mitigation: Use broader keywords or browse the full recipe list when a query returns no matches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/udon) <br>
- [100 Udon Noodle Recipes](references/recipes.md) <br>
- [Cookpad Udon category](https://cookpad.com/jp/categories/70) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown recipe search results with recipe titles, ingredients, and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python stdlib script reads the bundled recipe reference and prints matching results.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
