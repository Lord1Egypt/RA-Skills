## Description: <br>
Book winter escape flights to warm destinations for a winter sun getaway, with support for flight booking and related travel planning tasks powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liquanyu123](https://clawhub.ai/user/liquanyu123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search winter escape flights, compare recommended, cheapest, fastest, or direct options, and format live booking results with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run an unpinned global CLI package from npm. <br>
Mitigation: Install and verify @fly-ai/flyai-cli separately before use, or run the skill in an isolated environment. <br>
Risk: The skill handles travel searches that may involve personal travel preferences or account context. <br>
Mitigation: Provide only the travel details needed for the search and avoid unnecessary personal or account information. <br>
Risk: Flight availability and prices can change quickly and may be misleading if results are not generated from live CLI output. <br>
Mitigation: Require current flyai CLI output and booking detailUrl links for any listed flight results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liquanyu123/winter-escape-flight) <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown flight-search summaries with inline booking links and supporting shell commands when setup or execution is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should be based on flyai CLI output and include Book links when flight options are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
