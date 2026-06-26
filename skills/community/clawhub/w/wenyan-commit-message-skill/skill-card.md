## Description: <br>
Write git commit messages in Classical Chinese (文言文) when the user explicitly asks for 文言文, 古文, classical Chinese, or 雅驯/骈俪 style commit messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xing-lin](https://clawhub.ai/user/xing-lin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to turn staged or unstaged git diffs into concise Classical Chinese commit messages when that style is explicitly requested. It helps produce a commit subject and, for complex changes, an optional body ready for commit tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git diffs can contain secrets, credentials, or private data that would be exposed to the agent context. <br>
Mitigation: Avoid using the skill on changes that include secrets, credentials, or private data; review the diff before asking the agent to draft a commit message. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text commit message with optional subject and body] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Subject is limited to 50 Chinese characters; optional body lines are limited to 72 characters.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
