## Description:

A personal reading journal that lets an agent log books, recall takeaways, recommend what to read next, and use BlueColumn with a required API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to keep a searchable reading journal, recall book takeaways during conversation, and generate next-read recommendations from stored notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Book notes, preferences, tags, and recall queries are sent to BlueColumn's hosted service.

Mitigation: Avoid storing sensitive personal details unless the provider's retention and privacy practices are acceptable.

Risk: The BLUECOLUMN_API_KEY could be exposed if it is pasted into shared files, logs, or command history.

Mitigation: Keep the API key in a secure environment variable or secret store and avoid hard-coding it in shared artifacts.

## Reference(s):

- [BlueColumn API reference](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/remember-books)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLUECOLUMN_API_KEY; sends book notes, tags, preferences, and recall queries to BlueColumn's hosted service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
