## Description:

Use the SeggWat CLI to manage feedback, projects, and ratings from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hauju](https://clawhub.ai/user/hauju)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to install and authenticate the SeggWat CLI, query and triage feedback, inspect rating statistics, and script feedback workflows in CI/CD.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI from an untrusted or floating source can run unexpected code.

Mitigation: Install only from trusted SeggWat release sources and prefer pinned versions when available.

Risk: API keys can be exposed if passed on the command line or committed into scripts.

Mitigation: Store API keys in environment variables or a secrets manager, and avoid embedding tokens in command arguments or files.

Risk: Create, update, delete, archive, or CI automation commands can change production feedback data.

Mitigation: Require explicit confirmation before mutating production projects and test automation against non-production projects first.

## Reference(s):

- [SeggWat CLI Skill Page](https://clawhub.ai/hauju/skills/seggwat-cli)
- [SeggWat Platform](https://seggwat.com)
- [SeggWat Shell Installer](https://seggwat.com/static/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that call the SeggWat service and produce JSON when --json is requested.]

## Skill Version(s):

0.17.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
