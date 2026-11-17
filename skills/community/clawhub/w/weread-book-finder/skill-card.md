## Description:

Finds a requested book by first searching WeRead and adding a confident match to the user's shelf, then falling back to Z-Library download when WeRead cannot add the book.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinntrance](https://clawhub.ai/user/jinntrance)

### License/Terms of Use:

MIT-0

## Use Case:

Readers and agents use this skill to automate book lookup requests such as adding a title to a WeRead shelf or, when that fails, downloading an ebook fallback. It supports title and author hints, candidate reporting, login setup, and headed browser debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent browser profiles can retain WeRead and Z-Library login sessions.

Mitigation: Use a dedicated skill profile, avoid shared machines, and clear the profile after use when credentials should not persist.

Risk: The fallback path may save downloaded ebook files locally from Z-Library.

Mitigation: Use the skill only for content the user is authorized to access, and review downloaded files and their location before opening or sharing them.

Risk: Automation can add a matched title to the user's WeRead shelf.

Mitigation: Provide precise title and author hints for ambiguous books and review candidate output when confidence is uncertain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinntrance/skills/weread-book-finder)
- [Publisher profile](https://clawhub.ai/user/jinntrance)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance with shell commands, JSON status output, and locally saved ebook files when fallback download succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reuse a persistent browser profile for WeRead and Z-Library login sessions and may save downloads under ~/Downloads/OpenClaw-Books.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
