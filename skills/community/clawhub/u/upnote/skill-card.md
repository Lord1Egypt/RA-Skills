## Description:

Manage UpNote notes and notebooks via x-callback-url automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wemcdonald](https://clawhub.ai/user/wemcdonald)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to create, open, search, and navigate UpNote notes, notebooks, tags, filters, and views through the bundled shell wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open UpNote and create or navigate notes on the user's behalf.

Mitigation: Install and use it only when local UpNote automation through agent-generated commands is acceptable.

Risk: Some note, notebook, tag, filter, or space identifiers may include URL-special characters that are not consistently encoded.

Mitigation: Avoid untrusted or unusual IDs until URL parameters are encoded consistently across all script operations.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands that open the local UpNote application through x-callback-url automation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
