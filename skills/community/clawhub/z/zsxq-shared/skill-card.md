## Description: <br>
Guides agents using zsxq-cli through authentication, configuration diagnostics, low-level API calls, share-link construction, write/delete confirmation rules, feedback prompts, and common error handling for 知识星球. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zsxq](https://clawhub.ai/user/zsxq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users operating 知识星球 through zsxq-cli use this skill to log in, check CLI configuration, call supported or raw APIs, produce desktop and mobile share links, and recover from common authentication or HTTP errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to operate zsxq-cli with a user's authenticated account. <br>
Mitigation: Install only when the user intends agent access through zsxq-cli, and avoid sharing token or credential-bearing terminal output. <br>
Risk: Raw API, posting, editing, deleting, or feedback-submission actions can change user-visible 知识星球 content or account state. <br>
Mitigation: Review and explicitly approve those actions before execution, and confirm resource identifiers before write or delete operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zsxq/zsxq-shared) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zsxq) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include share-link URL templates and JSON parameter examples for zsxq-cli API commands.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
