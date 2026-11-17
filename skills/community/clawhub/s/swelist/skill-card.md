## Description:

Helps users find tech internships and new-grad jobs, track local applications, and prepare interview or career-advice responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyuan99](https://clawhub.ai/user/chenyuan99)

### License/Terms of Use:

MIT-0

## Use Case:

External users and job-search agents use this skill to browse software engineering internship and new-graduate listings, manage a local application tracker, and generate interview-prep or career-advice text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read a broad local profile path to resolve tracker settings.

Mitigation: Use an explicit tracker database path and avoid reading unrelated profile content.

Risk: Tracker commands can initialize, add, update, or export application data in local storage.

Mitigation: Confirm with the user before tracker init, add, update, or export operations.

Risk: Interview-prep prompts may include resumes or personal background details sent to jobgpt.

Mitigation: Redact sensitive resume and background details before using jobgpt.

Risk: The artifact installs the external swelist package, which may change independently of this card.

Mitigation: Install a pinned, reviewed swelist package version.

## Reference(s):

- [Swelist ClawHub skill page](https://clawhub.ai/chenyuan99/skills/swelist)
- [Swelist PyPI package](https://pypi.org/project/swelist/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and markdown emitted by CLI commands, with tracker export support for JSON or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or write a local SQLite tracker database and may call the OpenAI API when using jobgpt.]

## Skill Version(s):

1.0.13 (source: server release evidence; artifact frontmatter says 0.1.9)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
