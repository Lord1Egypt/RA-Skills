## Description:

Automatically batch uploads modified _GM.fit files to the Blackbird Cycling web platform with login detection and upload status handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckboss](https://clawhub.ai/user/ckboss)

### License/Terms of Use:

MIT-0

## Use Case:

Cyclists and developers use this skill to run a browser-assisted workflow that uploads selected FIT activity files, especially _GM.fit files, to Blackbird Sport. It supports single-file, directory, and glob-based upload workflows while prompting for manual login when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passing a broad directory or glob can upload FIT files the user did not intend to send to Blackbird.

Mitigation: Only pass directories or patterns containing FIT files intended for upload, and review the matched files before running the workflow.

Risk: The workflow depends on Playwright browser automation and a manual login session with the Blackbird website.

Mitigation: Install and run the skill in an isolated environment when possible, review or pin the Playwright dependency, and complete login only in the browser opened for this workflow.

## Reference(s):

- [Blackbird Sport](https://www.blackbirdsport.com)
- [ClawHub skill page](https://clawhub.ai/ckboss/skills/upload-fit-to-blackbird-web)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for manual browser login when needed and reports upload status for selected FIT files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
