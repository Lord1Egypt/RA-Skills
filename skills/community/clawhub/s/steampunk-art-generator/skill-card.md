## Description:

AI steampunk art generator - create Victorian steampunk portraits, cyberpunk Victorian characters, brass-and-gears illustrations, cosplay reference art, and industrial fantasy scenes via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, cosplayers, worldbuilders, and developers use this skill to generate steampunk-themed image URLs from text prompts through the Neta API. It supports selectable image dimensions and optional reference image UUIDs for style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Neta API tokens can be exposed through shell history, command logs, or process monitoring when passed directly on the command line.

Mitigation: Use a dedicated low-value token, prefer environment-variable expansion over literal token text, and rotate the token if it may have been logged.

Risk: Unpinned installation commands can retrieve a changed package version later.

Mitigation: Install through ClawHub or another trusted pinned installer when possible, and review the skill before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/skills/steampunk-art-generator)
- [Publisher Profile](https://clawhub.ai/user/blammectrappora)
- [Neta API Token Access](https://www.neta.art/open/)
- [Neta Image Generation API Endpoint](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text image URL with command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; optional size and reference image UUID parameters influence generated image dimensions and style.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
