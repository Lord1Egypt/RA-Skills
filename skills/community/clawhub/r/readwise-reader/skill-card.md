## Description: <br>
Interact with Readwise Reader library to list, create, update, and delete documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xinthink](https://clawhub.ai/user/xinthink) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to manage a Readwise Reader library, including listing saved items, saving new URLs or content, updating metadata, archiving documents, deleting documents, and listing tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires READWISE_ACCESS_TOKEN to access a user's Readwise Reader library. <br>
Mitigation: Keep the token private, avoid committing or sharing .env files, and prefer shell/session secrets or a secret manager. <br>
Risk: Update and delete actions can modify or remove Reader documents. <br>
Mitigation: Review document IDs and payloads before execution, use dry-run options where available, and avoid delete --confirm unless deletion is intentional. <br>


## Reference(s): <br>
- [Readwise Reader on ClawHub](https://clawhub.ai/xinthink/readwise-reader) <br>
- [Reader Scripts Usage Guide](references/usage-guide.md) <br>
- [Readwise Access Token](https://readwise.io/access_token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads; scripts return JSON or JSON Lines.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, pip, and READWISE_ACCESS_TOKEN.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
