## Description: <br>
Turn recipes into a Todoist Shopping list. Extract ingredients from recipe photos (Gemini Flash vision) or recipe web pages (search + fetch), then compare against the existing Shopping project with conservative synonym/overlap rules, skip pantry staples (salt/pepper), and sum quantities when units match. Also saves each cooked recipe into the workspace cookbook (recipes/). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Borahm](https://clawhub.ai/user/Borahm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and personal automation agents use this skill to extract recipe ingredients from photos or recipe pages, normalize them into shopping-list items, update a Todoist Shopping project, and optionally save a Markdown recipe record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipe photos or text are sent to Gemini for ingredient extraction. <br>
Mitigation: Crop photos to the ingredient list and avoid sending private recipe content unless that external processing is acceptable. <br>
Risk: The skill can create or update tasks in the user's Todoist Shopping project. <br>
Mitigation: Start with --dry-run and review the proposed items before allowing Todoist changes. <br>
Risk: The shell wrapper loads credentials from ~/.clawdbot/.env. <br>
Mitigation: Use the wrapper only when that file contains only the Gemini and Todoist credentials needed for this skill. <br>
Risk: The skill saves recipe records to the local workspace cookbook by default. <br>
Mitigation: Use --no-save for private recipes or when a persistent local cookbook entry is not wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Borahm/recipe-to-list) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands; script output is JSON and saved recipe entries are Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update Todoist Shopping tasks and write recipe files under recipes/ unless dry-run or no-save options are used.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
