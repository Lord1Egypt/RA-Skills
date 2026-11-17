## Description:

Save and review notes, quotes, articles, links, images, and video references in a personal commonplace book.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gniting](https://clawhub.ai/user/gniting)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use Robin to maintain a local commonplace book, file useful text and media references by topic, search saved entries, and resurface prior notes for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Path configuration and image handling may affect files outside the intended Robin library.

Mitigation: Use a dedicated Robin state directory, keep robin-config.json under user control, and set topics_dir and media_dir only to simple relative values such as topics and media.

Risk: Untrusted local image paths may cause unexpected file access or copying.

Mitigation: Only pass local image paths that the user trusts and expects Robin to copy into the configured media directory.

Risk: Entry deletion can remove saved knowledge if the wrong id is supplied.

Mitigation: Confirm entry ids before using delete operations.

## Reference(s):

- [Robin Skill Page](https://clawhub.ai/gniting/skills/robin)
- [Robin Guide](docs/guide.md)
- [Robin Config Example](references/robin-config-example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown entries, JSON command output, and human-facing recall text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local filesystem state and can copy accepted image assets into the configured media directory.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
