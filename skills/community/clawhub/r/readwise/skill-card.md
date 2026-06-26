## Description: <br>
Access Readwise highlights and Reader saved articles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[refrigerator](https://clawhub.ai/user/refrigerator) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to list, search, export, and retrieve Readwise highlights and Reader documents, and to save URLs into Reader when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Readwise token that can read private highlights, notes, saved article metadata and content, and can save URLs to Reader when explicitly invoked. <br>
Mitigation: Install only in trusted agent environments, provide READWISE_TOKEN only when needed, review commands before execution, and revoke or rotate the token if access is no longer required. <br>


## Reference(s): <br>
- [Readwise](https://readwise.io) <br>
- [Readwise Access Token](https://readwise.io/access_token) <br>
- [Readwise API Documentation](https://readwise.io/api_deets) <br>
- [Reader API Documentation](https://readwise.io/reader_api) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples; invoked scripts return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and READWISE_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
