## Description:

Videoinu platform skill for managing Graph projects, uploading and downloading files, chatting with AI Agents, and running Workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[everfirdev](https://clawhub.ai/user/everfirdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate Videoinu projects from an agent environment: create and inspect Graphs, move files into and out of projects, chat with project-bound agents, and run workflow definitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access tokens may be sent to untrusted destinations if VIDEOINU_API_BASE or direct download URLs are not trusted.

Mitigation: Use the default Videoinu endpoint or another trusted HTTPS endpoint, avoid untrusted direct URLs, and prefer short-lived or least-privilege tokens.

Risk: Saved access keys can create long-lived local credential exposure.

Mitigation: Review credential handling before installation and avoid storing long-lived tokens on disk where possible.

Risk: The agent chat script can approve remote tool actions automatically.

Mitigation: Avoid --auto-approve except in isolated test accounts and review approval requests before allowing actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/everfirdev/skills/videoinu)
- [Publisher Profile](https://clawhub.ai/user/everfirdev)
- [Videoinu](https://videoinu.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts interact with Videoinu using a user-provided access key and return JSON status, identifiers, URLs, downloaded file paths, or agent responses.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
