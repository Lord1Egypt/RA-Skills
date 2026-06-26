## Description: <br>
Web UI for the shopping-list skill that adds a /shopping page to Second Brain with full CRUD operations for viewing, adding, editing, checking off, and deleting items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajeenkya](https://clawhub.ai/user/ajeenkya) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Second Brain users use this skill to add a web shopping-list interface that shares data with the existing conversational shopping-list skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated app changes include API routes that can modify and delete items in the shared shopping-list data file. <br>
Mitigation: Review generated local diffs during installation and confirm the API behavior matches the intended CRUD workflow before deployment. <br>
Risk: The UI shares data with the conversational shopping-list skill, so changes from either interface affect the same active list. <br>
Mitigation: Confirm the shared data path and user identity configuration before using the web UI with important list data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ajeenkya/shopping-list-ui) <br>
- [Publisher profile](https://clawhub.ai/user/ajeenkya) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions describing Next.js files, API routes, navigation updates, and shared data behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Second Brain portal and the shopping-list skill; reads and writes the shared shopping-list JSON data file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
