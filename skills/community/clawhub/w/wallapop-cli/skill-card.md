## Description: <br>
Use the wallapop CLI to search listings, fetch item details, view user profiles, and list categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pjtf93](https://clawhub.ai/user/pjtf93) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to get concise wallapop-cli commands for searching Wallapop listings, retrieving item or user details, listing categories, and producing JSON output for scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches, location variables, item lookups, user lookups, and optional authenticated requests may be sent to Wallapop's API. <br>
Mitigation: Use the skill only when Wallapop API access is expected, avoid unnecessary precise location values, and set WALLAPOP_ACCESS_TOKEN only when needed. <br>
Risk: The skill provides CLI command guidance that may fail or behave differently if wallapop-cli is missing or incompatible. <br>
Mitigation: Confirm wallapop-cli is installed with Node.js 18 or later and check command exit codes before using generated commands in scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pjtf93/wallapop-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-output examples for scripting.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
