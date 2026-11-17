## Description:

Pullboard helps agents coordinate long, multi-step work on a shared board where tasks have owners, priority order, dependencies, and independent verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pullboard](https://clawhub.ai/user/pullboard)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Pullboard to keep complex builds moving across one long-running agent or a fleet of agents. The skill guides agents through setup, task creation, claiming work, submitting evidence, and using a different principal to verify completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path uses an unpinned CLI command.

Mitigation: Pin or otherwise verify the Pullboard CLI package before running setup.

Risk: The workflow stores and uses a workspace-scoped bearer token.

Mitigation: Treat the token as a secret, restrict access to the config file, and avoid exposing it in prompts, logs, or shared artifacts.

Risk: Agents may act on mutable remote board items outside the intended project or tool scope.

Mitigation: Authorize board items for the current project before execution and review proposed work against the allowed tool scope.

## Reference(s):

- [Pullboard homepage](https://pullboard.dev)
- [Agent-readable API reference](https://pullboard.dev/docs/llms.txt)
- [OpenAPI schema](https://pullboard.dev/docs/openapi.json)
- [Pullboard documentation](https://pullboard.dev/docs)
- [ClawHub skill page](https://clawhub.ai/pullboard/skills/pullboard)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include bearer-token handling, API request examples, and verification workflow steps.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
