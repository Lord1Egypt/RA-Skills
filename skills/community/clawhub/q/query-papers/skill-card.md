## Description: <br>
Searches a user's personal Gitea paper-kb knowledge base with two-stage retrieval and returns grounded Chinese answers with source links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to answer a registered user's questions about content stored in a personal paper-kb repository. It lists the catalog, reads relevant pages, and composes Chinese responses with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an admin-level Gitea token, which can create, read, and write repository data if exposed or over-scoped. <br>
Mitigation: Install only for a controlled Gitea server, use the least-privileged token that works, keep .env out of source control, restrict file permissions, and rotate the token if exposure is suspected. <br>
Risk: User search questions are automatically saved to log.md and may include sensitive research interests or project details. <br>
Mitigation: Inform users before use and change the skill to disable, redact, or periodically purge query logging when retention is not required. <br>


## Reference(s): <br>
- [Query Papers ClawHub page](https://clawhub.ai/myd2002/query-papers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown with source links and JSON-producing helper commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Two-stage retrieval output; user queries may be written to log.md.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
