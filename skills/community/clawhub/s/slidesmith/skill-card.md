## Description:

Edit a Google Slides deck in place from the command line: pull it to editable local SML, change it with semantic selectors, roles, components, images, and layout, preview an exact diff, and push batchUpdates back to the same deck.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bek91](https://clawhub.ai/user/bek91)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use slidesmith to create, inspect, restyle, and update native Google Slides decks while preserving editability and Drive history. It is suited for deck creation, deck-wide styling, image and layout work, QA checks, and controlled pushes to live presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live deck operations such as push, replace-image, group, reorder, create, and share can modify Google Slides or Drive state.

Mitigation: Review diffs, use dry-run where available, and prefer test copies for important decks before applying changes.

Risk: OAuth material may be exposed if insecure credential-file fallback is used.

Mitigation: Use OS keyring or managed secrets where possible, avoid insecure credential-file fallback unless the local storage risk is understood, and revoke or rotate tokens if credential files are exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bek91/skills/slidesmith)
- [slidesmith homepage](https://github.com/unblocklabs-ai/slidesmith)
- [recipes.md](recipes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, SML/XML snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide live Google Slides actions through the slidesmith CLI; users should preview diffs before pushing changes.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
