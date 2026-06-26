## Description: <br>
Helps agents use the Wolai Open API to read and write Wolai notes, blocks, pages, and databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cizixiu](https://clawhub.ai/user/cizixiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Wolai workspace users can use this skill to guide an agent through Wolai REST API operations for pages, blocks, databases, and token handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A permanent Wolai token can grant ongoing read/write access if it is exposed or over-permissioned. <br>
Mitigation: Use a dedicated Wolai app with minimum permissions, grant it only to intended pages or databases, store WOLAI_TOKEN in a secure credential mechanism, and rotate the token if exposed. <br>
Risk: Agent-guided API calls can modify Wolai pages or database rows. <br>
Mitigation: Review target page, block, and database IDs before write operations and keep the app scoped to the smallest required Wolai workspace resources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cizixiu/wolai-api-skill) <br>
- [Wolai Developer Center](https://www.wolai.com/dev) <br>
- [Wolai Open API Base URL](https://openapi.wolai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with PowerShell examples and REST API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses WOLAI_TOKEN for Wolai API authorization and targets Windows PowerShell examples.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
