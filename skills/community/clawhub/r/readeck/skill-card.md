## Description:

Readeck integration for saving and managing articles via Readeck's API, including adding URLs, listing entries, and managing bookmarks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayphen](https://clawhub.ai/user/jayphen)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to save articles to a configured Readeck instance, retrieve saved entries, manage bookmark status, and organize bookmarks with tags or collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Readeck API token could be exposed if the API base URL is misconfigured or chosen from task content.

Mitigation: Configure READECK_URL yourself to a trusted HTTPS Readeck instance and keep READECK_API_KEY scoped to that instance.

Risk: Delete operations can remove the wrong bookmark if an incorrect ID is used.

Mitigation: Confirm bookmark IDs carefully before running delete operations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline curl commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted Readeck base URL and API key supplied per request or through READECK_URL and READECK_API_KEY.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
