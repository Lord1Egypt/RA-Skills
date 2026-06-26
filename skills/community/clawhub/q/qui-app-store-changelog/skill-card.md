## Description: <br>
Create user-facing App Store release notes by collecting and summarizing all user-impacting changes since the last git tag or a specified ref. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release managers use this skill to turn git history into concise App Store release notes that emphasize user-visible changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local git history, commit messages, touched file paths, and repository context that may contain internal information. <br>
Mitigation: Use it only in repositories where those details are appropriate for the agent to inspect. <br>
Risk: Generated release notes may accidentally include internal implementation details or expose information unsuitable for App Store publication. <br>
Mitigation: Review the generated notes before publishing and remove internal details, technical jargon, ticket IDs, and file paths. <br>


## Reference(s): <br>
- [App Store Release Notes Guidelines](references/release-notes-guidelines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/quincygunter/qui-app-store-changelog) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown bullet list with optional title] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output should use concise, user-facing language and avoid internal jargon, ticket IDs, file paths, and purely technical implementation details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
