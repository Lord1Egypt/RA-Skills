## Description:

This skill should be used when interacting with the YouMind API to manage content such as boards, crafts, notes, picks, and materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[p697](https://clawhub.ai/user/p697)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to discover YouMind API endpoints, inspect request schemas, and run authenticated YouMind CLI calls for boards, crafts, notes, picks, and materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A global npm install can execute package installation logic from the @youmind-ai/cli package source.

Mitigation: Install only from a trusted package source and avoid elevated privileges during installation.

Risk: Passing a real API key directly with --api-key can expose credentials through shell history or process metadata.

Mitigation: Use YOUMIND_API_KEY or another protected secret mechanism instead of putting real keys in commands.

Risk: Authenticated YouMind API calls may create or modify user content.

Mitigation: Inspect endpoint schemas and review potentially destructive calls before allowing an agent to execute them.

## Reference(s):

- [YouMind API key settings](https://youmind.com/settings/api-keys)
- [YouMind default API endpoint](https://youmind.com)
- [YouMind ClawHub skill page](https://clawhub.ai/p697/skills/youmind)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include YouMind CLI command sequences and authenticated API call guidance.]

## Skill Version(s):

3.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
