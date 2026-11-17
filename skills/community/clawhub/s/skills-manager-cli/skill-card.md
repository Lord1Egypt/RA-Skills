## Description:

Drive the Skills Manager CLI (`skm`) to initialize the hub, adopt unmanaged skills, list, enable, or disable skills per AI tool, and diagnose or repair symlink synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiweiyeah](https://clawhub.ai/user/jiweiyeah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage Skills Manager CLI workflows from terminal, SSH, CI, or headless environments, including hub initialization, skill adoption, per-tool enablement, and sync repair.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutating commands such as `init`, `adopt --yes`, `enable`, `disable`, and `fix --yes` can change Skills Manager configuration, move skill directories, or create and remove tool links.

Mitigation: Preview affected paths where possible, prefer documented dry-run or JSON inspection commands, and confirm the target tool and skill identifiers before applying changes.

Risk: Ambiguous skill or tool prefixes can target the wrong entry when multiple ids share a prefix.

Mitigation: Resolve exact ids from `skm list --json`, `skm list --tool <id> --json`, or `skm doctor --json`, and rerun with a longer token when the CLI reports ambiguity.

Risk: Automation may misread command success because some JSON-mode commands require checking fields as well as exit codes.

Mitigation: Parse stdout according to `references/json.md`, gate `doctor --json` on `issues_count`, and check `failed_count` after `fix --yes --json`.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiweiyeah/skills/skills-manager-cli)
- [Skills Manager Website](https://skillsmanager.freeourdays.com)
- [Skills Manager Download](https://skillsmanager.freeourdays.com/?ref=clawhub#download)
- [Skills Manager Source and Docs](https://github.com/jiweiyeah/skills-manager)
- [Skills Manager Releases](https://github.com/jiweiyeah/skills-manager/releases)
- [`skm` JSON contracts](references/json.md)
- [Tool ids for `skm --for` / `skm list --tool`](references/tools.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, json, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON parsing notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct agents to run mutating filesystem commands only after previewing or confirming affected tools, skills, and paths.]

## Skill Version(s):

2.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
