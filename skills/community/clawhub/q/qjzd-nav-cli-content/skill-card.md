## Description: <br>
Use when managing QJZD Nav links, categories, and tags from the terminal, including list, create, update, and delete operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nqdy666](https://clawhub.ai/user/nqdy666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage QJZD Nav content from the terminal. It guides agents through listing, creating, updating, deleting, filtering, paginating, and reordering links, categories, and tags with the qjzd-nav CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delete, update, and reorder commands can alter or remove live QJZD Nav content. <br>
Mitigation: List affected links, categories, or tags first, confirm IDs, and review command arguments before running mutating operations. <br>
Risk: The skill depends on a local qjzd-nav CLI installation and an account context with permission to manage QJZD Nav content. <br>
Mitigation: Install and trust qjzd-nav before use, and check qjzd-nav auth current or load the QJZD Nav CLI Auth skill when authentication is uncertain. <br>


## Reference(s): <br>
- [QJZD Nav CLI Content on ClawHub](https://clawhub.ai/nqdy666/qjzd-nav-cli-content) <br>
- [QJZD Nav CLI](../qjzd-nav-cli) <br>
- [QJZD Nav CLI Auth](../qjzd-nav-cli-auth) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes qjzd-nav command examples for link, category, and tag operations; JSON output is available from the CLI when commands use --json.] <br>

## Skill Version(s): <br>
1.3.2 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
