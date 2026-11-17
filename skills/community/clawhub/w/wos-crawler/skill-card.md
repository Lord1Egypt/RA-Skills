## Description:

WOS Crawler helps agents guide users through Web of Science literature searching, Excel export, and batch PDF downloading through a local Web UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grizzlyccc](https://clawhub.ai/user/grizzlyccc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to help agents start a local Web of Science and PDF workflow, prompt for WOS search criteria or an existing export, and guide users through PDF download results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence says the main crawling script was removed, which may disable the core WOS crawling workflow.

Mitigation: Confirm the installed package includes the expected Web UI and crawler implementation before relying on the skill.

Risk: The security evidence says WOS session cookies may be saved locally.

Mitigation: Use a dedicated virtual environment and review local cookie storage behavior before authenticating with institutional credentials.

Risk: The security evidence flags institutional terms, copyright, and Sci-Hub access implications.

Mitigation: Confirm the workflow complies with institutional access terms, copyright obligations, and local policy before downloading papers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/grizzlyccc/skills/wos-crawler)

## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and file workflow descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of Excel exports and downloaded PDF files through the local Web UI.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
