## Description: <br>
Run Seongnam Library tasks from the command line, including login, book search, account status checks, interlibrary loan requests, hope-book requests, and basket queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruseel](https://clawhub.ai/user/ruseel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Library users and agents use this skill to run Seongnam Library CLI workflows for discovery, account/session checks, loan status, interlibrary loan requests, hope-book requests, and basket queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated commands use a Seongnam Library account and may expose credentials if pasted into shared terminals, logs, or chat transcripts. <br>
Mitigation: Pass credentials through SNLIB_USER and SNLIB_PASSWORD only in trusted environments, and avoid sharing real passwords or personal details in logs or transcripts. <br>
Risk: Interlibrary loan and hope-book request commands can submit real requests on the user's account. <br>
Mitigation: Start with read-only commands and manually review any interloan-request or hope-book-request command before execution. <br>
Risk: The wrapper downloads and runs the upstream snlib-cli Clojure dependency on first execution. <br>
Mitigation: Install only when you trust the upstream snlib-cli package and are comfortable using your Seongnam Library account with it. <br>


## Reference(s): <br>
- [Command patterns](references/commands.md) <br>
- [Library code reference](references/lib-code.md) <br>
- [Manage code reference](references/manage-code.md) <br>
- [Skill page](https://clawhub.ai/ruseel/snlib-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require bash, Java, Clojure, and SNLIB_USER/SNLIB_PASSWORD for authenticated operations.] <br>

## Skill Version(s): <br>
2026.4.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
