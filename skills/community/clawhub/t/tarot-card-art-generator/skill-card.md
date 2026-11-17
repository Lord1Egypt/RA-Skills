## Description:

Generate stunning AI tarot card art and mystical oracle deck illustrations with custom major and minor arcana, divination, spiritual, occult-themed, and fortune card visuals via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate tarot, oracle, divination, and occult-themed image artwork from text prompts through the Neta/TalesOfAI image API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and the Neta token are sent to the Neta/TalesOfAI image API.

Mitigation: Install only if this external API use is acceptable for the intended data, and avoid sending sensitive prompts or secrets.

Risk: Passing the token directly on the command line can expose it through shell history, shared transcripts, or logs.

Mitigation: Avoid placing real tokens in shared logs or transcripts, prefer a pinned install source, and rotate the token if it has already been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/tarot-card-art-generator)
- [Neta AI token signup](https://www.neta.art/open/)
- [TalesOfAI image creation endpoint](https://api.talesofai.com/v3/make_image)
- [TalesOfAI task polling endpoint](https://api.talesofai.com/v1/artifact/task/${taskUuid})

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [Plain text image URL with status messages on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token passed with --token; supports size selection and optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
