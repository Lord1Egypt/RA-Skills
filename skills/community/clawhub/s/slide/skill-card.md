## Description:

Create and manage presentation slides using JSONL storage. Use when building slide decks, applying themes, or exporting to HTML presentations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to create, edit, theme, preview, and export local slide decks with speaker notes and built-in templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slide data and speaker notes are stored locally in ~/.slide/data.jsonl.

Mitigation: Install only when local storage of deck content and notes is acceptable, and avoid storing sensitive information unless the local environment is appropriately protected.

Risk: HTML export can turn slide text into executable browser script.

Mitigation: Avoid adding untrusted HTML or text from outside sources, and review exported HTML before sharing or hosting it.

Risk: Exports can write to user-supplied paths and may overwrite existing user-writable files.

Mitigation: Choose export paths carefully and verify the target path before running an export.

## Reference(s):

- [Slide ClawHub Skill Page](https://clawhub.ai/ckchzh/skills/slide)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [JSON command output, text previews, and exported HTML or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores deck and slide records locally in ~/.slide/data.jsonl; HTML exports are self-contained files.]

## Skill Version(s):

2.0.0 (source: release evidence; artifact frontmatter and script report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
