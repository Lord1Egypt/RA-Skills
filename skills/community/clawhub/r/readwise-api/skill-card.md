## Description: <br>
Manage Readwise highlights, books, daily review, and Reader documents (save-for-later / read-it-later). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gchapim](https://clawhub.ai/user/gchapim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to save URLs to Readwise Reader, browse and search reading lists, manage highlights and notes, and review books or daily highlights through the Readwise APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Readwise API token that can access the user's Readwise and Reader account. <br>
Mitigation: Treat READWISE_TOKEN like a password and provide it only in trusted environments. <br>
Risk: Update and delete commands can modify or remove documents and highlights from the user's account. <br>
Mitigation: Review the target item ID and require explicit confirmation before running modifying or deleting commands. <br>


## Reference(s): <br>
- [Readwise & Reader API Reference](references/api.md) <br>
- [Readwise Access Token](https://readwise.io/access_token) <br>
- [Readwise API v2](https://readwise.io/api/v2) <br>
- [Reader API v3](https://readwise.io/api/v3) <br>
- [ClawHub Skill Page](https://clawhub.ai/gchapim/readwise-api) <br>
- [Publisher Profile](https://clawhub.ai/user/gchapim) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands call Readwise and Reader APIs and return compact JSON by default, with optional pretty-printed JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
