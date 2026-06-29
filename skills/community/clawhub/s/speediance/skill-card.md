## Description: <br>
Read completed workouts, browse and export the exercise catalog, and push custom training programs to a Speediance Gym Monster smart cable machine through the Speediance cloud API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stozo04](https://clawhub.ai/user/stozo04) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and compatible agents use this skill to retrieve Speediance workout history, inspect exercise catalog data, and create account-owned training programs from structured plan JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Speediance account credentials and caches a live session token. <br>
Mitigation: Prefer environment variables or a secret manager over plaintext config files, keep the token cache private, and avoid committing config, .env, or token files. <br>
Risk: The skill can create training programs on the user's Speediance account. <br>
Mitigation: Use the push command's --dry-run mode before creating programs and use the skill only with an account the user owns. <br>
Risk: The integration uses an unofficial Speediance API client, so upstream API changes can affect behavior. <br>
Mitigation: Use the latest released version, review command output before relying on it, and treat returned workout fields as source API data rather than corrected metrics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stozo04/speediance) <br>
- [Project homepage](https://github.com/stozo04/speediance-cli) <br>
- [Release binaries](https://github.com/stozo04/speediance-cli/releases) <br>
- [Go package documentation](https://pkg.go.dev/github.com/stozo04/speediance-cli) <br>
- [Security policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI commands described by the skill emit parseable JSON for workout, session, catalog, configuration, version, and dry-run program payload outputs.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
