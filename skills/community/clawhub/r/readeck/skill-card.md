## Description: <br>
Readeck integration for saving and managing articles. Supports adding URLs, listing entries, and managing bookmarks via Readeck's API. Configure custom URL and API key per request or via environment variables READECK_URL and READECK_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jayphen](https://clawhub.ai/user/Jayphen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to save URLs to Readeck, list saved entries, inspect individual bookmarks, delete entries, and mark articles as read through the Readeck API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may send bookmark requests to the wrong Readeck server if READECK_URL is misconfigured. <br>
Mitigation: Verify that READECK_URL points to the intended Readeck instance before using the skill. <br>
Risk: The skill uses a Readeck API key that grants the agent access to bookmark operations. <br>
Mitigation: Provide only an API key that is appropriate for agent use and rotate or revoke it if exposure is suspected. <br>
Risk: Update or delete operations can affect the wrong bookmark if the entry ID is incorrect. <br>
Mitigation: Confirm bookmark IDs before marking entries as read or deleting entries. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses READECK_URL and READECK_API_KEY or per-request URL and API key values.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
