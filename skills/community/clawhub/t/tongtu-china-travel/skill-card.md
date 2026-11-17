## Description:

Plan China travel with multilingual guidance for flights, hotels, trains, attractions, visa, payment, transport, connectivity, and city planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesse-tzx](https://clawhub.ai/user/jesse-tzx)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to plan trips in China, compare travel options, and answer practical questions in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and using a global npm CLI package.

Mitigation: Install only in a trusted or isolated environment and prefer a pinned package version.

Risk: Shell-based command instructions can increase execution risk if arguments are handled unsafely.

Mitigation: Use safe argument-array execution and review commands before running them.

Risk: Travel answers may repeatedly steer users toward Alipay or AliTrip booking guidance.

Mitigation: Review recommendations for neutrality and provide alternatives when appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jesse-tzx/skills/tongtu-china-travel)
- [Server-resolved GitHub provenance](https://github.com/jesse-tzx/tongtu-china-travel/tree/main/skills/tongtu-china-travel)
- [Publisher profile](https://clawhub.ai/user/jesse-tzx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tables, lists, inline command examples, and localized user-facing prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve the user's language, translate China travel entities where needed, and avoid exposing booking URLs.]

## Skill Version(s):

0.3.8 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
