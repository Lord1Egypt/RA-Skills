## Description:

Build and drill spaced-repetition packs with recallit: turn a PDF, URL, repo, or plain concept into honest, source-grounded flashcards, then run the daily review loop through the CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanwaits](https://clawhub.ai/user/ryanwaits)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create source-grounded flashcard packs from documents, URLs, repositories, or concepts, then run a chat-mediated review loop where the recallit CLI grades answers. It is suited for study workflows that need local pack authoring, deterministic gating, and spaced-repetition drills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The answer workflow may pass user replies through unsafe shell-style command construction.

Mitigation: Pass user replies as separate process arguments or stdin, and avoid interpolating raw user text into shell commands.

Risk: The installation path uses a global, unpinned CLI package.

Mitigation: Review the package before installing and pin or otherwise control the installed CLI version in managed environments.

Risk: Source documents and generated packs are retained locally for later study.

Mitigation: Avoid sensitive documents or confidential concepts unless the operator controls local retention, storage location, and any network use.

## Reference(s):

- [Recallit ClawHub listing](https://clawhub.ai/ryanwaits/skills/recallit)
- [Publisher profile](https://clawhub.ai/user/ryanwaits)
- [npm package @waits/recallit](https://www.npmjs.com/package/@waits/recallit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local pack files such as manifest.json, cards.json, and .author/source.txt when authoring flashcard packs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
