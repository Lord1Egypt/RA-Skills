## Description:

Xiaoqinli (XQL) helps agents write structured .xql.json AST files and compile them to Go, Rust, TypeScript, Kotlin, Swift, or Python with type, effect, and capability checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freecode100year](https://clawhub.ai/user/freecode100year)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent builders use Xiaoqinli to validate structured XQL AST files and generate source code for supported languages while checking types, effects, and declared capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance builds mutable third-party source and may place the resulting binary on the system PATH.

Mitigation: Review the upstream repository before installing, pin a release or commit with a verified checksum, build as an unprivileged user, and prefer a user-local bin directory unless system-wide access is required.

## Reference(s):

- [Xiaoqinli ClawHub skill page](https://clawhub.ai/freecode100year/skills/xiaoqinli)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the xql binary; building from source requires Go 1.23 or later.]

## Skill Version(s):

2.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
