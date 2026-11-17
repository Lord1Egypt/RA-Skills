## Description:

Searches and references Simpsons episode scripts from Springfield! Springfield!, including quote lookup, episode identification, recurring joke comparison, character briefs, and short sourced excerpts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smev1](https://clawhub.ai/user/smev1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find Simpsons episode titles, script links, short quote excerpts, scene matches, and grounded character-style reference material without loading a full corpus into context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch Simpsons pages from Springfield! Springfield! and cache script data locally.

Mitigation: Review the network behavior before installation, restrict outbound access to the intended source site when practical, and inspect local cache contents before broader deployment.

Risk: Character voice helpers may be used as official-character impersonation or to produce long copyrighted quotations.

Mitigation: Use them as disclosed style-reference tools, avoid claiming official identity, and keep quoted excerpts short.

Risk: Quote and scene matches depend on a user-maintained script source and may be approximate.

Mitigation: Include source links, label approximate matches, and verify important quotations against the linked script page.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smev1/skills/simpsons-search)
- [Springfield! Springfield! Simpsons episode scripts](https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=the-simpsons)
- [Simpsons episode index](references/simpsons-episodes.json)
- [Simpsons character briefs](references/simpsons-characters.json)
- [Simpsons character evidence](references/simpsons-character-evidence.json)
- [Simpsons character dossiers](references/simpsons-character-dossiers.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON result snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include short excerpts, source links when relevant, and an explicit note when a match is approximate.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
