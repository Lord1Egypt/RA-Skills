## Description: <br>
This skill should be used when interacting with the YouMind API to manage content such as boards, crafts, notes, picks, and materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[p697](https://clawhub.ai/user/p697) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover YouMind API endpoints, inspect request schemas, and execute authenticated YouMind CLI calls for boards, crafts, notes, picks, and materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a YouMind API key and can make authenticated changes to account content. <br>
Mitigation: Set YOUMIND_API_KEY through a secure environment or secret manager, avoid command-line API keys, and review YouMind API calls before allowing content changes. <br>


## Reference(s): <br>
- [YouMind API key settings](https://youmind.com/settings/api-keys) <br>
- [YouMind API endpoint](https://youmind.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses YOUMIND_API_KEY or --api-key for authenticated CLI calls.] <br>

## Skill Version(s): <br>
3.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
