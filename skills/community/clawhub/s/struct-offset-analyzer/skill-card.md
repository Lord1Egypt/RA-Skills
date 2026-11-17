## Description:

Statically analyze C struct member offsets through code reading to calculate memory layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littleenough](https://clawhub.ai/user/littleenough)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and security engineers use this skill to calculate C struct member offsets from source code when reverse engineering, debugging, or analyzing binary layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Offset calculations can be wrong when the target platform, compiler ABI, packing pragmas, or conditional compilation differ from the assumptions used during analysis.

Mitigation: Confirm the target platform, compiler, packing directives, and active conditional compilation before relying on calculated offsets.

Risk: Manual layout analysis can miss nested structs, typedef aliases, enum sizes, constants, or union behavior that affects member offsets.

Mitigation: Collect definitions for nested types, aliases, constants, enums, and unions before producing the final offset table.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/littleenough/skills/struct-offset-analyzer)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with offset tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces manual analysis guidance; no hidden execution, persistence, credentials, or network behavior is identified by the security evidence.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
